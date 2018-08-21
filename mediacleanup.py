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

import re
import os
import glob
import datetime
import send2trash

#----------------------- Open 'expressions.txt' -----------------------

def open_expressionsfile():

    while True:
        try:
            with open('./config/expressions.txt', 'r', encoding="utf-8-sig") as file: #if running .py script
                data = file.readlines()
        except:
            try:
                with open('../config/expressions.txt', 'r', encoding="utf-8-sig") as file: #if running .exe
                    data = file.readlines()
            except:
                input("\nError when oppenning 'expressions.txt'.\nVerify if the file is inside the 'config/' folder and press any key to Retry: ")
            else:
                break
        else:
            break

    expressions_list = [] #Format: [(old,new)...]
    for line in data: #Analyze every line that don't start with '#'
        if not (line.startswith('#') or line == ''): #Avoid reading empty lines
            old, new = line.strip().strip("'").split('=')
            expressions_list.append((old, new))

    return expressions_list

#--------------------- Open 'mediaextensions.txt' ---------------------

def open_mediaextensionsfile():

    while True:
        try:
            with open('./config/mediaextensions.txt', 'r', encoding="utf-8") as file: #if running .py script
                data = file.readlines()
        except:
            try:
                with open('../config/mediaextensions.txt', 'r', encoding="utf-8") as file: #if running .exe
                    data = file.readlines()
            except:
                input("\nError when oppenning 'mediaextensions.txt'.\nVerify if the file is inside the 'config' folder and press any key to Retry: ")
            else:
                break
        else:
            break

    allowedextensions = []
    for line in data: #Analyze every line that don't start with '#'
        if not (line.startswith('#') or line == ''): #Avoid reading empty lines
            allowedextensions.append(line.strip().lower())

    return allowedextensions

#-------------------------- Scan and Rename ---------------------------

def scan_rename(expressions_list):

    folders, files = 0, 0
    rename_files = {} #Format: {'old':'new',...}
    rename_folders = {} #Format: {'old':'new',...}

    print("\nScanning '{}' for Folders and Filenames that match 'expressions.txt'...".format(initialdir))

    for dirpath, dirnames, filenames in os.walk(initialdir, topdown=False):

        folders += len(dirnames)
        files += len(filenames)

        for file in filenames:
            extension = os.path.splitext(file)[1]
            for exp_old, exp_new in expressions_list:
                if os.path.join(dirpath, file) not in rename_files.keys(): #If Path NOT in dict
                    temp_file = os.path.splitext(file)[0] #Using filename without extension
                else: #If Path ALREADY in dict
                    temp_file = os.path.splitext(os.path.basename(rename_files[os.path.join(dirpath, file)]))[0] #.basename is needed here to separate file from path
                if exp_old in temp_file:
                    temp_file = ' '.join(temp_file.replace(exp_old, exp_new).split()) #Removes extra spacing
                    temp_file = ' '.join(re.sub(r'\(\)', '', temp_file).split()) #Don't let '()' remaining in the string and removes extra spaces again
                    while temp_file.endswith('-') or temp_file.endswith('_') or temp_file.endswith('.') or temp_file.endswith(' '):
                        temp_file = temp_file[:-1]
                    if temp_file == '':
                        temp_file = 'media'    
                    rename_files[os.path.join(dirpath, file)] = os.path.join(dirpath, temp_file+extension)

        for directory in dirnames: #Only folders
            for exp_old, exp_new in expressions_list: #Compare with each expression
                if os.path.join(dirpath, directory) not in rename_folders.keys(): #If Path NOT in dict
                    temp_dir = directory
                else: #If Path ALREADY in dict
                    temp_dir = os.path.split(rename_folders[os.path.join(dirpath, directory)])[1] #Get only last DIR
                if exp_old in temp_dir: #Only directories
                    temp_dir = ' '.join(temp_dir.replace(exp_old, exp_new).split()) #Removes extra spaces
                    temp_dir = ' '.join(re.sub(r'\(\)', '', temp_dir).split()) #Don't let '()' remaining in the string and removes extra spaces again
                    while temp_dir.endswith('-') or temp_dir.endswith('_') or temp_dir.endswith('.') or temp_dir.endswith(' '):
                        temp_dir = temp_dir[:-1]
                    if temp_dir == '':
                        temp_dir = 'media'    
                    rename_folders[os.path.join(dirpath, directory)] = os.path.join(dirpath, temp_dir)

    print('Total Folders:', folders)
    print('Total Files:', files)

    if rename_files or rename_folders:
        print('\nItems to be Renamed [', len(rename_files)+len(rename_folders), ']:')

        if rename_files:
            thereis = False
            rename_files_list = [(old, new) for old, new in rename_files.items()]
            rename_files_list.sort(key=lambda x: x[0]) #sorts by 'old'
            for old, new in rename_files_list:
                if not thereis:
                    print('\nFILES TO BE RENAMED')
                thereis = True
                print('{} -> {}'.format(os.path.basename(old), os.path.basename(new)))

        if rename_folders:
            thereis = False
            rename_folders_list = [(old, new) for old, new in rename_folders.items()]
            rename_folders_list.sort(key=lambda x: x[0]) #sorts by 'old'
            for old, new in rename_folders_list:
                if not thereis:
                    print('\nFOLDERS TO BE RENAMED')
                thereis = True
                print('{} -> {}'.format(os.path.basename(old), os.path.basename(new)))

        rename_confirm = input("\nDo you want to Rename ALL of them?\nType 'y' to confirm (WARNING: YOU CAN'T UNDO THIS OPERATION): ").lower()
        if rename_confirm == 'y':
            errors = 0
            if rename_files:
                for old, new in rename_files.items():
                    try:
                        os.replace(old, new) #os.replace() was chosen because is cross-plataform
                    except:
                        print("Error when renaming file '{}'".format(old))
                        errors += 1

            if rename_folders:
                for old, new in rename_folders.items():
                    try:
                        os.replace(old, new) #os.replace() was chosen because is cross-plataform
                    except:
                        print("Error when renaming folder '{}'".format(old))
                        errors += 1

            if not errors:
                print('\n***All items renamed!***')
            else:
                print('\n***{} error(s) occurred when renaming.***'.format(errors))
        else:
            print('Operation canceled.')

    else:
        print('\nNo items to Rename.')

    if option == 'A':
        input('\n(Press ENTER to continue)')
        print('-------------------------')

