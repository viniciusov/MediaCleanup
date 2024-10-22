# MediaCleanup

## The problem
I started to code this program to help me with an issue.  
I download a lot of media files and organize them in folders with these files, subtitles, audio, images, etc., but I realize that a lot of those folders are empty or contain just a bunch of useless files, like website information, spam, etc.  
Besides, I use a media server that has the functionality to remotely delete only the media files, leaving the folder empty or only with the subtitles files inside.  
So, I decided to code a script to cleanup these folders, removing automatically empty folders or with no media inside, renaming unwanted 
expressions from folders and filenames, removing files with unwanted extensions and listing all of them as a catalog.

I know there are some alternatives on the web with more complex features like graphical interface and other stuff, but I would like to create something efficient and simple. More portable, just click and run.  
Just to give you an idea, I tried 2 different software for execute these tasks: I couldn't run one of them on my OS (and I can't unninstall it completely - a lot of bugs!) and another require Java updates as soon as it was installed.

*And this is how MediaCleanup was born...*

I though this project could help some other users too, so I decided to open it here on GitHub.  

## About
MediaCleanup is a free tool to cleanup your media files and folders.
It will scan a provided path for folders and media files and can automatically:
- Find folders and files with specific expressions and rename them;
- Find empty folders or with no media files inside and remove them;
- Find files without specific extensions and remove them;
- List all 'media files' and save it in a .txt file (like catalog).

It's simple script but can be very useful to maintain large collections of media.  
MediaCleanup runs directly on your OS Terminal/Prompt and can manage files **recursively** inside a path provided by user.  
User can see all changes and must confirm every step before the script apply them, so it is relatively safe but I recommend 
reading carefully all the instructions before using it.

## How to use it
### Download
First you need to download the MediaCleanup files.  
On the top of this page you should see a button with a 'Clone or download' label. 
- Click on it and choose **Download ZIP**.
- After completing the download, **Unzip** the downloaded file (Right-click and 'Extract Here').

### Install & Run
Now there are **two ways** to proceed:  
  
#### 1) If you have Python>=3 installed on your Operating System:

- Open up your OS Terminal/Prompt:
  - Search for Terminal in your OS main menu (for Linux)
  - Click on 'Start Menu', type 'cmd' and hit ENTER (for Windows)

- Go to the folder where you extracted MediaCleanup, for example, type:
  > cd /home/\<user>/downloads/MediaCleanup-master (for **Linux**, **Mac OS**)  
  > cd C:\Users\<user>\downloads\MediaCleanup-master (for **Windows**)  

  Where \<user> should be the name of your user.  
  
- Install the requirements with the command below:
  > sudo python3 setup.py install (for **Linux**, **Mac OS**)  
  > python setup.py install (for **Windows**) 
  
  If you got the "No Module named Setuptools" error, you should install the Setuptools module.  
  Check on the web how to install it and repeat the above process before proceeding.  
  
- And execute the script:
  > ./mediacleanup.py (for **Linux**, **Mac OS**)  
  > mediacleanup.py (for **Windows**)
  
- If you can't get it running, try execute:
  > python3 mediacleanup.py (for **Linux**, **Mac OS**)  
  > python mediacleanup.py (for **Windows**)   
  
#### 2) If you don't have Python>=3
- If you are on **Windows**, there's no need to install python. I've already create a .exe file ready to be executed. 
  - Go to the folder 'mediacleanup/exe/';
  - Execute file 'mediacleanup.exe'.

- If you are on **another OS**:
  - Download the latest Python version from [Python.org](https://www.python.org/getit/) and install it;
  - Follow the steps above.

##### *ps.1: Not sure if it is supported by Python2.*
##### *ps.2: Not tested on MacOS, but I think it should work fine.*
  
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
*If user choose A (note the Caps here), the script will run ALL above options in a sequence.  
For best cleaning, it will run in the following sequence: f->d->c->l.*   

- **h**:
*Show up help and about information.*

- **q**:
*If user type 'q' and press Enter, the software will stop and quit.*

Choose one of the options above, type the respective letter and press ENTER.  
After choosing the desired option, MediaCleanup will ask for the path to be scanned.

Provide a path for the search, like:  
> /home/\<user>/videos (for **Linux**, **MacOS**)  
> C:\Users\<user>\Videos (for **Windows**)  
  
If a valid path was entered, the script will start the scanning process (this can take a while, depending on how many files and folders are there).  

Alternatively, you can provide the desired option and path as command-line paramaters to run in a single command:  
> python3 mediacleanup.py -A /home/user/videos (for **Linux**, **MacOS**)  
> mediacleanup.exe -A C:\Users\user\Videos (for **Windows**)  
  
As soon as it completed the scanning, it will show up the information according the chosen option.  
Everytime some file or folder is about to be renamed or removed, the software will wait for user to confirm, 
typing 'y' and pressing ENTER.
  
When processing has done, it will wait for the user to press ENTER to continue until it reaches the end.  
After all operations have finished, the script gives the option to run again if the user type 'r' and press ENTER.
   
##### *ps.3: May occur issues with your OS Terminal when displaying long lists of files/folders due its limited number of lines.*
##### *I recommend changing the Terminal preferences to the MAXIMUM scrollback or screen buffer size.*
  
## Configuration Files
As seen in the Functionalities section, some of MediaCleanup steps relies on configuration files.
The configuration files are .txt files inside 'config/' folder.

There are 2 configuration files:
- **mediaextensions.txt**  
The content of this file tells to the MediaCleanup which extensions will be considered media extensions.  
All extensions written in a single line that doesn't start with '#' will be used to compare against the files extensions.  
You can edit this this file, as long you maintain the same format: one extension per line, starting with a dot.  
If this file is removed or renamed, the script will show an error.  

- **expressions.txt**  
In this file there are all the options you want to find in folders and filenames and the expressions you want to replace them.  
You can edit this file too, but you have to maintain this specific format: 'old=new'.  
For example, if you want to replace all letter 'x' in folder and filenames for 'y', you just have to write 'x=y'.  
As the 'mediaextensions.txt', you should write one expression per line, in a line that doesn't start with '#'.  
If this file is removed or renamed, the script will show an error too.  

## Errors
You may get errors when executing some options.  
If removing or renaming items, be sure that you must have Write Permissions to do so and if the file or folder aren't Read-Only, otherwise the script will not remove/rename them. In addition, if you get errors when renaming, check if there isn't a file or folder already in that location with the same new name.  
If you got an unexpected error, please let me know.  

## Warning
**Use at your own risk!**  
Although the script always shows what's going to be renamed or removed (sent to trash) and asks for confirmation, if you have very important data inside the informed path I recommend you backup your data.  

## License
All this project is under GPLv3 license. 
You can find the complete license in the 'COPYING.txt' file and a Copyright note inside the main script.
These information must not been removed if you're using or sharing this project.

## Contact
If you have any doubt, suggestions or want to contact me, use my email viniciusov@hotmail.com.
