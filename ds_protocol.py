# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

#  Paolo Andrew Urani
# Uranip@uci.edu
# 24555312


import json
from collections import namedtuple
import socket

# Namedtuple to hold the values retrieved from json messages.

def connectable(server, port):
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
      client.connect((server,port))
      client.sendall('h'.encode('utf-8'))
      resp = client.recv(4096)
      resp = resp.decode('utf-8')
      #print(repr(resp))
      if resp == '{"response": {"type": "error", "message": "Invalid DS Protocol format"}}\r\n':
        return True
      else:
        return False
  except:
    return False

def getValidity(resp):
  obj = json.loads(resp)
  valid = None
  try:
    valid = obj['response']['type']
    return valid == 'ok'
  except:
    return False 

# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple('DataTuple', ['type','message'])
#just get the protocol keys of the responses. 
def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  try:
    json_obj = json.loads(json_msg)
    type = json_obj['response']['type']
    message = json_obj['response']['message']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(type,message)
