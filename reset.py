__author__ = 'Nina Stawski'
__contact__ = 'me@ninastawski.com'

import os

def resetParpar():
    """
    Removes all files from working directories, invokes parpar setup
    """
    os.remove('parpar.db')
    dirs = ['esc', 'incoming', 'logs', 'tables']
    for dir in dirs:
        files = os.listdir(dir)
        for file in files:
            os.remove(dir + os.sep + file)
    import setup
    setup.setup()

if __name__ == '__main__':
    resetParpar()