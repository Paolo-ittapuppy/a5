# a4.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python
from ast import Return
import cmd
from glob import escape
from http import server
from logging.config import valid_ident
import pathlib
import re
from tkinter import N
from tkinter.messagebox import RETRY
from Profile import Profile, Post
from pathlib import Path
import json, ds_client, socket
from ui import UI
from OpenWeather import OpenWeather
from LastFM import LastFM

#to handle inputs given by the user
class InputHandler():

    _inputPure = None
    cmd = None
    path = None
    optionsToUse = None
    optionstoUseIndexes = None
    optionsToUseInputs = None

    #when you make an input handler object, you need to put the raw input as a string
    def __init__(self, pureinp) -> None:
        self._inputPure = pureinp

    #reset the object, might not be the best way to go about getting new input but it works
    def reset(self):
        self._inputPure = None
        self.cmd = None
        self.path = None
        self.optionsToUse = None
        self.optionstoUseIndexes = None
        self.optionsToUseInputs = None

    #chcks if a letter is one of the 4 comands in this project
    def isCmdValid(self, cmd):
        if cmd in ['C', 'O', 'E', 'P', 'U']:
            return True
        else:
            return False

    #obtains the first letter in the input and then if its a valid command the cmd attribute is updtated
    def getCmd(self) -> str:
        if self._inputPure != None:
            if len(self._inputPure) > 0:
                t = self._inputPure[0]
                if self.isCmdValid(t):
                    self.cmd = self._inputPure[0]
                    return self.cmd
        print('ERROR')
        return None
    
    #Checks if from the 2nd index that there is a valid path.  the path attribute is updated if there is a valid path
    def getPath(self) -> Path:
        try:
            end = self._inputPure.find(' -')
            p = None
            if end != -1:
                p = self._inputPure[2:end]
            else:
                p = self._inputPure[2:]
            pat = Path(p)
            if pat.exists():
                self.path = pat
                return pat
            else:
                print('ERROR')
                return None

        except:
            print('ERROR')
            return None

    #given a list of options, checks if it is a valid combination of options
    def _isOptionsValid(self, inputsToUse: list):
        s = set(inputsToUse)
        if self.cmd == 'C':
            if s.issubset({' -n'}):
                return True
            else: 
                return False
        elif self.cmd == 'O':
            if s.issubset({}):
                return True
            else:
                return False
        elif self.cmd == 'E':
            if s.issubset({' -usr', ' -pwd', ' -bio', ' -addpost', ' -delpost', ' -srv'}):
                return True
            else:
                return False
        elif self.cmd == 'P':
            if s.issubset({' -usr', ' -pwd', ' -bio', ' -posts', ' -post', ' -all'}):
                return True
        elif self.cmd == 'U':
            if s.issubset({' -post', ' -posts', ' -wrt', ' -srv'}):
                return True
            else:
                return False
        else:
            return False

    #uses the object input attribute and obtains all the options possible. it then chekcs if thos opetions are valid and if so 
    #it will update the options to use attribute and their indexes stored in a parralel list
    def getOptions(self):
        optionsToUse = []
        inputIndexes = []
        for option in [' -srv', ' -n', ' -usr', ' -pwd', ' -bio', ' -posts', ' -post', 
                       ' -all', ' -addpost', ' -delpost', ' -wrt']:
            place = self._inputPure.find(option)
            if place != -1:
                if self._inputPure.count(option) <= 1:
                    if option == ' -post':
                        start = self._inputPure.find(option) + len(option) + 1
                        try:
                            if self._inputPure[start -1 ] == 's':
                                continue
                        except:
                            print('ERROR')
                            self.optionsToUse = None
                            return None
                    optionsToUse.append(option)
                    inputIndexes.append(place)
                else: 
                    print('ERROR')
                    self.optionsToUse = None
                    return None
        if self._isOptionsValid(optionsToUse) and optionsToUse != []:
            self.optionsToUse = optionsToUse
            self.optionstoUseIndexes = inputIndexes
            return optionsToUse
        else:
            if self.cmd != 'O':
                print('ERROR!')
            self.optionsToUse = None
            self.optionstoUseIndexes = None
            return None

    #Obtains all the inputs after each option and checks if those inputs are valid. I should make smaller functions to make this code more 
    #readable, but i am too lazy at this point. there is also alot of repeated code that could be condensed. might fix later
    def getInputs(self):
        inp = self._inputPure
        options = self.optionsToUse
        inputsForOptions = []
        for i in range(len(options)):
            opt = options[i]
            start = inp.find(opt) + len(opt)
            inputForOption = ''
            end = inp[start:].find(' -')
            if end == -1:
                inputForOption = inp[start + 1:]
            else:
                end += len(inp[:start])
                inputForOption = inp[start + 1: end]

            if opt in [' -delpost', ' -post']:
                try:
                    inputForOption = (int(inputForOption))
                except:
                    print('ERROR')
                    self.optionsToUse = None
                    return
            elif self.cmd == 'E':
                #should make this into a function
                if opt in [' -usr', ' -pwd', ' -bio', ' -addpost', ' -srv']:
                    try:
                        #should make this boolean statement its own function
                        if (inputForOption[0] == '"' and inputForOption[-1] == '"') or (inputForOption[0] == "'" and inputForOption[-1] == "'"):
                            inputForOption = inputForOption[1:-1]
                            if inputForOption == "":
                                print('ERROR')
                                self.optionsToUse = None
                                return
                        else:
                            print('ERROR')
                            self.optionsToUse = None
                            return
                    except: 
                        print('ERROR')
                        self.optionsToUse = None
                        return
            elif self.cmd == 'P':
                if inputForOption != '':
                    print('ERROR')
                    self.optionsToUse = None
                    return
            inputsForOptions.append(inputForOption)
        if inputsForOptions != []:
            self.optionsToUseInputs = inputsForOptions
        else:
            if self.cmd != 'O':
                print('ERROR')
            self.optionsToUseInputs = None

    #goes through the input given and gets all the nessesary info, such as the command, path, options and inputs when needed
    def proccessInp(self):
        self.getCmd()
        if self.cmd != None:
            if self.cmd in ['C', 'O']:
                self.getPath()
            self.getOptions()
            if self.optionsToUse != None:
                self.getInputs()

    #after the input has been proccessed, this function will return true if the input is valid or false if you shouldnt run naything with the input
    def validInp(self) -> bool:
        if self.cmd == 'O':
            if self.path != None:
                return True
            else:
                return False
        if None in [self.cmd, self.optionsToUse, self.optionsToUseInputs]:
            return False
        else:
            return True

    #tester code
    def printInp(self):
        print(self.cmd)
        print(self.path)
        print(self.optionsToUse)
        print(self.optionstoUseIndexes)
        print(self.optionsToUseInputs)

