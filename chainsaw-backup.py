#declare
import os
from os import system
from os import getcwd 
import sys
import subprocess
from time import sleep
from pathlib import Path
#define
target_dirs=[]
backup_dir=''
config={}
target_dirs=[]
period_int=0
valid=False
entries_int=0
home = Path.home()
#functions
def kill():                 #immediately terminate the program
    sys.exit() 
def help():                 #dislpay help information
    print('---chainsaw-backup help---')
    print('Commands:\nconfigure -- reconfigure backup options\ncheck_integrity -- verify integrity of configuration files')
def output(string):         #check output for shell command
    return(str(subprocess.check_output(string, shell=True, text=True)))
def check_dir(directory):
    expanded_directory = os.path.expanduser(directory)  #expand tilde
    return(os.path.isdir(expanded_directory))
def check_file(path_to_file):
    expanded_file_path = os.path.expanduser(path_to_file)  #expand tilde
    return(os.path.isfile(expanded_file_path))
def expand_path(path):      #somehow some things don't work without expanding the path, as in the functions above, some python quirk prolly
    #yeah it really does demand expanding ~ to full home somehow. It works, I won't dare to complain
    return(os.path.expanduser(path))
def configure():            #configure manually
    try:
        file=open(expand_path('~/silly-software/chainsaw-backup/config.json'), 'w+')
    except:
        com='touch '+expand_path('~/silly-software/chainsaw-backup/config.json')
        system(com)
        file=open(expand_path('~/silly-software/chainsaw-backup/config.json'), 'w+')
    print('---Configuration---')
    print('Path to directory containing backups')
    print('e.g. ~/folder1/folder2/')
    inp=input('>>> ')
    while not check_dir(str(inp)):
        temp_dir=inp
        print('Please enter a valid value, check for typos or make sure the directory exists')
        print('Enter y to override and attempt to create the folder')
        inp=input('>>> ')
        if inp=='y':
            try:
                com='mkdir -p',expand_path(str(temp_dir))
                print("Created:",expand_path(temp_dir))
                break
            except:
                print('Bash has returned an exception while creating a directory; please enter a valid value!')
    backup_dir=str(inp)
    print()
    print('Paths to directories to backup')
    print('Add several, then return an empty line once done')
    inp=''
    while inp!="":
        inp=input('>>> ')
        while not check_dir(str(inp)):
            print('Please enter a valid value, check for typos or make sure the directory exists')
            inp=input('>>> ')
        if str(inp) in target_dirs:
            print('That dir is already added')
        if inp!='' and str(inp) not in target_dirs:
            target_dirs.append(str(inp))
    print()
    print('Time intervals between backups in seconds')
    print('Enter a natural non-zero number')
    inp=input('>>> ')
    valid=False
    while True:
        try:
            period_int=int(inp)
            if period_int==int(inp) and period_int>0:
                valid=True
        except:
            valid=False
        if valid==True:
            break
        else:
            print('Invalid value. Enter a natural non-zero number')
            inp=input('>>> ')
    print()
    print('Amount of backup entries to keep')
    print('Enter a natural non-zero number')
    inp=input('>>> ')
    valid=False
    while True:
        try:
            entries_int=int(inp)
            if entries_int==int(inp) and entries_int>0:
                valid=True
        except:
            valid=False
        if valid==True:
            break
        else:
            print('Invalid value. Enter a natural non-zero number')
            inp=input('>>> ')
    #insert json magic here
    print('Done! Changes were applied. Restart the tool to take effect')
def check_integrity():
    print('Running integrity check...')
    if check_dir('~/silly-software/'):
        if check_dir('~/silly-software/chainsaw-backup'):
            if check_file('~/silly-software/chainsaw-backup/config.json'): #checks if json config file exists
                print('All files intact')   #all files present
                config=open(expand_path('~/silly-software/chainsaw-backup/config.json'))
            else:
                system('touch silly-software/chainsaw-backup/config.json') #creates json config
                configure() #calls for manual configure since the json file was missing
        else:
            system('mkdir -p silly-software/chainsaw-backup/')                 #creates program folder
            system('touch silly-software/chainsaw-backup/config.json')      #creates json config
            configure() #calls for manual configure since the json file was missing
    else:                               #creates general folder (avoid cluttering of ~/home)
        system('mkdir -p silly-software/chainsaw-backup/')                     #creates program folder
        system('touch silly-software/chainsaw-backup/config.json')          #creates json config
        configure() #calls for manual configure since the json file was missing
#start up routine
check_integrity()
print('Welcome,',(str(home).replace('/','')).replace('home','')+'!')
#mainloop
while True:
    #so basically this thing is supposed to be a never-ending loop taking your input to control it
    #you use codewords to call functions
    #aaand it is precisely what it sounds like
    #also because of this I had to make a separate background process to handle the backups themselves
    inp=(input(">>> "))
    if inp=='help':
        help()
    if inp=='configure':
        configure()