#--------------------------- Scan for Dirs ----------------------------

def scan_dirs(allowedextensions):

    folders, files = 0, 0
    remove_list = [] #Format: [[path,reason],...]

    print("\nScanning '{}' for Empty Folders or with no Media Files inside...".format(initialdir))

    for dirpath, dirnames, filenames in os.walk(initialdir, topdown=False):

        folders += len(dirnames)
        files += len(filenames)

        if dirpath != initialdir: #Avoid deleting the top folder even if it is empty
            if not dirnames:
                if not filenames:  #If don't have any directory inside AND don't have any file
                    remove_list.append([dirpath, 0]) #Reason 0: Empty Folder
                else: #If there is files
                    for file in filenames:
                        if os.path.splitext(os.path.join(dirpath, file))[1].lower() in allowedextensions: #[1] is the second item of the generated tuple (the extension, in this case)
                            break
                    else:
                        remove_list.append([dirpath, 1]) #Reason 1: Folder with No Media Files inside

            else:
                glob_path = dirpath.replace('[', '[[]') #workaround to use 'glob' if there are brackets in folder or filenames
                if not glob.glob(glob_path+'/**/*.*', recursive=True): #If path DOESN'T have any file
                    remove_list.append([dirpath, 1]) #Reason 1: Folder with No Media Files inside

                else: #If path DOES have files
                    for file in glob.iglob(glob_path+'/**/*.*', recursive=True):
                        if os.path.splitext(file)[1] in allowedextensions:
                            break
                    else:
                        remove_list.append([dirpath, 1]) #Reason 1: Folder with No Media Files inside

    print('Total Folders:', folders)
    print('Total Files:', files)

    if remove_list:
        remove_list.sort(key=lambda x: x[0]) #sorts Inplace (First by name)
        remove_list.sort(key=lambda x: x[1]) #sorts Inplace (After sorts by Reason)

        print('\nItems to be Removed [', len(remove_list), ']:')

        thereis = False
        for path, reason in remove_list:
            if reason == 0:
                if not thereis:
                    print('\nEMPTY FOLDERS')
                thereis = True
                print(path)

        thereis = False
        for path, reason in remove_list:
            if reason == 1:
                if not thereis:
                    print('\nFOLDERS WITH NO MEDIA FILES INSIDE')
                thereis = True
                print(path)

        remove_confirm = input("\nDo you want to Remove ALL of them?\nType 'y' to confirm (WARNING: YOU CAN'T UNDO THIS OPERATION): ").lower()
        if remove_confirm == 'y':
            errors = 0
            remove_list.sort(key=lambda x: x[0], reverse=True) #/dir/subdir must be removed before /dir to avoid errors
            remove_list.sort(key=lambda x: x[1]) #First removes empty files
            for path, reason in remove_list:
                try:
                    send2trash.send2trash(path) #move items to trash
                except:
                    print("Error when removing '{}'.".format(path))
                    errors += 1
            if not errors:
                print('\n***All items removed!***')
            else:
                print('\n***{} error(s) occurred.***'.format(errors))
        else:
            print('Operation canceled.')

    else:
        print('\nNo items to Remove.')

    if option == 'A':
        input('\n(Press ENTER to continue)')
        print('-------------------------')

