MediaInfoWrapper is extremely easy and simple to set up.

Step 1: Decide where to put it.  This script is all self contained, meaning that it has everything it needs to run right out of the box.

Step 2: Download script.  You will need everything in the scripts folder and everything in the exe folder, but the exe folder is pretty much just shortcuts that you need to add to your PATH variable on either Windows or Mac.

Step 3: Download latest version of MediaInfo.  You only want the CLI version (CLI = Command Line Interface), this isn't meant to look pretty, this script was developed for the functionality.  Place the MediaInfo exe inside of a folder called unixExecutables on the root of this directory structure.

Step 4: Create links to MediaInfo CLI exe and mediaInfoWrapper.py in the exe folder on the root.  Then make sure the exe folder is in your PATH environment variable.  Make sure the root of this script is in your PYTHONPATH environment variable too.

And you should be ready to roll.

Example setup: I've downloaded the folder and placed my MediaInfo folder in a location on a server and I'm working off of a Mac, so my root will be here:

/Volumes/SERVER/SAMPLEFOLDER/standalone/mediaInfoWrapper/

Inside of the root folder the file structure should look like this:

mediaInfoWrapper/__init__.py (This is actually essential so make sure you have this in here, but don't worry, the __init__.py file is blank [That's just how Python works])
mediaInfoWrapper/exe/ (My PATH links in here, these links allow me to run this standalone function from the terminal)
mediaInfoWrapper/scripts/
mediaInfoWrapper/unixExecutables/ (MediaInfo executable goes in here)

Inside of the scripts folder the files and file structure should look like this:

(root)/scripts/__init__.py
(root)/scripts/config.py
(root)/scripts/mediaInfoWrapper.py
(root)/scripts/ops.py
(root)/scripts/testModules/ (This simply has a test function in it, you can use that test function to check and make sure mediaInfo is working properly)

NOTE: The mediaInfoWrapper.py in the scripts folder is the file you want everything to link to, for me, my link was titled miWrap, which means when I went into terminal I typed miWrap and then gave it whatever parameters I wanted to send the function.

However, if you want to have other scripts use this function, then you are looking for the mIWrap function inside of the mediaInfoWrapper.py file, the mIWrap function is the one that calls all of the necessary functions and it will pass back the information in the form of dictionaries ("key -> value" pairs).

Also: mediaInfoWrapper.py needs an executable (link), inside of the exe folder on the root titled mediainfo, so for optimal performance of this script and function you should put two links inside of the exe folder:

(root)/exe/mediainfo	---> A link to the MediaInfo CLI executable
(root)/exe/miWrap		---> A link to (root)/scripts/mediaInfoWrapper.py

And in a standard Python script, if you are wanting to run this from a Python script, you will need to make sure the root of this folder is in your PYTHONPATH environment variable, then you can simply use the following statement:

from mediaInfoWrapper.scripts import mediaInfoWrapper as miWrapper

Then you will be able to access the necessary function:

miWrapper.mIWrap()

The mIWrap function only requires a True or False value (for quiet or prompt modes), and a file, everything else the function will prompt for unless it is run in quiet mode.

Specifically this is the parameters for mIWrap:

mIWrap( quiet, file, all=None, category=None, detailRequests=None )

All is a boolean value, category is a list (array), and detailRequest is a list (array), but detailRequest has to have 'category;request' pairs in it otherwise the script won't like it.  If you aren't sure what category you want then put 'None' as the category and the script will ask you for the appropriate categories.