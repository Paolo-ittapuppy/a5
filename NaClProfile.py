# NaClProfile.py
# An encrypted version of the Profile class provided by the Profile.py module
# 
# for ICS 32
# by Mark S. Baldwin


# TODO: Install the pynacl library so that the following modules are available
# to your program.
from concurrent.futures import BrokenExecutor
from tkinter.messagebox import RETRY
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box

# TODO: Import the Profile and Post classes
# TODO: Import the NaClDSEncoder module
from NaClDSEncoder import NaClDSEncoder
from Profile import Profile, Post
from pathlib import Path
import json, time, os

class DsuFileError(Exception):
    pass

class DsuProfileError(Exception):
    pass

# TODO: Subclass the Profile class
class NaClProfile(Profile):
    def __init__(self):
        """
        TODO: Complete the initializer method. Your initializer should create the follow three 
        public data attributes:
        """
        super().__init__()
        self.public_key:str
        self.private_key:str
        #always public then private for keypair
        self.keypair:str
        """
        Whether you include them in your parameter list is up to you. Your decision will frame 
        how you expect your class to be used though, so think it through.
        """
        pass

    def generate_keypair(self) -> str:
        """
        Generates a new public encryption key using NaClDSEncoder.

        TODO: Complete the generate_keypair method.

        This method should use the NaClDSEncoder module to generate a new keypair and populate
        the public data attributes created in the initializer.

        :return: str    
        """
        naclObj = NaClDSEncoder()
        naclObj.generate()
        self.public_key = naclObj.private_key
        self.private_key = naclObj.public_key
        #always public then private for keypair
        self.keypair = self.public_key + self.private_key
        self.recieverPublicKey = None
        return self.keypair

    def import_keypair(self, keypair: str):
        """
        Imports an existing keypair. Useful when keeping encryption keys in a location other than the
        dsu file created by this class.

        TODO: Complete the import_keypair method.

        This method should use the keypair parameter to populate the public data attributes created by
        the initializer. 
        
        NOTE: you can determine how to split a keypair by comparing the associated data attributes generated
        by the NaClDSEncoder
        """
        self.keypair = keypair
        if len(keypair) == 88:
            splice = keypair.find('=')
            self.public_key = keypair[:splice + 1]
            self.private_key = keypair[splice + 1:]
        else:
            self.public_key = None
            self.private_key = None
            self.keypair = None

    """
    TODO: Override the add_post method to encrypt post entries.

    Before a post is added to the profile, it should be encrypted. Remember to take advantage of the
    code that is already written in the parent class.

    NOTE: To call the method you are overriding as it exists in the parent class, you can use the built-in super keyword:
    
    super().add_post(...)
    """
    #create a box object with a given pub key string and private key string
    def boxer(self, pubKey:str, privKey:str):
        n = NaClDSEncoder()
        pubKeyObj = n.encode_public_key(pubKey)
        privKeyObj = n.encode_private_key(privKey)
        box = n.create_box(privKeyObj, pubKeyObj)
        return box

    #encrypts a message with a given pubkey and privkey
    def encrypt(self, pubKey:str, privKey:str, msg:str):
        box = self.boxer(pubKey, privKey)
        n = NaClDSEncoder()
        encryptMSG = n.encrypt_message(box, msg)
        return encryptMSG

    #decrypts a message made with the other pair of public and private keys
    def decrypt(self, pubKey:str, privKey:str, msg:str):
        box = self.boxer(pubKey, privKey)
        n = NaClDSEncoder()
        decryptedMSG = n.decrypt_message(box, msg)
        return decryptedMSG

    def add_post(self, post: Post) -> None:
        msg = post.get_entry()
        encryptMSG = self.encrypt(self.recieverPublicKey, self.private_key, msg)
        print(encryptMSG, 'here')
        newPost = Post(encryptMSG, post.get_time())
        print(newPost)
        self._posts.append(newPost)

    """
    TODO: Override the get_posts method to decrypt post entries.

    Since posts will be encrypted when the add_post method is used, you will need to ensure they are 
    decrypted before returning them to the calling code.

    :return: Post
    
    NOTE: To call the method you are overriding as it exists in the parent class you can use the built-in super keyword:
    super().get_posts()
    """

    def get_posts(self) -> list[Post]:
        posts = self._posts
        postList = []
        for post in posts:
            decodedMSG = self.decrypt(self.recieverPublicKey, self.private_key, post.get_entry())
            newPost = Post(decodedMSG, post.get_time())
            postList.append(newPost)
        return postList

    
    """
    TODO: Override the load_profile method to add support for storing a keypair.

    Since the DS Server is now making use of encryption keys rather than username/password attributes, you will 
    need to add support for storing a keypair in a dsu file. The best way to do this is to override the 
    load_profile module and add any new attributes you wish to support.

    NOTE: The Profile class implementation of load_profile contains everything you need to complete this TODO.
     Just copy the code here and add support for your new attributes.
    """

    def load_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                self.keypair = obj['keypair']
                self.recieverPublicKey = obj['recieverPublicKey']
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()

    def encrypt_entry(self, entry:str, public_key:str) -> bytes:
        """
        Used to encrypt messages using a 3rd party public key, such as the one that
        the DS server provides.
        
        TODO: Complete the encrypt_entry method.

        NOTE: A good design approach might be to create private encrypt and decrypt methods that your add_post, 
        get_posts and this method can call.
        
        :return: bytes
        """
        self.recieverPublicKey = public_key
        return self.encrypt(public_key, self.private_key, entry)
        pass
