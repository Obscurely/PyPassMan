# PyPassMan - password manager app
[![Current Version](https://img.shields.io/badge/version-0.0.1-green.svg)](https://github.com/Obscurely/PyPassMan)<br />
Password Manager created with Python.

## Table of contents
- [General info](#general-info)
- [Technologies](#technologies)
- [Program dependencies](#program-dependencies)
- [Setup](#setup)
  - [To run PyPassMan](#to-run-pypassman)
    - [For master branch version](#for-master-branch-version)
    - [For release version](#for-release-version)
  - [To install PyPassMan](#to-install-pypassman)
  - [To uninstall PyPassMan](#to-uninstall-pypassman)
- [Functionalities](#functionalities)
- [Progress status and Known issues](#progress-status-and-known-issues)
- [How it works](#how-it-works)
- [If you want to use my work](#if-you-want-to-use-my-work)
- [Screenshots](#screenshots)
- [Other notes](#other-notes)

## General info
This is an open-source cross-platform local password manager (runs by creating encrypted files on your pc offline) created with python that aims to one day reach the level of something like LastPass and even further, with privacy and stability in mind.

## Technologies
Project is created with:
* Python 3.9.1
* Qt Designer 6.0.0

## Program dependencies
All of the dependecies can be found in the **requirements.txt** file found in every directory.

## Setup
### To run PyPassMan:
#### For master branch version:
* Extract everything in a folder
* run pip install requirements.txt
* double click to open PyPassMan.py (or do py/python3 PyPassMan.py)

#### For release version:
* Extract everything in a folder
* double click PyPassMan.exe

### To install PyPassMan:
* double click the installer executable
* select a location to install to
* click next and install

### To uninstall PyPassMan:
* double click the installer executable
* select the location to uninstall from
* click uninstall (if there are any error refer to [Manual Uninstall](#manual-uninstall))

## Functionalities
- Operations on Accounts Folders: Create Accounts Folders, List Accounts Folders, Remove Accounts Folder
- Operations for Accounts Folders: Add Account To Folder (optionally with labels), Get Accounts in a Folder (prints them sorted with numbers before them and the label where exists), Remove Accounts in a Folder, Clear all Accounts in a Folder
- Generate Strong Password
- Backup
- Restore
- Logout
  
## Progress status and Known issues
Go to Projects Tab under **PyPassMan Progress Board**

## How it works
The app uses **.json files** to store all the needed data (PyPassMan accounts aswell as accounts folders and accounts in them). They are **encrypted** using an algorithm based on an **encryption key**.It runs completely **offline** so no worries your data is **safe**.

## If you want to use my work
Just stick to the **license conditions**: Your program has to be **open-source**, **credit me**, use the **same license** and **state any changes**.

## Screenshots
![Login Window](https://github.com/Obscurely/PyPassMan/blob/master/screenshots/Login%20into%20account%20window.png)
![Locker Window](https://github.com/Obscurely/PyPassMan/blob/master/screenshots/Locker%20window.png)

## Other notes:
* If you have any issues post them and in the issues tab using this format: *the app version you are using*, *the python version you are using*, *what kind of release you use*, *how you run it on your system python/release/installed*, *the issue/s*, *what you did before that happen*, *other notes you think are useful*. I will try to fix them as soon as I can and have time to
* If you want to ask questions you can use the discussions tab
* Check wiki for other things about the app
