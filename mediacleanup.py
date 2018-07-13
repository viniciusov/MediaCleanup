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

import os

#-------------------------- Scan Directories --------------------------

def scandir():
    
    folders,files = 0,0
    remove_folders = []

    for dirpath, dirnames, filenames in os.walk(initialdir):

        folders += len(dirnames)
        files += len(filenames)

        #CONDITIONS TO REMOVE:
        if len(dirnames)==0:

            if len(filenames)==0:  #Se a pasta não tem diretórios E não tem arquivos sera apagada
                remove_folders.append([dirpath,0]) #Motivo 0: Pasta vazia 
                
            else: #Se existe algum arquivo arquivos

                for file in filenames:        
                    if (os.path.splitext(dirpath+'\\'+file)[1] in allowedextensions): #obs: o [1] indica que é o segundo item do tuple gerado, neste caso a extensão
                        break
                else:
                    remove_folders.append([dirpath,1]) #Motivo 1: Sem arquivo de vídeo                                       

    print('\nScanning Directory:',initialdir)
    print('Folders:',folders)
    print('Files:',files) 

    if len(remove_folders):
        remove_folders.sort(key=lambda x: x[0]) #sort Inplace
        
        print('\nFolders to be Removed [',len(remove_folders),']:')

        thereis = 0
        for folder,reason in remove_folders:
            if reason==0:
                if not thereis:
                    print('\nEMPTY FOLDERS')
                thereis = 1
                print(folder)
        
        thereis = 0
        for folder,reason in remove_folders:
            if reason==1:
                if not thereis:
                    print('\nNO VIDEO FILES WITHIN')
                thereis = 1
                print(folder)

        confirm = input("\nDo you want to remove ALL of them? Press 'y' to confirm (WARNING: YOU CAN'T UNDO THIS OPERATION): ").lower()
        if confirm == 'y':
            print('Files removed!')
        else:
            print('Operation canceled.')
        
    else:
        print('\nNo Folders to be Removed!')

#---------------------- Main Program starts below ---------------------

print('Welcome to the MediaCleanup!\n')

while True:
    while True:
        try:
            with open('mediaextensions.txt','r') as file:
                data = file.readlines()
        except:
            print("Error when oppenning 'mediaextensions.txt'. Verify if the file is in the same folder.")
            input('Press any key to Retry:')
        else:
            allowedextensions = []
            allowedextensions = [x.strip() for x in data]
            break    

    option = input("""Choose one of the options below:
    d - Scan for empty directories or with no media files within;
    f - Scan for files with no media extensions;
    l - Create a list with all your media files, like a catalog;
    i - Serch on IMDB for media information and put into a .txt file;
    A - Run ALL above;
    h - View help;
    q - Quit.\nAnd enter the respective key: """)

    while not (option in ['d','f','l','i','A'] or option=='q'):
        option = input("Invalid Option. Please choose one of the options above or type 'q' to quit: ")

    if option=='q':
        break    

    initialdir = input('\nType the Path do you wanto to Scan (for example, /home/user):\n')
    
    while not (os.access(initialdir, os.W_OK) or initialdir=='q'):
        initialdir = input("\nInvalid Path or you don't have permission to Read it.\nType the Path again or type 'q' to quit:\n")
        
    if initialdir=='q':
        break

    if option=='d':
        scandir()

    repeat = input("\nPress 'r' to Run again or another Key to Exit: ").lower()
    if repeat!='r':
        break
    else:
        print('------------------------------------------------------------\n')
