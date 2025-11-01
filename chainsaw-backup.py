#declare
from os import system
from os import getcwd 
import sys
import subprocess
from time import sleep
#define
target_dirs=[]
backup_dir=''
config=''
#functions
def kill():     #immediately terminate the program
    sys.exit() 
def help():     #dislpay help information
    print('chainsaw-backup help:')
def output(string):
    return(subprocess.check_output(string, shell=True, text=True))
#start up routine
if output('silly-software/')=='bash: silly-software/: Is a directory':
    if output('silly-software/chainsaw-backup')=='bash: silly-software/chainsaw-backup/: Is a directory':
        if 'No such file or directory' not in output('cat silly-software/chainsaw-backup/config'):
            print('All files intact')
            config=open()
else:
    system('mkdir silly-software/')
    system('mkdir silly-software/chainsaw-backup/')
#mainloop
while True:
    inp=(input())