#-------------------------- Scan for Files ----------------------------

def scan_files(allowedextensions):

    folders, files = 0, 0
    remove_list = []

    print("\nScanning '{}' for extensions that match 'mediaextensions.txt'...".format(initialdir))

    for dirpath, dirnames, filenames in os.walk(initialdir):

        folders += len(dirnames)
        files += len(filenames)

        for file in filenames:
            if not ((os.path.splitext(os.path.join(dirpath, file))[1].lower() in allowedextensions+['.srt', '.sub']) or file == 'mediacatalog.txt'): #'.lower' avoids it remove .AVI
                remove_list.append(os.path.join(dirpath, file)) #Reason 2: File with No Media Extension

    print('Total Folders:', folders)
    print('Total Files:', files)

    if remove_list:
        print('\nItems to be Removed [', len(remove_list), ']:')

        thereis = False
        for path in remove_list:
            if not thereis:
                print("\nFILE EXTENSIONS DOESN'T MATCH")
            thereis = True
            print(path)

        remove_confirm = input("\nDo you want to Remove ALL of them?\nType 'y' to confirm (WARNING: YOU CAN'T UNDO THIS OPERATION): ").lower()
        if remove_confirm == 'y':
            errors = 0
            for file in remove_list:
                try:
                    os.remove(file)
                except:
                    print("Error when removing '{}'.".format(file))
                    errors += 1
            if not errors:
                print('\n***All items removed!***')
            else:
                print('\n***{} error(s) occurred.***'.format(errors))
        else:
            print('Operation canceled.')

    else:
        print('\nNo items to Remove.')

    if option == 'A':
        input('\n(Press ENTER to continue)')
        print('-------------------------')

#--------------------------- Scan and List ----------------------------

def scan_list(allowedextensions):

    folders, files = 0, 0
    catalog = []

    print("\nScanning '{}' for Media Files...".format(initialdir))

    for dirpath, dirnames, filenames in os.walk(initialdir):

        folders += len(dirnames)
        files += len(filenames)

        for file in filenames:
            if os.path.splitext(os.path.join(dirpath, file))[1].lower() in allowedextensions:
                catalog.append(os.path.join(os.path.basename(dirpath), file))

    print('Total Folders:', folders)
    print('Total Files:', files)

    if catalog:
        print('\nYour Media Files [', len(catalog), ']:\n')

        catalog.sort()
        for file in catalog:
            print(file)

        write_confirm = input("\nDo you want save the above list as a '.txt' file? Type 'y' to proceed: ").lower()
        if write_confirm == 'y':
            write_path = input("\nType the Path where do you want to save or press ENTER to use the same Path:\n(Current Path: {})\n".format(initialdir))

            while not (os.access(write_path, os.W_OK) or write_path == ''):
                write_path = input("\nInvalid Path. Type the Path again or press ENTER to use the same directory:\n")

            if write_path == '':
                write_path = initialdir
            try:
                f = open(write_path+"/mediacatalog.txt", "w+", encoding="utf-8")
                f.write("Media files in '{}':\n\n".format(initialdir))

                for number, file in enumerate(catalog, 1): #counting starts with 1
                    f.write("("+str(number)+") "+str(file)+"\n")

                now = datetime.datetime.now()
                f.write("\n---------------------------------------------\nCreated at {} with MediaCleanup.\n(https://github.com/viniciusov/mediacleanup)".format(now.strftime("%Y-%m-%d %H:%M")))
                f.close()
            except:
                print("Error when creating 'mediacatalog.txt'.\n(Verify if you have permission to write in {}).".format(write_path))
            else:
                print("***'mediacatalog.txt' successfully created at '{}'.***".format(write_path))

        else:
            print('Operation canceled.')

    else:
        print('\nNo Media Files to show.')

