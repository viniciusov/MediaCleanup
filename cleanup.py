#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

allowedextensions = []

while True:
    try:
        with open('allowedextensions.txt','r') as file:
            data = file.readlines()
    except:
        print("\nError when oppenning 'allowedextensions.txt'. Verify if the file is in the same folder.")
        input('Press any key to Retry:')
    else:
        break
            
allowedextensions = [x.strip() for x in data]
initialdir = os.getcwd()

while True:

    folders,files = 0,0
    remove_folders = []

    for dirpath, dirnames, filenames in os.walk(initialdir):
        #print('\nCurrent Path:', dirpath)
        #print('Directories:', dirnames)
        #print('Files:',filenames)

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

        confirm = input("\nDo you want to remove ALL of them? Press 'y' to confirm (WARNING: YOU CAN'T UNDO THIS OPERATION):").lower()
        if confirm == 'y':
            print('Files removed!')
        else:
            print('Operation canceled.')
        
    else:
        print('\nNo Folders to be Removed!')

    repeat = input("\nPress 'r' to Reescan or another Key to Exit:").lower()
    if repeat!='r':
        break

    
    

