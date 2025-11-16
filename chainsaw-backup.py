#declare
import datetime
import os
from os import system
from os import getcwd 
import sys
import subprocess
from time import sleep
from pathlib import Path
import json
import shutil
#define
inp=''
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
    if arg=='start':
        print('(!) Backup daemon started now at ', end='')
        x = datetime.datetime.now()
        print(x.strftime("%c"))
        print('!!! ----PLEASE READ CAREFULLY THE FOLLOWING---- !!!')
        print('(!) First backup is going to be created in 60 seconds.')
        print('(!) Please make sure backup storing folder is empty every time before running')
        print('(!) Insert Ctrl+C or Ctrl+D to stop doing backups immediately. All pereviously made backups will be kept')
        print('(!) Terminating at exactly the time a backup is made may create a race condition with big files. Handle risks on slower systems accordingly')
        print('(!) It is adviced you review your backup settings before proceeding, use show_config ')
        print('(i) You will get a notification each time a backup is made')
        print('(i) Input is unavailable while backup service is running')
        #!!!!!! ACTUAL BACKUP DAEMON STARTS HERE!!
        config=open(expand_path('~/silly-software/chainsaw-backup/config.json'), 'r')
        config_imported=json.load(config)
        backup_dir=config_imported.get('backup_dir')
        target_dirs=config_imported.get('target_dirs')
        entries_int=config_imported.get('entries_int')
        period_int=config_imported.get('period_int')
        sleep(60)
        while True:
            backup_dir=config_imported.get('backup_dir')
            x=str(datetime.datetime.now()).replace(' ','_')
            print('Now copying...')
            prompt=str('mkdir -p '+expand_path(backup_dir)+'backup-'+str(x))
            backup_dir=backup_dir+'/backup-'+str(x)
            try:
                system(prompt)
            except:
                print('Fatal error while copying: failed to create a target directory')
            
            for target in target_dirs:
                prompt=str('cp -r '+expand_path(target)+' '+backup_dir).replace('//','/')
                try:
                    system(prompt)
                except:
                    print("(!!) ERROR while copying",expand_path(target))
                    print("Promt was: '"+prompt+"'")
            print('Created backup:',x)
            rm_oldest(config_imported.get('backup_dir'))
            sleep(period_int)
def check_folders(): #dumped for now, realized ~cp creates the dirs anyway bruh
    legit=True
    config=open(expand_path('~/silly-software/chainsaw-backup/config.json'), 'r')
    config_imported=json.load(config)
    backup_dir=config_imported.get('backup_dir')
    target_dirs=config_imported.get('target_dirs')
    entries_int=config_imported.get('entries_int')
    period_int=config_imported.get('period_int')
    print('Checking directories...')
    print('Backup directory:')
    if check_dir(backup_dir):
        print(expand_path(backup_dir), '-- is a directory')
    else:
        print(expand_path(backup_dir), '-- is a directory')
        legit=False
    for element in target_dirs:
        check_dir(target_dirs)
