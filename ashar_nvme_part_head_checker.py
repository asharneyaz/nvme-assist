import os
import sys
from sys import *
import pytsk3
import pyewf
import datetime
import hashlib
from itertools import islice
from tabulate import tabulate
import pyfiglet
from art import *
import pathlib

#ASCII ONLY WORKS ON INTEGERS.
var = "y"
while(var == "y" or var=="yes" or var=="Y"):
    file_path = input(r"Please enter the path of the file: ")
    os.chdir(file_path)

    array = os.listdir(file_path)
    print("The contents of the directory path is listed below: ")
    for count, i in enumerate(os.listdir(file_path)):
        print(count+1,".",i, end='\n')

    imagefile = int(input(r"Please choose the file to check for logical acquisition image: ")) -1
    imagefile = array[imagefile]
    print("The file chosen: ", str(imagefile))

    #os.system('cls')
    with open(imagefile, "rb") as f:
        data_jump_int = f.read(3)
        data_oem = f.read(8) # read 3 characters at a time, while f.read() means read all characters at once.
        data_oem = data_oem.decode("utf-8")
        print(data_oem)

        if(data_oem == "\x4E\x54\x46\x53\x20\x20\x20\x20"):
            print("This is a stand-alone NTFS logical image")
            
        if(data_oem == "\x4D\x53\x57\x49\x4E\x34\x2E\x31"):
            print("This is a stand-alone FAT-16 logical image")
        
        if(data_oem == "\x4D\x53\x44\x4F\x53\x35\x2E\x30"):
            print("This is a stand-alone FAT-32 logical image")
    
    var = input("Do you want to continue checking (Y or N):")
    var = var.lower()
    
    

