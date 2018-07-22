#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------
# Copyright (C) 2018, Vinícius Orsi Valente (viniciusov@hotmail.com)
#
# This file is part of MediaCleanup.
#
# Mediacleanup is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Mediacleanup is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Mediacleanup. If not, see <https://www.gnu.org/licenses/>.
#----------------------------------------------------------------------

import os, glob, shutil, datetime

#----------------------- Open 'expressions.txt' -----------------------

def open_expressionsfile():
    
    while True:
            try:
                with open('./config/expressions.txt','r') as file: #if running .py script
                    data = file.readlines()
            except:
                try:
                    with open('../config/expressions.txt','r') as file: #if running .exe
                        data = file.readlines()
                except:     
                    input("\nError when oppenning 'expressions.txt'.\nVerify if the file is inside the 'config/' folder and press any key to Retry: ")
                else:
                    break
            else:
                break
            
    expressions_dict = {}
    for line in data: #Analyze every line that don't start with '#'
        if not line.startswith('#'):
            old, new = line.strip().strip("'").split('=')
            expressions_dict.update({old:new})
    return expressions_dict

#--------------------- Open 'mediaextensions.txt' ---------------------

def open_mediaextensionsfile():
    
    while True:
        try:
            with open('./config/mediaextensions.txt','r') as file: #if running .py script
                data = file.readlines()
        except:
            try:
                with open('../config/mediaextensions.txt','r') as file: #if running .exe
                    data = file.readlines()
            except:     
                input("\nError when oppenning 'mediaextensions.txt'.\nVerify if the file is inside the 'config' folder and press any key to Retry: ")
            else:
                break
        else:
            break
        
    allowedextensions = []
    for line in data: #Analyze every line that don't start with '#'
        if not line.startswith('#'):
            allowedextensions.append(line.strip().lower())

    return allowedextensions        

#-------------------------- Scan and Rename ---------------------------

def scan_rename(expressions_dict):
          
    folders,files = 0,0
    rename_files = {} #Format: {'old':'new',...}
    rename_folders = {} #Format: {'old':'new',...}
    rename_dic = {}

    for dirpath, dirnames, filenames in os.walk(initialdir, topdown=False):

        folders += len(dirnames)
        files += len(filenames)

        for file in filenames: #For each file   
            for expression in expressions_dict.keys(): #Compare with each expression
                if expression in os.path.basename(os.path.join(dirpath,file)): #Only filename, without extension
                    if os.path.join(dirpath,file) not in rename_files.keys(): #If Path NOT in dict  
                        temp_file = os.path.basename(os.path.join(dirpath,file))
                        temp_extension = os.path.splitext(os.path.join(dirpath,file))[1]
                    else: #If Path ALREADY in dict   
                        temp_file = os.path.basename(rename_files[os.path.join(dirpath,file)])
                        temp_extension = os.path.splitext(rename_files[os.path.join(dirpath,file)])[1]
                    temp_file = temp_file.replace(expression,expressions_dict[expression])      
                    rename_files[os.path.join(dirpath,file)]=os.path.join(dirpath,temp_file+temp_extension)

        for directory in dirnames: #Only folders
            for expression in expressions_dict.keys(): #Compare with each expression
                if expression in os.path.join(dirpath,directory): #Only filename, without extension
                    if os.path.join(dirpath,directory) not in rename_folders.keys(): #If Path NOT in dict  
                        temp_path = os.path.join(dirpath,directory)
                    else: #If Path ALREADY in dict   
                        temp_path = rename_folders[os.path.join(dirpath,directory)]
                    temp_path = temp_path.replace(expression,expressions_dict[expression])    
                    rename_folders[os.path.join(dirpath,directory)]=temp_path
                                        
    print("\nScanning '{}' for Folders and Filenames that match 'expressions.txt'...".format(initialdir))
    print('Total Folders:',folders)
    print('Total Files:',files)
    
    rename_dict = rename_files.copy() #Organize dicts to show files first
    rename_dict.update(rename_folders)

    if len(rename_dict):
        print('\nFiles and Paths to be Renamed [',len(rename_dict),']:')

        thereis = False
        for old in rename_dict.keys():
            if not thereis:
                    print('\nOLD NAMES')
            thereis = True
            print(old)

        thereis = False
        for new in rename_dict.values():
            if not thereis:
                    print('\nNEW NAMES')
            thereis = True
            print(new)

        rename_confirm = input("\nDo you want to Rename ALL of them? Press 'y' to confirm (WARNING: YOU CAN'T UNDO THIS OPERATION): ").lower()
        if rename_confirm == 'y':
            errors = 0
            for old,new in rename_dict.items():
                try:
                    os.replace(old,new) #os.replace() was chosen because is cross-plataform
                except:
                    print("Error when renaming '{}'./nVerify if you have Write Permission to rename it.".format(old))
                    errors += 1
            else:
                if not errors:
                    print('***All items renamed!***')
                else:
                    print('{} error(s) occurred'.format(errors))
        else:
            print('Operation canceled.')    

    else:
        print('\nNo items to Rename!')        

