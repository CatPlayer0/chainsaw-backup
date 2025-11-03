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
def daemon(arg):
    if arg=='stop':
        print('(!) Backup daemon stopped')
    if arg=='start':
        print('(!) Backup daemon started')
def kill():                 #immediately terminate the program
    #check if daemon currently running
    sys.exit('Exit configurator...') 
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
    try:
        return(os.path.expanduser(path))
    except:
        print('Caught exception: invalid directory path')
        return('')
def configure():            #configure manually
    try:
        file=open(expand_path('~/silly-software/chainsaw-backup/config.json'), 'w+')
    except:
        com='touch '+expand_path('~/silly-software/chainsaw-backup/config.json')
        system(com)
        file=open(expand_path('~/silly-software/chainsaw-backup/config.json'), 'w+')
    print('     ---Configuration---     ')
    print('1. Enter path to directory containing backups')
    print('e.g. ~/folder1/folder2/')
    inp=input('>>> ')
    while not check_dir(str(inp)):
        temp_dir=inp
        print('Please enter a valid value, check for typos or make sure the directory exists')
        print('Enter y to override and attempt to create the folder')
        inp=input('>>> ')
        if inp=='y':
            try:
                com='mkdir -p '+expand_path(str(temp_dir))
                system(com)
                if check_dir(temp_dir):
                    print("Created:",expand_path(temp_dir))
                    break
                else:
                    print('An unknown error has occured, failed to create a directory. Please try again')
            except:
                print('Bash has returned an exception while creating a directory; please enter a valid value!')
    backup_dir=str(inp)
    print()
    print('2. Enter paths to directories to backup')
    inp=None
    target_dirs=[]
    while inp!='':
        print('Add one or more paths, return an empty line once done')
        inp=input('>>> ')
        temp_dir=inp
        while not check_dir(str(inp)) and inp!='': #handles directory creation if one doesn't exist already
            temp_dir=inp
            print('Please enter a valid value, check for typos or make sure the directory exists')
            print('Enter y to override and attempt to create the folder')
            inp=input('>>> ')
            if inp=='y':
                try:
                    com='mkdir -p '+expand_path(str(temp_dir))
                    system(com)
                    if check_dir(temp_dir):
                        print("Created:",expand_path(temp_dir))
                        break
                    else:
                        print('An unknown error has occured, failed to create a directory. Please try again')
                except:
                    print('Bash has returned an exception while creating a directory; please enter a valid value!')
        if str(expand_path(temp_dir)) in target_dirs:
            print('That directory is already added')
        if temp_dir!='' and str(temp_dir) not in target_dirs:
            target_dirs.append(str(expand_path(temp_dir)))
    print()
    print('3. Enter time intervals between backups in seconds')
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
    print('4. Enter amount of backup entries to keep (once out of space oldest entry is going to be overwritten)')
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
    print("\nReview your choices:")
    print('1. Backup containing folder:')
    print(backup_dir)
    print('2. Directories to backup:')
    print(str(len(target_dirs))+',', target_dirs)
    print("3. Time interval between backups:")
    print("Every",period_int//3600,"hour(s)",period_int%3600//60,"minute(s)",period_int%3600%60,"second(s)")
    print("4. Backup entries to keep:")
    print(entries_int, "entries")
    print()
    #insert json magic here
    print("You're all set! Changes are applied automatically")
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
    if inp=='exit':
        kill()
    if inp=='stop':
        daemon('stop')
    if inp=='start':
        daemon('start')