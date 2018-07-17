# Script to copy Android class or xml dependency

This is a script to copy the dependent resources like drawables, xmls, strings, dimens, colors from a specified class file or xml file of an Android project. This is a python script and you need to install *Python 3 or greater version* to run this script. 

## Steps to copy dependency

### 1

Copy the path of the class file or xml file from the Android project
![Copy file path][copy_path]

### 2

First navigate to the root directory of your Android project. Then copy the script *ResourceCopierAndroid.py* to that root directory. Then open Command Promt or Terminal on that direcotory and Run the application using the following command:
    python ResourceCopierAndroid.py
You will be given a prompt to paste a file path. Then paste the file path using `Ctrl + v` and press `Enter`

Then wait for the script to complete searching.

### 3
You will get all the dependent resources on a folder named `ziftaRes` within that folder you will get all the resources you need. All the drawables and files will be copied to folders named according to the dependent class or xml files. Also there will be a `res` folder where you will get all the files together. The colors, string and dimen files on the `ziftaRes` folder may contain duplicate referance. You will also get file specific folder for each file dependent on the selected one.

## Recomendations

This script may fail if the class files are not written in standard indentations. It may also fail if the android project does not contain any resource file or text which the class or xml file is dependent on.



[copy_path]: https://github.com/triplemzim/androidresourcecopier/images/copy_path.png