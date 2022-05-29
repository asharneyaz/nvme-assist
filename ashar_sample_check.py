import os
from sys import *
import pytsk3
import datetime
import hashlib
from itertools import islice
from tabulate import tabulate
import pyfiglet
from art import *
import pathlib

if platform == "win32":
    os.system('cls')

imagefile = r"C:\Users\Ashar-LabPC\Desktop\a6. DF Ashar's MP NVM_in_USB_Enclosure Image Codes-Pending\3_ashar_code_may2022\ssd_64g_gpt_dd.001"

with open(imagefile,"rb") as f:
    f.read(512)
    a = []
    for _ in range(0,8):
        b = f.read(1)
        b = b.hex()
        a.append(b)
    a= ' '.join(a)
    print("before conversion", a)
    a = bytes.fromhex(a).decode('ascii')
    print("after conversion",a)
    #print(type(a))
    
    if a == "EFI PART":
        print("This image acquired from GPT style storage device")
    else:
        print("This image acquired from MBR style storage device")