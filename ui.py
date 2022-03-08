# ui.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

from re import L, fullmatch
import re
from Profile import Profile
from ds_client import send


class UI():
    adminMode: bool = False
    #goal: have different functions that return strings, if admin mode is on, then it returns ''
    #i am to lazy to implement the error reports, maybe another day
    #error explenations

    
    #the user will only be able to change one attribute at a time. It is to much to ask the user to 
    #change everything at once
    def E_inputCreator(self):
        fullInp = 'E '
        print('What would you like to eddit?')
        inp = input('Username (-usr), Password (-pwd), Bio (-bio), Server IP (-srv) Add a post (-addpost), or to delete a post (-delpost):\n')
        while inp not in ['-usr', '-pwd', '-bio', '-addpost', '-delpost', '-srv']:
            inp = input('You did not enter a valid option to eddit try again:\n')
        fullInp += inp + ' "'

        if inp in ['-usr', '-pwd', '-bio', '-srv']:
            inp = input('What would you like to change it to?\n')
        elif inp == '-addpost':
            print('You can get the weather at the moment by typing @weather into your post')
            print('You can also get the top artist in with @lastfm anda random top artist with @lastfmRand')
            inp = input('Your post:\n')
        elif inp == '-delpost':
            inp = input('index of the post you want to delete:\n')
            notValid = True
            while notValid:
                for char in inp:
                    if char not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                        inp = input('not a number, please try again')
                    else:
                        notValid = False
        fullInp += inp + '"'
        
        return fullInp

    def P_inputCreator(self):
        fullInp = 'P '
        print('What would you like to print?')
        inp = input('Username (-usr), Password (-pwd), Bio (-bio), All of your posts (-posts), one of your posts (-post), everything in your file (-all):\n')
        while inp not in ['-usr', '-pwd', '-bio', '-posts', '-post', '-all']:
            inp = input('You did not enter a valid option to print try again:\n')
        fullInp += inp + ' '

        if inp == '-post':
            inp = input('index of the post you want to print:\n')
            notValid = True
            while notValid:
                for char in inp:
                    if char not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                        inp = input('not a number, please try again')
                    else:
                        notValid = False
            fullInp += inp
        return fullInp

    def C_inputCreator(self):
        fullInp = 'C'
        inp = input('Please enter a directory to create the file:\n')
        fullInp += ' ' + inp + ' -n '
        inp = input('Please enter the file name you would like:\n')
        fullInp += inp
        return fullInp

    def O_inputCreator(self):
        fullInp = 'O '
        inp = input('Please enter the file path you would like to load:\n')
        fullInp += ' ' + inp
        return fullInp

    def U_inputCreator(self, hasServer):
        fullInp = 'U '
        if not hasServer:
            print('You have not connected to a server yet')
            inp = input('What server would you like to upload to?: \n')
            fullInp += '-srv ' + inp
        else:
            print('What/How would you like to upload?')
            inp = input('Upload one of your posts (-post), Upload all your posts (-posts), Upload a new post (-wrt):\n')
            while inp not in ['-post', '-posts', '-wrt']:
                inp = input('You did not enter a valid option to print try again:\n')
            fullInp += inp + ' '

            if inp == '-post':
                inp = input('index of the post you want to upload:\n')
                notValid = True
                while notValid:
                    for char in inp:
                        if char not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                            inp = input('not a number, please try again')
                        else:
                            notValid = False
                fullInp += inp
            elif inp == '-wrt':
                inp = input('What message do you want posted?: \n')
                fullInp += inp 
            print(fullInp)
        return fullInp

    

    #the user interface creates the input that would be taken in admin mode. very dope
    def inputCreator(self, loaded: bool, fileLoaded: str, hasServer:bool):
        inp = ''
        fullInp = ''
        if loaded:
            print(f'You have {fileLoaded} loaded')
            inp = input('You can Edit (E), Print (P), Upload to the internet (U) or Create (C) or Load(O) another file:\n')
            if inp == 'E':
                fullInp = self.E_inputCreator()
            elif inp == 'P':
                fullInp = self.P_inputCreator()
            elif inp == 'C':
                fullInp = self.C_inputCreator()
            elif inp == 'O':
                fullInp = self.O_inputCreator()
            elif inp == 'U':
                fullInp = self.U_inputCreator(hasServer)
            return fullInp

        else:
            inp = input('"C" to create a file in a specific directory, and "O" to Load one:\n')
            if inp == 'C':
                fullInp = self.C_inputCreator()
                return fullInp
            elif inp == 'O':
                fullInp += inp
                inp = input('Please enter the file path you would like to load:\n')
                fullInp += ' ' + inp
                return fullInp
            elif inp == 'admin':
                self.adminMode = 'True'
                return 'admin'
            else:
                print('sorry come again?')
                return fullInp


# Replace the following placeholders with your information.

# Paolo Andrew, Manalo, Urani
# Uranip@uci.edu    
# 24555312