def show_config(): #perfect parser, reuse in daemon!
    config=open(expand_path('~/silly-software/chainsaw-backup/config.json'), 'r')
    config_imported=json.load(config)
    backup_dir=config_imported.get('backup_dir')
    target_dirs=config_imported.get('target_dirs')
    entries_int=config_imported.get('entries_int')
    period_int=config_imported.get('period_int')
    print('1. Backup containing folder:')
    print('','',backup_dir)
    print('2. Directories to backup:')
    print('','',str(len(target_dirs))+',', target_dirs)
    print("3. Time interval between backups:")
    print('','',"Every",period_int//3600,"hour(s)",period_int%3600//60,"minute(s)",period_int%3600%60,"second(s)")
    print("4. Backup entries to keep:")
    print('','',entries_int, "entries")
    print()
def parse_json(silent):
    config=open(expand_path('~/silly-software/chainsaw-backup/config.json'), 'r')
    config_imported=json.load(config)
    backup_dir=config_imported.get('backup_dir')
    target_dirs=config_imported.get('target_dirs')
    entries_int=config_imported.get('entries_int')
    period_int=config_imported.get('period_int')
    if not silent: print(config_imported)
def kill():                 #immediately terminate the program
    #check if daemon currently running
    sys.exit('Exit...') 
def help():                 #dislpay help information
    print('---chainsaw-backup help---')
    print('Commands:\n')
    print('configure       -- reconfigure backup options')
    print('check_integrity -- verify integrity of configuration files')
    print('show_config     -- parse config and display current values')
    #print('check_folders   -- verify the existence of folders before running')
    print('\nAdvanced:\n')
    print('parse_json      -- parse and print out Raw Data in config.json')
    print('\nDebug:           (!)For development and testing. Use at your own risk\n')
    print("d_rem_oldest    -- calls rm_oldest() using the current directory configuration as argument by default. Note that it doesn't override entries_int argument in config")
    print('d_easter_egg    -- ???')
    print('\nOther:\n')
    print('disclaimer      -- prints out boring legal stuff')
    print('credits         -- prints out info about creators')
def output(string):         #check output for shell command
    return(str(subprocess.check_output(string, shell=True, text=True)))
def check_dir(directory):
    if '~/'==directory:
        return False
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
        config=open(expand_path('~/silly-software/chainsaw-backup/config.json'), 'w+')
    except:
        com='touch '+expand_path('~/silly-software/chainsaw-backup/config.json')
        system(com)
        config=open(expand_path('~/silly-software/chainsaw-backup/config.json'), 'w+')
    print('     ---Configuration---     ')
    print('1. Enter path to directory containing backups')
    print('e.g. ~/folder1/folder2/')
    inp=input('~/')
    inp='~/'+inp
    while not check_dir(str(inp)) or inp=='~/':
        temp_dir=inp
        print('Directory not found')
        print('Enter y to attempt to create the folder or anything else to try again')
        print("Please note that you can't use ~/")
        inp=input('>>> ')
        if inp=='y': #I could make it .lower() the input, but thats another exception to handle.
            try:                        #pointless overcomplication. Same applies to all subsequent y/n choices
                com='mkdir -p '+expand_path(str(temp_dir))
                system(com)
                if check_dir(temp_dir):
                    print("Created:",expand_path(temp_dir))
                    break
                else:
                    print("An unknown error has occured, failed to create a directory. You normally shouldn't be able to see this message")
            except:
                print('Bash has returned an exception while creating a directory; please enter a valid value!')
        else:
            inp=input('~/')
            inp='~/'+inp
    backup_dir=str(expand_path(inp))
    print()
    print('2. Enter paths to directories to backup')
    inp=None
    target_dirs=[]
    while True:
        print('Add one or more paths, return a $ once done')
        if inp=='~/$' and len(target_dirs)>0:
            break
        inp=input('~/')
        inp='~/'+inp
        temp_dir=inp
        while not check_dir(str(inp)) and inp!='~/$' and inp!='' and inp!='$': #handles directory creation if one doesn't exist already
            temp_dir=inp
            print('Directory not found')
            print('Enter y to attempt to create the folder or anything else to try again')
            print("Please note that you can't use ~/")
            inp=input('>>> ')
            if inp=='y':
                try:
                    com='mkdir -p '+expand_path(str(temp_dir))
                    system(com)
                    if check_dir(temp_dir):
                        print("Created:",expand_path(temp_dir))
                        break
                    else:
                        print("An unknown error has occured, failed to create a directory. You normally shouldn't be able to see this message")
                except:
                    print('Bash has returned an exception while creating a directory; please enter a valid value!')
        if str(expand_path(temp_dir)) in target_dirs:
            print('That directory is already added')
        if temp_dir!='~/$' and temp_dir!='' and temp_dir!='~/' and str(temp_dir) not in target_dirs:
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
    print('4. Enter amount of backup entries to keep (once out of space oldest entry is going to be overwritten!)')
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
    if backup_dir[-1]!='/':
        backup_dir=str(backup_dir)+'/'
    for element in target_dirs:
        if element[-1]!='/':
            target_dirs[target_dirs.index(element)]=(element)+'/'
    element=''
    print("\nDoes everything look okay?")
    print('1. Backup containing folder:')
    print('','',backup_dir)
    print('2. Directories to backup:')
    print('','',str(len(target_dirs))+',', target_dirs)
    print("3. Time interval between backups:")
    print('','',"Every",period_int//3600,"hour(s)",period_int%3600//60,"minute(s)",period_int%3600%60,"second(s)")
    print("4. Backup entries to keep:")
    print('','',entries_int, "entries\nApply changes? y/n")
    inp=input('>>>')
    if inp=='y':
        print("You're all set!")
    else:
        return 0
    #insert json magic here
    config_local = {
  "backup_dir": backup_dir,
  "target_dirs": target_dirs,
  "entries_int": entries_int,
  "period_int": period_int
}
    try:
        config=open(expand_path('~/silly-software/chainsaw-backup/config.json'), 'w+')
        config.write(json.dumps(config_local))
        print("Changes were applied")
        print("type 'start' to start backups now")
    except:
        print('There was an error writing the config file, sorry!')
def check_integrity():
    print('Running integrity check...')
    if check_dir('~/silly-software/'):
        if check_dir('~/silly-software/chainsaw-backup'):
            if check_file('~/silly-software/chainsaw-backup/config.json'): #checks if json config file exists
                print('All files present')   #all files present
                config=open(expand_path('~/silly-software/chainsaw-backup/config.json'), 'r')
                try:
                    parse_json(True)
                except:
                    print('config.json is corrupt, initializing configuration routine')
                    configure()
            else:
                system('touch silly-software/chainsaw-backup/config.json') #creates json config
                print('Config file was missing, initializing configuration routine')
                configure() #calls for manual configure since the json file was missing
        else:
            system('mkdir -p silly-software/chainsaw-backup/')                 #creates program folder
            system('touch silly-software/chainsaw-backup/config.json')      #creates json config
            print('Config file was missing, initializing configuration routine')
            configure() #calls for manual configure since the json file was missing
    else:                               #creates general folder (avoid cluttering of ~/home)
        system('mkdir -p silly-software/chainsaw-backup/')                     #creates program folder
        system('touch silly-software/chainsaw-backup/config.json')          #creates json config
        print('Config file was missing, initializing configuration routine')
        configure() #calls for manual configure since the json file was missing
def rm_oldest(directory):  #Some of the methods here were suggested by perplexity and stack overflow
    config=open(expand_path('~/silly-software/chainsaw-backup/config.json'), 'r')
    config_imported=json.load(config)
    backup_dir=config_imported.get('backup_dir')
    target_dirs=config_imported.get('target_dirs')
    entries_int=config_imported.get('entries_int')
    period_int=config_imported.get('period_int')

    dir_path = Path(backup_dir)       #I better be honest I hadn't known about these. All better than inefficient lists and 'ls -a' parsing **** I was planning to create initially
                               #THOUGH lower your forks and torches I built and double-checked everything. AI's code would be botched anyway
    subdirs = [d for d in dir_path.iterdir() if d.is_dir()]
    if len(subdirs)<=entries_int:
        return
    if not subdirs:
        print("No subdirectories found. Where did you take all the backups? What is going on?")
        return
    oldest = min(subdirs, key=lambda x: x.stat().st_mtime)
    print(f"Deleting deprecated backup files: {oldest}")
    try:
        shutil.rmtree(oldest)
    except OSError as e:
        print(f"Error deleting {oldest}: {e}") #printfs are beautiful. I should use these more
def easteregg():
    print('⠀⢸⠂⠀⠀⠀⠘⣧⠀⠀⣟⠛⠲⢤⡀⠀⠀⣰⠏⠀⠀⠀⠀⠀⢹⡀\n⠀⡿⠀⠀⠀⠀⠀⠈⢷⡀⢻⡀⠀⠀⠙⢦⣰⠏⠀⠀⠀⠀⠀⠀⢸⠀\n⠀⡇⠀⠀⠀⠀⠀⠀⢀⣻⠞⠛⠀⠀⠀⠀⠻⠀⠀⠀⠀⠀⠀⠀⢸⠀\n⠀⡇⠀⠀⠀⠀⠀⠀⠛⠓⠒⠓⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀\n⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠀\n⠀⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⠀⠀⢀⡟⠀\n⠀⠘⣇⠀⠘⣿⠋⢹⠛⣿⡇⠀⠀⠀⠀⣿⣿⡇⠀⢳⠉⠀⣠⡾⠁⠀\n⣦⣤⣽⣆⢀⡇⠀⢸⡇⣾⡇⠀⠀⠀⠀⣿⣿⡷⠀⢸⡇⠐⠛⠛⣿⠀\n⠹⣦⠀⠀⠸⡇⠀⠸⣿⡿⠁⢀⡀⠀⠀⠿⠿⠃⠀⢸⠇⠀⢀⡾⠁⠀\n⠀⠈⡿⢠⢶⣡⡄⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⣴⣧⠆⠀⢻⡄⠀⠀\n⠀⢸⠃⠀⠘⠉⠀⠀⠀⠠⣄⡴⠲⠶⠴⠃⠀⠀⠀⠉⡀⠀⠀⢻⡄⠀\n⠀⠘⠒⠒⠻⢦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⠞⠛⠒⠛⠋⠁⠀\n⠀⠀⠀⠀⠀⠀⠸⣟⠓⠒⠂⠀⠀⠀⠀⠀⠈⢷⡀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠙⣦⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⣼⣃⡀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠉⣹⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡆')
    print("You like making software, don't you?")
def disclaimer():
    print("""
    chainsaw-backup.py -- Easy automatic command line backup tool for Linux-based operating systems
    Copyright (C) 2025 CatPlayer8274

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    """)
#start up routine
check_integrity()
print('Welcome,',(str(home).replace('/','')).replace('home','')+'!')

#mainloop
commands=['help','configure','exit','start','parse_json','show_config','d_easter_egg','disclaimer']
while inp!='start':
    #so basically this thing is supposed to be a never-ending loop taking your input to control it
    #you use codewords to call functions
    #aaand it is precisely what it sounds like
    #also because of this -- oopsie oopsie never mind i fogor what was supposed to be here ^.^
    inp=(input(">>> "))
    if inp=='help':
        help()
    if inp=='configure':
        configure()
    if inp=='exit':
        kill()
    if inp=='start':
        daemon('start')
    if inp=='parse_json':
        parse_json(False)
    if inp=='show_config':
        parse_json(True)
        show_config()
    if inp=='d_easter_egg':
        easteregg()
    if inp=='disclaimer':
        disclaimer()
    if inp not in commands:
        print(inp,'-- unknown command. Type help for list of all commands')