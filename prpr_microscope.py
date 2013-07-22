#!/usr/bin/env python3

# prpr_human.py, a part of PR-PR (previously known as PaR-PaR), a biology-friendly language for liquid-handling robots
# Author: Nina Stawski, nstawski@lbl.gov, me@ninastawski.com
# Copyright 2012-2013, Lawrence Berkeley National Laboratory
# http://github.com/JBEI/prpr/blob/master/license.txt

__author__ = 'Nina Stawski'
__version__ = '0.6'

import os
from prpr import *

class PRPR:
    def __init__(self, ID):
        print('_yay, microscope!_')
        self.expID = ID
        db = DatabaseHandler(ID)
        self.transfers = db.transfers
        self.logger = []
        self.robotConfig = []
        self.transactions = []
        self.createTransfer()
        self.saveLog()
        self.saveConfig()

    def createTransfer(self):
        self.config('import microscope')
        self.config('import os')
        self.config('')
        self.config('d = microscope.director')
        self.config('proj_dir = os.path.join(d.root_directory, "Local Storage", "experiment_' + str(self.expID) + '")')
        self.config('if not os.path.exists(proj_dir):')
        self.config('\tos.makedirs(proj_dir)')
        self.config('d.set_working_directory(proj_dir)')
        self.config('')
        self.config('d.turn_light(1, True)')
        self.config('')
        
        allTransfers = self.transfers
        print('allTransfers', allTransfers)
        for transfer in allTransfers:
            print('transffffferrrr', transfer)
            trType = transfer['type']
            els = transfer['info']
            if trType == 'command':
                self.parseCommand(els)

    def config(self, line):
        self.robotConfig.append(line)

    def saveConfig(self):
        def writeLines(file):
            for line in self.robotConfig:
                file.write(line.rstrip() + '\n')
                
        fileName = 'esc' + os.sep + 'config' + self.expID + '.py'
        with open(fileName, 'a') as myfile:
            writeLines(myfile)

    def log(self, item):
        from datetime import datetime
        time = str(datetime.now())
        self.logger.append(time + ': ' + item)

    def saveLog(self):
        logname = 'logs/experiment' + self.expID + '.log'
        self.log('Translation log location: ' + logname)
        writefile = open(logname, "a")
        writefile.writelines( "%s\n" % item for item in self.logger )
        print('Translation log location: ' + logname)

    def message(self, message):
        self.addWash()
        command = '# ' + message
        self.config(command)

    def comment(self, comment):
        command = '# ' + comment
        self.config(command)

    def command(self, action, tipNumber, gridAndSite, wellString, method, volumesString):
        location = str(gridAndSite[0]) + ',' + str(gridAndSite[1])
        command = action            + '(' + \
                  str(tipNumber)    + ',"' + \
                  method            + '",' + \
                  volumesString     + ',' + \
                  location          + ',1,"' + \
                  wellString        + '",0);'
        self.config(command)

    def parseCommand(self, transferList):
        tr = transferList
        for option in tr:
            if option['command'] == 'move':
                loc = option['location']
                self.config('d.reset_position' + loc)
                self.config('d.take_snapshot()')
            if option['command'] == 'comment':
                self.config('# ' + option['message'])
    
class defaults:
    fileExtensions = {'py' : 'py'}

if __name__ == '__main__':
    prpr = Prpr_Tecan(310)
    print('Config:')
    for element in prpr.robotConfig:
        print(element)