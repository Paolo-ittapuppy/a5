# NaClDSEncoder.py
# 
# ICS 32 
#
# v0.3
# 
# The following module is designed to abstract the encoding procedures required
# when using the NaCl library. By default, NaCl works with bytes, but bytes are
# not very human friendly. So to make keypairs a little easier to work with, this 
# module will handle the generation of keys and encoding of keys into the 
# PublicKey and PrivateKey objects required by NaCl encryption functions.

import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box

class NaClDSEncoder:
    def generate(self):
        """
        The generate method handles the creation of a private and public keys. These keys
        are also combined to form a keypair. Call this function when your program needs to 
        generate new keys.
        """
        # call the key generator function from the nacl library.
        raw = PrivateKey.generate()
        # the raw keypair, stored as PrivateKey.
        self.raw_keypair = raw
        # the private key, encoded from bytes to string
        self.private_key = raw.encode(encoder=nacl.encoding.Base64Encoder).decode(encoding = 'UTF-8')
        # the public key, encoded from bytes to string
        self.public_key = raw.public_key.encode(encoder=nacl.encoding.Base64Encoder).decode(encoding = 'UTF-8')
        # the keypair, useful for storage, but primarily a convenience attribute
        # that simply concatenates the public and private keys and stores them as a string.
        self.keypair = self.public_key + self.private_key
    
    def encode_public_key(self, public_key:str) -> PublicKey:
        """
        encode_public_key takes an public_key string as a parameter and generates
        a PublicKey object.
        """
        return PublicKey(public_key, nacl.encoding.Base64Encoder)
    
    def encode_private_key(self, private_key:str) -> PrivateKey:
        """
        encode_private_key takes an private_key string as a parameter and generates
        a PrivateKey object.
        """
        return PrivateKey(private_key, nacl.encoding.Base64Encoder)
    
    def create_box(self, encoded_private_key:PrivateKey, encoded_public_key:PublicKey) -> Box:
        """
        A Box object enables messages to be encrypted and decrypted.

        creates an encryption Box using PrivateKey and PublicKey objects. Key types can be 
        created using the encode_private_key and encode_public_key methods.

        Example usage:
        dsenc = NaClDSEncoder()
        box = dsenc.create_box(dsenc.encode_private_key("YOUR PRIVATE KEY"), dsenc.encode_public_key("YOUR PUB KEY"))
        """
        return Box(encoded_private_key, encoded_public_key)
    
    def encrypt_message(self, box:Box, message:str) -> str:
        """
        encrypts a message using a Base64Encoder and UTF-8 encoding

        :param box: the encryption box to use for encrypting. A box can be generated using the create_box method.
        :param message: the message to be encrypted

        :returns: an encrypted message in bytes
        """
        
        #first convert the message to bytes
        bmsg = message.encode(encoding='UTF-8')
        # encrypt message
        encrypted_msg = box.encrypt(bmsg, encoder=nacl.encoding.Base64Encoder)
        # convert back to str
        msg = encrypted_msg.decode(encoding='UTF-8')

        return msg
    
    def decrypt_message(self, box:Box, message:str) -> str:
        """
        encrypts a message using a Base64Encoder and UTF-8 encoding

        :param box: the encryption box to use for decrypting. A box can be generated using the create_box method.
        :param message: the message to be decrypted

        :returns: a decrypted message of type str
        """
        
        #first conver the message to bytes
        bmsg = message.encode(encoding='UTF-8')
        decrypted_msg = box.decrypt(bmsg, encoder=nacl.encoding.Base64Encoder)
        # convert back to str
        msg = decrypted_msg.decode(encoding='UTF-8')

        return msg

'''
naclObj = NaClDSEncoder()
naclObj.generate()
print(naclObj.public_key)
print(naclObj.private_key)
print(naclObj.keypair)
''' #findings: the keys end in equals so i can splice a keypair by the first instance of an equal sign
