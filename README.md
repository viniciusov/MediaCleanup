# MediaCleanup

## The problem
Initially I started to code this program to help me with a issue.
I download a lot of media files and organize them in folders with these files, subtitles, audio, images, etc., but I realize that 
a lot of those folders contain just a bunch of useless files, like website information, spam, or some of them are even empty.
Besides, I use a media server that has the functionality to delete only the media files, leaving the folder empty or with the subtitles only.
So, I decided to code a script to cleanup these folders, removing automatically empty folders or with no media inside, renaming unwanted 
expressions from folders and filenames, removing files with unwanted extensions and listing all of them as a catalog.
I though this project could help some other users too, so I decided to open it here on GitHub.  
*And this is how MediaCleanup was born...*

## About
MediaCleanup is a free tool to cleanup your media files and folders.
It will scan a provided path for folders and media files and can automatically:
- Find folders and files with specific expressions and rename them;
- Find empty folders or with no media files inside and remove them;
- Find files without specific extensions and remove them;
- List all of 'media files' and save it in a .txt file (like catalog).

It's simple script but can be very useful to maintain large collections of media.
MediaCleanup runs directly on your OS Terminal/Prompt and can manage files recursively inside a path provided by user.
User can see all changes and must confirm every step before the script apply it, so it is relatively safe but I recommend 
reading carefully all the instructions before using it.

## How to use it
### Download
First you need to download the MediaCleanup files.  
On the top of this page you should see a button with 'Clone or download' label. 
- Click on it and choose 'Download ZIP'.
- After completing the download, Unzip the downloaded file (Right-click and 'Extract Here').

### Run
Now you have to run the main script.
There are two ways for running this script:  
  
#### 1) If you have Python>=3 installed on your OS:

- Open up your OS Terminal/Prompt:
  - Ctrl + Alt + T (for Linux)
  - Click on 'Start Menu', type CMD and hit ENTER (for Windows)

- Go to the folder where do you extracted MediaCleanup, for example, type:
  > cd /home/\<user>/downloads/mediacleanup (for **Linux**, **Mac OS**)  
  > cd C:\Users\<user>\downloads\mediacleanup (for **Windows**)

- And then type the command below to execute the script:
  > mediacleanup.py

- If you can't get it running, try execute:
  > python mediacleanup.py

#### 2) If you don't have Python>=3
If you are on **Windows**: there's no need to install python. I've already create a .Exe file ready to be executed. 
- Go to the folder 'mediacleanup/exe/';
- Click on the executable file 'mediacleanup.exe'.

If you are on **another OS**:
- Download the latest Python version from [Python.org](https://www.python.org/getit/) and install it;
- Follow the steps above.

##### *ps.1: Not sure if it is supported by Python2.*
##### *ps.2: Not tested on Mac OS, but I think it should work fine.*

### Functionalities
Now you are with the main script running let's go through its functionalities.  
As soon as the MediaCleanup script starts, it will appear a bunch of options with the respective letter for user choose.
  
The options are:
- **c**: 
*In this option, the script will scan a specific path for files and folders that match expressions inside the file config/expressions.txt'. 
If any file/folder match, the software will list it to rename with the desired expression in 'config/expressions.txt'.* 

- **d**:
*If chosen, MediaCleanup will scan a specific path for folders that are empty or don't have any file with media extensions.
The software will use all extensions inside 'config/mediaextensions.txt' to compare and determine if a file is a media file or not.*

- **f**:
*The script will scan a specific path for files that don't have media extensions.
Like the 'd' option, it will use all extensions inside 'config/mediaextensions.txt' to compare against the files extensions.
If files extensions don't match, the software will list all and the user will be asked to remove them.*

- **l**:
*MediaCleanup will list all media files (according 'config/mediaextensions.txt') inside the provide path and show them.
The user will be asked to save the list as a .txt file (mediacatalog.txt) and the software will ask for destination path.
If user type 'ENTER' to the destination path, the .txt file will be crated in the same scanned path.*

- **A**:
*If user choose A (note the Caps here), the script will run ALL above options in a sequence.*

- **h**:
*Show up help and about information.*

- **q**:
*If user type 'q' and press Enter, the software will stop and quit.*

Choose one of the options above, type the respective letter and press ENTER.

After choosing the desired option, MediaCleanup will ask for the path to be scanned.

Provide a path for the search, like:  
> /home/\<user>/videos (for **Linux**, **Mac OS**)  
> C:\Users\<user>\Videos (for **Windows**)  

If a selected path was entered, the script will start the scanning process.
this can take a while, depending on how many files and folders are there, sizes, etc.

As soon as it completed the scanning, it will show up the information according the chosen option.
Everytime some file or folder is about to be renamed or removed, the software will wait for user to confirm, 
typing 'y' and pressing ENTER.
When it is done with the processing, it will wait for user press ENTER to continue until it reach the end.

When all the operation is completed, the script gives the option to run again if user type 'r' and press ENTER.

Further I'll add more functionalities to the code...  
    
##### *ps.3: May occur issues with your OS Terminal when displaying long lists of files/folders due its limited number of lines.*
##### *I recommend changing the Terminal preferences to the MAXIMUM scrollback or screen buffer size.*  
  
## Configuration Files
As seen in the **Functionalities** section, some of MediaCleanup steps relies on configuration files.
The configuration files are .txt files inside 'config/' folder.

There are 2 configuration files:
- **mediaextensions.txt**:
The content of this file tells to the MediaCleanup which extensions will be considered MEDIA EXTENSIONS.
All extensions written in a single line that doesn't start with '#' will be used to compare against the files extensions.
You can edit this this file, as long you maintain the same format: one extension per line, starting with a dot.
If this file is removed or renamed, the script will show an error.

- **expressions.txt**:
In this file there are all the options you want to find in folders and filenames and the expressions you want to replace them.
You can edit this file too, but you have to maintain this specific format: 'old=new'.
For example, if you want to replace all letter 'x' in folder and filenames for 'y', you just have to write 'x=y'.
As the 'mediaextensions.txt', you should write one expression per line, in a line that doesn't start with '#'.
If this file is removed or renamed, the script will show an error too.

## License
All this project is under GPLv3 license. 
You can find the complete license in the 'COPYING.txt' file and Copyrights notes inside the codes.
These files and notes MUST NOT been removed if you're using or sharing this project.

## Warning
**Use at your own risk!**

Although the script always shows what's going to be renamed or removed and asks for confirmation, if you have very important data 
inside the path informed I recommend you backup your data.

## Contact
If you have any doubt, suggestions or want to contact me, use my email viniciusov@hotmail.com.