#--------------------------- Scan for Dirs ----------------------------

def scan_dirs(allowedextensions):
          
    folders,files = 0,0
    remove_list = [] #Format: [[path,reason],...]

    for dirpath, dirnames, filenames in os.walk(initialdir, topdown=False):

        folders += len(dirnames)
        files += len(filenames)

        if len(dirnames)==0:
            if len(filenames)==0:  #If don't have any directory inside AND don't have any file
                remove_list.append([dirpath,0]) #Reason 0: Empty Folder
            else: #If there is files
                for file in filenames:        
                    if (os.path.splitext(os.path.join(dirpath,file))[1].lower() in allowedextensions): #[1] is the second item of the generated tuple (the extension, in this case)
                        break
                else:
                    remove_list.append([dirpath,1]) #Reason 1: Folder with No Video Files inside

        else:
            if not len(glob.glob(dirpath+'/**/*.*', recursive=True)): #If path DOESN'T have any file
                remove_list.append([dirpath,0]) #Reason 0: Empty Folder

            else: #If path DOES have files
                for file in glob.iglob(dirpath+'/**/*.*', recursive=True):
                    if ('.'+file.split('.')[1]) in allowedextensions:
                        break
                else:
                    remove_list.append([dirpath,1]) #Reason 1: Folder with No Video Files inside
    
    print("\nScanning '{}' for Empty Folders or with no Media Files inside...".format(initialdir))
    print('Total Folders:',folders)
    print('Total Files:',files)
    
    if len(remove_list):
        remove_list.sort(key=lambda x: x[1]) #sorts Inplace
        
        print('\nItems to be Removed [',len(remove_list),']:')

        thereis = False
        for path,reason in remove_list:
            if reason==0:
                if not thereis:
                    print('\nEMPTY FOLDERS')
                thereis = True
                print(path)
        
        thereis = False
        for path,reason, in remove_list:
            if reason==1:
                if not thereis:
                    print('\nFOLDERS WITH NO VIDEO FILES INSIDE')
                thereis = True
                print(path)    

        remove_confirm = input("\nDo you want to Remove ALL of them? Press 'y' to confirm (WARNING: YOU CAN'T UNDO THIS OPERATION): ").lower()
        if remove_confirm == 'y':
            errors = 0
            for path,reason in remove_list:
                try:
                    if reason==0:
                        os.rmdir(path) #Remove only empty folders                   
                    else:
                        shutil.rmtree(path) #Remove folders containing files              
                except:
                    print("Error when removing '{}'./nVerify if you have Write Permission or if it isn't Read-Only.".format(path))
                    errors += 1
            else:
                if not errors:
                    print('***All items removed!***')
                else:
                    print('{} error(s) occurred'.format(errors))
        else:
            print('Operation canceled.')
    else:
        print('\nNo items to Remove!')

#-------------------------- Scan for Files ----------------------------

def scan_files(allowedextensions):

    folders,files = 0,0
    remove_list = []
    
    for dirpath, dirnames, filenames in os.walk(initialdir):

        folders += len(dirnames)
        files += len(filenames)

        for file in filenames:
                if not (os.path.splitext(os.path.join(dirpath,file))[1].lower() in allowedextensions+['.srt','.sub']): #'.lower' avoids it remove the file if its extension is .AVI
                    remove_list.append(os.path.join(dirpath,file)) #Reason 2: File with No Media Extension
                    
    print("\nScanning '{}' for extensions that match 'allowedextensions.txt'...".format(initialdir))
    print('Total Folders:',folders)
    print('Total Files:',files)

    thereis = False
    for path in remove_list:
        if not thereis:
            print("\nFILE EXTENSIONS DOESN'T MATCH")
        thereis = True
        print(path)

    if len(remove_list):
        remove_confirm = input("\nDo you want to Remove ALL of them? Press 'y' to confirm (WARNING: YOU CAN'T UNDO THIS OPERATION): ").lower()
        if remove_confirm == 'y':
            errors = 0            
            for file in remove_list:
                try:
                    os.remove(file)
                except:
                    print("Error when removing '{}'./nVerify if you have Write Permission or if it isn't Read-Only.".format(file))
                    errors += 1
            else:
                if not errors:
                    print('***All items removed!***')
                else:
                    print('{} error(s) occurred'.format(errors))
        else:
            print('Operation canceled.')
    else:
        print('\nNo items to Remove!')

#--------------------------- Scan and List ----------------------------