#-------------------------- Show help/about ---------------------------

def show_help():
    clear_screen()
    print("""MediaCleanup is a free tool to cleanup your media files and folders.
It will scan a provided path for folders and media files, can find specific expressions and extensions, allowing to rename or remove them.

Help:
To start with it, run MediaCleanup, choose one from main options, type the respective key and press Enter.
'c' - Will scan a specific path for folders and filenames that match expressions inside the file 'config/expressions.txt'.
      If any file/folder match, the software will list it to rename with the desired expression in 'config/expressions.txt'.
      After the listing process, the user will be asked to confirm the files and folders renaming.
'd' - Will scan a specific path for folders that are empty or don't have any file with media extensions.
      The software will use all extensions inside 'config/mediaextensions.txt' to compare and determine if a file is a media file or not.
      After the listing process, the user will be asked to confirm the removing.
'f' - Will scan a specific path for files that don't have media extensions.
      Like the 'd' option, it will use all extensions inside 'config/mediaextensions.txt' to compare against the files extensions.
      If files extensions don't match, the software will list all and the user will be asked to remove them.
'l' - MediaCleanup will list all your media files (according 'config/mediaextensions.txt') and show them.
      The user will be asked to save the list as a .txt file (mediacatalog.txt) and the software will ask for destination path.
      If user type 'ENTER' to the destination path, the .txt file will be crated in the same scanned path.
'A' - Will run ALL options above. For best cleaning, it will run in the following sequence: f->d->c->l.
'h' - Show up all this information.
'q' - The software will stop and quit.
After choosing the desired option, MediaCleanup will ask for the path to be scanned.

About:
* Created by Vinícius Orsi Valente (2018)
* Licensed under GPLv3
* Version 1.4b (Beta)

MediaCleanup is freely available at 'https://github.com/viniciusov/mediacleanup/'.
Check it out to see more detailed information or download the newest versions.\n""")
    input("(Press ENTER to Quit help/about and return)")

#---------------------------- Clear Screen ----------------------------

def clear_screen():
    if os.name == 'nt':
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
    A - Run ALL options above (f->d->c->l);
    h - View help/about;
    q - Quit.\nAnd enter the respective key: """)

    while not (option in ['c', 'd', 'f', 'l', 'A', 'h', 'q']):
        option = input("Invalid Option. Please choose one of the options above or type 'q' to quit: ")

    if option == 'h':
        show_help()
        continue

    if option == 'q':
        break

    if os.name == 'nt':
        initialdir = input('\nType the Path do you wanto to Scan (for example, C:\\Users\\<user>\\Videos):\n')
    else:
        initialdir = input('\nType the Path do you wanto to Scan (for example, /home/<user>/Videos):\n')

    while not (os.access(initialdir, os.W_OK) or initialdir == 'q'):
        initialdir = input("\nInvalid Path or you don't have permission to Read it.\nType the Path again or type 'q' to quit:\n")

    if initialdir == 'q':
        break
    else:
        print('-'*len(initialdir))

        if option in ['f', 'A']:
            scan_files(open_mediaextensionsfile())

        if option in ['d', 'A']:
            scan_dirs(open_mediaextensionsfile())

        if option in ['c', 'A']:
            scan_rename(open_expressionsfile())

        if option in ['l', 'A']:
            scan_list(open_mediaextensionsfile())

    print('-'*45)
    repeat = input("\nType 'r' to Run again or press ENTER to Exit: ").lower()
    if repeat == 'r':
        continue
    else:
        break
