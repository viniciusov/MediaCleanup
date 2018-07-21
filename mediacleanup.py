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

import os, shutil, datetime

#----------------------- Scan Directories/Files -----------------------
def scan():

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

    if option=='c' or option=='A':
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
            old, new = line.strip().split('=')
            expressions_dict.update({old:new})
          
    folders,files = 0,0
    rename_list = [] #Format: [[old,new,isdir],...]
    remove_list = [] #Format: [[path,reason,isdir],...]
    catalog = []

    for dirpath, dirnames, filenames in os.walk(initialdir):

        folders += len(dirnames)
        files += len(filenames)

        if (option=='c' or option=='A'):
            found_path = False #Using this flag to avoid reporting several times the same path
            for file in filenames:
                found_file = False #Using this flag to avoid reporting several times the same file
                for expression in expressions_dict.keys():
                    if (expression in dirpath) and not found_path:
                        rename_list.append([dirpath, dirpath.replace(expression,expressions_dict[expression]), 1])
                        found_path = True
                    if (expression in file) and not found_file: #[0] is the first item of the generated tuple (the filename, in this case)
                        rename_list.append([dirpath+os.sep+file, (dirpath+os.sep)+file.replace(expression,expressions_dict[expression]) ,0])
                        found_file = True
                    
        if (option=='d' or option=='A') and len(dirnames)==0:
            if len(filenames)==0:  #If don't have any directory within AND don't have any file
                remove_list.append([dirpath,0,1]) #Reason 0: Empty Folder 
            else: #If there is files
                for file in filenames:        
                    if (os.path.splitext(dirpath+os.sep+file)[1].lower() in allowedextensions): #[1] is the second item of the generated tuple (the extension, in this case)
                        break
                else:
                    remove_list.append([dirpath,1,1]) #Reason 1: Folder with No Video File

        if (option=='f' or option=='A'):
            for file in filenames:
                if not (os.path.splitext(dirpath+os.sep+file)[1].lower() in allowedextensions+['.srt','.sub']): #'.lower' avoids it remove the file if its extension is .AVI
                    remove_list.append([dirpath+os.sep+file,2,0]) #Reason 2: File with No Media Extension

        if (option=='l' or option=='A'):
            for file in filenames:
                if (os.path.splitext(dirpath+os.sep+file)[1].lower() in allowedextensions):
                    catalog.append(file)
                    
    print('\nScanning Directory:',initialdir)
    print('Total Folders:',folders)
    print('Total Files:',files)
    
    if len(rename_list): #Run if 'c' or 'A' are chosen
        rename_list.sort(key=lambda x: x[0]) #sorts Inplace
        print('\nFiles and Paths to be Renamed [',len(rename_list),']:')

        thereis = False
        for old,new,isdir in rename_list:
            if not thereis:
                    print('\nOLD FILE/PATH NAMES')
            thereis = True
            print(old)

        thereis = False
        for old,new,isdir in rename_list:
            if not thereis:
                    print('\nNEW FILE/PATH NAMES')
            thereis = True
            print(new)

        rename_confirm = input("\nDo you want to Rename ALL of them? Press 'y' to confirm (WARNING: YOU CAN'T UNDO THIS OPERATION): ").lower()
        if rename_confirm == 'y':
            for x in range(0,2): #isdir can be 0 or 1
                for old,new,isdir in rename_list:
                    if isdir==x: #Checks if is a dir (directories should be the last removed)
                        os.replace(old,new) #os.replace() was chosen because is cross-plataform                
            print('***Itens renamed!***')
        else:
            print('Operation canceled.')    

    elif option in ['c','A']:
        print('\nNo itens to Rename!')        

    if len(remove_list): #Run if 'd', 'f' or 'A' are chosen
        remove_list.sort(key=lambda x: x[0]) #sorts Inplace
        
        print('\nItens to be Removed [',len(remove_list),']:')

        thereis = False
        for path,reason,isdir in remove_list:
            if reason==0:
                if not thereis:
                    print('\nEMPTY FOLDERS')
                thereis = True
                print(path)
        
        thereis = False
        for path,reason,isdir in remove_list:
            if reason==1:
                if not thereis:
                    print('\nFOLDERS WITH NO VIDEO FILES WITHIN')
                thereis = True
                print(path)

        thereis = False
        for file,reason,isdir in remove_list:
            if reason==2:
                if not thereis:
                    print("\nFILE EXTENSIONS DOESN'T MATCH")
                thereis = True
                print(file)        

        remove_confirm = input("\nDo you want to Remove ALL of them? Press 'y' to confirm (WARNING: YOU CAN'T UNDO THIS OPERATION): ").lower()
        if remove_confirm == 'y':
            for x in range(0,2): #isdir can be 0 or 1
                for path,reason,isdir in remove_list:
                    if isdir==x:
                        if reason==0:
                            os.rmdir(path) #Remove only empty folders
                        elif reason==1:
                            shutil.rmtree(path) #Remove folders containing files
                        else:        
                            os.remove(path)          
            print('***Itens removed!***')
        else:
            print('Operation canceled.')
            
    elif option in ['d','f','A']:
        print('\nNo itens to Remove!')

    if len(catalog): #Run if 'l' or 'A' are chosen
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

            f= open(write_path+"/media_catalog.txt","w+", encoding="utf-8")
            f.write("Media files in '{}':\n\n".format(initialdir))
            
            for number,file in enumerate(catalog,1): #counting starts with 1
                f.write("("+str(number)+") "+str(file)+"\n")
                
            now = datetime.datetime.now()
            f.write("\nCreated at {} with MediaCleanup.\n(https://github.com/viniciusov/mediacleanup)".format(now.strftime("%Y-%m-%d %H:%M")))
            f.close()

            print("***'media_catalog.txt' successfully created!***")
        
        else:
            print('Operation canceled.')
            
    elif option in ['l','A']:
        print('\nNo Media Files to show!')
        
#---------------------- Main Program starts below ---------------------

print('Welcome to the MediaCleanup!\n')

while True:  

    option = input("""Choose one of the options below:
    c - Clean up folder and file names
    d - Scan for empty directories or with no media files within;
    f - Scan for files with no media or subtitles extensions;
    l - Create a list with all your media files, like a catalog;
    A - Run ALL above;
    h - View help/about;
    q - Quit.\nAnd enter the respective key: """)
    #Soon it will include:
    #i - Serch on IMDB for media information and put into a .txt file;

    while not (option in ['c','d','f','l','A','h','q']):
        option = input("Invalid Option. Please choose one of the options above or type 'q' to quit: ")

    if option=='q':
        break    

    initialdir = input('\nType the Path do you wanto to Scan (like /home/<user> or C:\\Users\\<user>):\n')
    
    while not (os.access(initialdir, os.W_OK) or initialdir=='q'):
        initialdir = input("\nInvalid Path or you don't have permission to Read it.\nType the Path again or type 'q' to quit:\n")
        
    if initialdir=='q':
        break

    if option in ['c','d','f','l','A']:
        scan()

    repeat = input("\nPress 'r' to Run again or another key to Exit: ").lower()
    if repeat=='r':
        print('------------------------------------------------\n')
    else:
        break
