# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Paolo Andrew, Manalo, Urani
# uranip@uci.edu
# 24555312
from ctypes.wintypes import MSG
from email.message import Message
from http import server
from lib2to3.pgen2 import token
from ntpath import join
from pydoc import cli
import re
from shutil import unregister_unpack_format
import socket
import json
from urllib import response
from Profile import Post
import ds_protocol
from NaClProfile import NaClProfile

global messagePrint
messagePrint = ''

{"join": {"username": "paul","password": "123","token":""}}
{"token":"user_token", "post": {"entry": "Hello World!","timestamp": "1603167689.3928561"}}
{"token":"user_token", "bio": {"entry": "Hello World!","timestamp": "1603167689.3928561"}}


#connect('168.235.86.101', 3021)
'{"response": {"type": "error", "message": "Invalid DS Protocol format"}}'

#print(connectable('168.235.86.101', 3021))

def makeJoin(usrnme:str, pswd:str, selfPubKey):
  m = '{"join": {"username": "' + usrnme + '","password": "' + pswd + '","token":"'+selfPubKey+'"}}'
  return m.encode('utf-8')


def pushToServer(server:str, port:int, m:str):
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
      client.connect((server, port))
      client.sendall(m)
      msg = client.recv(4096)
      return msg.decode('utf-8')
  except:
    return ''

      
{"token":"user_token", "post": {"entry": "Hello World!","timestamp": "1603167689.3928561"}}
def makePost(msg:str, token: str):
  m = '{"token":"' + token + '", "post": ' + msg + '}'
  return m.encode('utf-8')

def newBio(msg:str, token:str):
  m = '{"token":"' + token + '", "bio": ' + msg + '}'
  return m.encode('utf-8')


#print(command('{"join": {"username": "paul","password": "123","token":""}}'))
def getValidity(resp):
  obj = json.loads(resp)
  valid = None
  try:
    valid = obj['response']['type']
    return valid == 'ok'
  except:
    return False 

def getToken(resp):
  obj = json.loads(resp)
  token = obj['response']['token']
  return token

def makeMSG(msg: str):
  m = Post(msg)
  return json.dumps(m)



def send(server:str, port:int, username:str, password:str, pubToken:str, message:str, bio:str=None ):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  valid1 = True
  valid2 = True
  valid3 = True
  global messagePrint
  messagePrint = ''
  try:
    if ds_protocol.connectable(server,port):
      msg1 = makeJoin(username, password, pubToken)
      resp = pushToServer(server, port, msg1)
      #print(getMSG(resp))
      extractable = ds_protocol.extract_json(resp)
      print(resp)
      print(extractable.message)
      try:
        valid1 = extractable.type == 'ok'
      except:
        valid1 = False
      if valid1:
        tokenn = getToken(resp)
        if message != '':
          msg2 = makePost(makeMSG(message), pubToken)
          print(msg2)
          resp = pushToServer(server, port, msg2)
          extractable = ds_protocol.extract_json(resp)
          print(resp)
          print(extractable.message)
          valid2 = extractable.type == 'ok'
        if bio != None and bio != '' and type(bio) == str and valid2:
          msg3 = newBio(makeMSG(bio), tokenn)
          resp = pushToServer(server, port, msg3)
          extractable = ds_protocol.extract_json(resp)
          print(extractable.message)
          valid3 = extractable.type == 'ok'
      else:
        #print(1)
        return False
      if valid1 and valid2 and valid3:
        #print(2)
        return True
      else:
        #print(3)
        return False
    else:
      print('The server you are trying to access does not work')
      return False


  except:
    #print(5)
    return False

#print(send('168.235.86.101', 301, "andrew568", "123", '', '{"entry": "Hello World!","timestamp": "1603167689.3928561"}'))
#print(send('168.235.86.101', 3021, "dinger", "pissbaby", '{"token":"603ac67d-e6a8-4b81-8eae-bde90f0d105b", "bio": {"entry": "from pyke","timestamp": "1603167689.3928561"}}'))
if __name__ == "__main__":
  testprof = NaClProfile()
  testprof.generate_keypair()
  serv = '168.235.86.101'
  port = 3021
  username = 'bigtester'
  pswd = 'password'
  msg = 'huh'
  bio = 'hi'

  print(send(serv, port, username, pswd, testprof.public_key, msg, bio))