#this class will deal with the profile class and the dsu file being updated with the profile information
class DSUHandler():
    DSUpath: Path = None
    inputs: InputHandler = None
    prof: Profile = None

    #input a input handler object into the instantiaon of the object
    def __init__(self, inp: InputHandler) -> None:
        self.inputs = inp
    
    def validIP(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except:
            return False
            



    #if making a new profile, it will ask the user for all the information needed for the profile
    def makeProfile(self):
        userName = ' '
        while ' ' in userName:
            userName = input('UserName: ')
            if ' ' in userName:
                print('No whitespaces alowed, try again: ')
        
        password = ' '
        while ' ' in password:
            password = input('Password: ')
            if ' ' in userName:
                print('No whitespaces alowed, try again: ')
        
        bio = input('Bio: ')

        serv = ''
        
        '''while not self.validIP(serv):
            serv = input('Enter server IP adress you would like to upload to: ')
            if not self.validIP(serv):
                print('Invalid IP adress, try again')
        '''
        prof = Profile(serv, userName, password)
        prof.bio = bio



        #print(prof.username, prof.password, prof.bio)
        return prof

    # takes the create file directory and file name and creates a dsu path
    def makeDSUPath(self):
        if self.inputs.validInp():
            dir = self.inputs.path.absolute()
            end = self.inputs.optionsToUseInputs[0] + '.dsu'
            self.DSUpath = Path(dir) / end

    #this is pretty much the profile.load function except its to test if it is loadable. 
    def loadable(self, p):
        try:
            f = open(p, 'r')
            obj = json.load(f)
            keys = obj.keys()
            shouldBeKeys = ["username", 'password', 'dsuserver', 'bio', '_posts']
            for i in keys:
                #this could be optimized and it also does not catch every case. need to fix
                if i not in shouldBeKeys:
                    return False
                else:
                    shouldBeKeys.remove(i)
            if shouldBeKeys != []:
                return False
            for post_obj in obj['_posts']:
                testKeys = post_obj.keys()
                if 'entry' not in testKeys or 'timestamp' not in testKeys:
                    return False
            return True
        except:
            return False

    # takes the premade dsu file and makes a profile object to store in the dsu handler.
    def loadDSU(self):
        if self.DSUpath == None:
            self.DSUpath = self.inputs.path
        p = self.DSUpath
        if p.exists() and p.suffix == '.dsu' and self.loadable(p):
            prof = Profile()
            prof.load_profile(p)
            self.prof = prof
            self.DSUpath = p
        else:
            self.DSUpath = None
            print('ERROR')

    #makes a new dsu file and create a profile
    def createDSU(self):
        if self.inputs.path != None:
            self.makeDSUPath()
            p = self.DSUpath
            if p.exists() == False:
                self.prof = self.makeProfile()
                p.touch()
                self.prof.save_profile(p)
            else:
                self.loadDSU()

    #given a string, this code will tranclude it with the Lastfm and 
    #openweather api 
    def transcludeMSG(self, msg: str):
        weather = OpenWeather()
        weather.set_apikey('47c57598a8dea1145b37db4121f67161')
        weather.load_data()
        fm = LastFM()
        fm.set_apikey('67a0e9526f7a52637dde3a5539499e56')
        fm.load_data()
        p = weather.transclude(msg)
        p = fm.transclude(p)
        return p

    #if the user inputs e, it will eddit the dsu file accordingly to the options given and their inputs
    def edditDSU(self):
        optionsToUse = self.inputs.optionsToUse
        inps = self.inputs.optionsToUseInputs
        prof = self.prof
        for i in range(len(optionsToUse)):
            for i in range(len(optionsToUse)):
                if optionsToUse[i] == ' -usr':
                    prof.username = inps[i]
                elif optionsToUse[i] == ' -pwd':
                    prof.password = inps[i]
                elif optionsToUse[i] == ' -bio':
                    prof.bio = inps[i]
                elif optionsToUse[i] == ' -srv':
                    prof.dsuserver = inps[i]
                elif optionsToUse[i] == ' -addpost':
                    #if the user wants to add a post, it will tranclude the post they want to add to their user
                    p = self.transcludeMSG(inps[i])
                    post = Post(p)
                    prof.add_post(post)
                elif optionsToUse[i] == ' -delpost':
                    if len(prof._posts) > int(inps[i]):
                        prof.del_post(int(inps[i]))
                    else: 
                        print('ERROR')
                prof.save_profile(self.DSUpath)

    #if the user inputs p, this function will print all the inofrmation that the user inputed as options
    def printDSU(self):
        optionsToUse = self.inputs.optionsToUse
        inps = self.inputs.optionsToUseInputs
        prof = self.prof
        for i in range(len(optionsToUse)):
            if optionsToUse[i] == ' -usr':
                print(prof.username)
            elif optionsToUse[i] == ' -pwd':
                print(prof.password)
            elif optionsToUse[i] == ' -bio':
                print(prof.bio)
            elif optionsToUse[i] == ' -posts':
                for x in range(len(prof._posts)):
                    print(f'{x}: ' + str(prof._posts[x]))
            elif optionsToUse[i] == ' -post':
                if len(prof._posts) > int(inps[i]):
                    print(f'{inps[i]}: ' + str(prof._posts[int(inps[i])]))
                else: 
                    print('ERROR')
            elif optionsToUse[i] == ' -all':
                f = self.DSUpath.open('r')
                content = f.read()
                print(content)
                f.close()

    '168.235.86.101'
    #Given a server inputed by a user, this code will upload to that server whatever the user wants to upload
    def uploadDSUtoServer(self):
        optionsToUse = self.inputs.optionsToUse
        inps = self.inputs.optionsToUseInputs
        prof = self.prof
        for i in range(len(optionsToUse)):
            if optionsToUse[i] == ' -srv':
                prof.dsuserver = inps[i]
                prof.save_profile(self.DSUpath)
                self.prof = prof
            if optionsToUse[i] == ' -post':
                if len(prof._posts) > int(inps[i]):
                    print(ds_client.send(prof.dsuserver, 3021, prof.username, prof.password, prof._posts[int(inps[i])].get_entry(), prof.bio))
                else:
                    print('ERROR')
            elif optionsToUse[i] == ' -posts':
                for post in prof._posts:
                    print(ds_client.send(prof.dsuserver, 3021, prof.username, prof.password, post.get_entry(), prof.bio))
            elif optionsToUse[i] == ' -wrt':
                msg = self.transcludeMSG(inps[i])
                print(ds_client.send(prof.dsuserver, 3021, prof.username, prof.password, msg, prof.bio))
        

    # takes the input hadnler object and uses the appropriate functions 
    def run(self):
        cmd = self.inputs.cmd
        #print('huh', self.DSUpath != None)
        if cmd == 'C':
            self.createDSU()
        elif cmd == 'O':
            self.loadDSU()
        elif cmd == 'E' and self.DSUpath != None:
            self.edditDSU()
        elif cmd == 'P' and self.DSUpath != None:
            self.printDSU()
        elif cmd == 'U' and self.DSUpath != None:
            self.uploadDSUtoServer()
        else:
            print('ERROR')

# keeps taking new inputs intill the command = q
def main():
    ui = UI()
    i = None
    inp = InputHandler('')
    dsu = DSUHandler('')
    while inp.cmd != 'q':
        loaded = dsu.DSUpath != None
        hasServer = None
        try:
            hasServer = dsu.prof.dsuserver != ''
        except:
            hasServer = False
        if ui.adminMode == False:
            i = ui.inputCreator(loaded, dsu.DSUpath, hasServer)
        else:
            i = input()
        #print(i)
        if i!= '' and i != 'admin':
            inp = InputHandler(i)
            inp.proccessInp()
            #inp.printInp()
            
            if inp.validInp():
                if dsu == None:
                    dsu = DSUHandler(inp)
                else:
                    dsu.inputs = inp
                dsu.run()        

if __name__ == "__main__":
    main()

        
# Paolo Andrew, Manalo, Urani
# Uranip@uci.edu
# 41635