def scan_list(allowedextensions): 

    folders,files = 0,0
    catalog = []

    for dirpath, dirnames, filenames in os.walk(initialdir):

        folders += len(dirnames)
        files += len(filenames)

        for file in filenames:
            if (os.path.splitext(os.path.join(dirpath,file))[1].lower() in allowedextensions):
                catalog.append(file)
                    
    print("\nScanning '{}' for Media Files...".format(initialdir))
    print('Total Folders:',folders)
    print('Total Files:',files)
        
    if len(catalog):
        print('\nYour Media Files [',len(catalog),']:\n')
        
        catalog.sort()
        for file in catalog:
            print(file)

        write_confirm = input("\nDo you want save the above list as a '.txt' file? Press 'y' to proceed: ").lower()
        if write_confirm == 'y':
            write_path = input("\nType the Path where do you want to to save or 's' to use the same directory:\n")

            while not (os.access(write_path, os.W_OK) or write_path=='s'):
                write_path = input("\nInvalid Path. Type the Path again:\n")

            if write_path=='s':
                write_path=initialdir

            try:
                f= open(write_path+"/media_catalog.txt","w+", encoding="utf-8")
                f.write("Media files in '{}':\n\n".format(initialdir))
                
                for number,file in enumerate(catalog,1): #counting starts with 1
                    f.write("("+str(number)+") "+str(file)+"\n")
                    
                now = datetime.datetime.now()
                f.write("\nCreated at {} with MediaCleanup.\n(https://github.com/viniciusov/mediacleanup)".format(now.strftime("%Y-%m-%d %H:%M")))
                f.close()
            except:    
                print("Error when creating 'media_catalog.txt'.\nVerify if you have permission to write in {}".format(write_path))
            else:
                print("***'media_catalog.txt' successfully created at '{}'.***".format(write_path))
        
        else:
            print('Operation canceled.')
            
    else:
        print('\nNo Media Files to show!')

#-------------------------- Show help/about ---------------------------

def show_help():
    clear_screen() 
    print("""MediaCleanup is a free tool to cleanup your media files and folders.
It will scan the provided path to media files and can rename files with specific expressions or remove unwanted files.

Help:
To start with it, run MediaCleanup, choose one from main options, type the respective key and press Enter.
'c' - Will scan a specific path for files and folders that match expressions inside the file 'config/expressions.txt'.
      If any file/folder match, the software will list it to rename with the desired expression in 'config/expressions.txt'.
      After the listing process, the user will be asked to confirm the files/folders renaming.
'd' - Will scan a specific path for folders that are empty or don't have any file with media extensions.
      The software will use all extensions inside 'config/allowedextensions.txt' to compare and determine if a file is a media file or not.
      After the listing process, the user will be asked to confirm the folders removing.
'f' - Will scan a specific path for files that don't have media extensions.
      Like the 'd' option, it will use all extensions inside 'config/allowedextensions.txt' to compare against the files extensions.
      If files extensions don't match, the software will list all and the user will be asked to remove them.
'l' - MediaCleanup will list all your media files (according 'config/allowedextensions.txt') and show them.
      The user will be asked to save the list as a .txt file (media_catalog.txt) and the software will ask for destination path.
      If user type 's' to the destination path, the .txt file will be crated in the same scanned path.
'h' - Show up all this information.
'q' - If user type 'q' and press Enter, the software will stop and quit.
After choosing the desired option, MediaCleanup will ask for the path to be scanned.

About:
- Created by Vinícius Orsi Valente (2018)
- Licensed under GPLv3
- Version 0.6 (Beta)

MediaCleanup is freely avaliable at https://github.com/viniciusov/mediacleanup/.
Check it out to see more detailed information or download the newest versions.\n""")
    key = input("Press any key to Quit help/about and return: ")

#---------------------------- Clear Screen ----------------------------    

def clear_screen():
    if os.name =='nt':
        os.system('cls')
    else:
        os.system('clear')   
        
#---------------------- Main Program starts below ---------------------

while True:
    clear_screen()
    print('Welcome to the MediaCleanup!')
    option = input("""\nChoose one of the options below:
    c - Clean up folder and file names;
    d - Scan for empty directories or with no media files inside;
    f - Scan for files with no media or subtitles extensions;
    l - Create a list with all your media files, like a catalog;
    A - Run ALL above;
    h - View help/about;
    q - Quit.\nAnd enter the respective key: """)
    #Soon it will include:
    #i - Serch on IMDB for media information and put into a .txt file;

    while not (option in ['c','d','f','l','A','h','q']):
        option = input("Invalid Option. Please choose one of the options above or type 'q' to quit: ")

    if option=='h':
        show_help()
        continue    

    if option=='q':
        break    

    if os.name=='nt':
        initialdir = input('\nType the Path do you wanto to Scan (e.g. C:\\Users\\<user>\\Videos):\n')
    else:
        initialdir = input('\nType the Path do you wanto to Scan (e.g. /home/<user>/Videos):\n') 
    
    while not (os.access(initialdir, os.W_OK) or initialdir=='q'):
        initialdir = input("\nInvalid Path or you don't have permission to Read it.\nType the Path again or type 'q' to quit:\n")
        
    if initialdir=='q':
        break

    if option in ['c','A']:
        scan_rename(open_expressionsfile())

    if option in ['d','A']:
        scan_dirs(open_mediaextensionsfile())

    if option in ['f','A']:
        scan_files(open_mediaextensionsfile())    

    if option in ['l','A']:
        scan_list(open_mediaextensionsfile())

    repeat = input("\nPress 'r' to Run again or another key to Exit: ").lower()
    if repeat=='r':
        continue
    else:
        break
