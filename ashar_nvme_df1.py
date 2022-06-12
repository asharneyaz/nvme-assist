#!/usr/bin/python

import os
from sys import *
import sys
import pytsk3
import datetime
import hashlib
from itertools import islice
from tabulate import tabulate
import pyfiglet
from art import *
import pathlib
from simple_colors import *


var = "y"

if(len(sys.argv) == 2):
    if(sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "/?"):
        print("****************MANUAL PAGE OF NVMe-Assist****************\n")
        print("Description: Display the partition layout of a volume system (partition tables), list of files in a directory, MD5, SHA-1, and timestamps of the forensic image file \n")
        print("Help manual for MBR stype partitions: python nvme_df.py --help or python nvme_df.py -h or python nvme_df.py /? \n") 
        print("Help manual for GPT stype partitions: python nvme_dfe01.py --help or python nvme_dfe01.py -h or python nvme_dfe01.py /? \n") 
        print("Usage: python nvme_df.py or python nvme_dfe01.py")
else:
          #  print("usage: python ashar_nvme_df.py for program execution")
          #  print("usage: python ashar_nvme_df.py for program execution")

    while(var == "y" or var=="yes" or var=="Y"):
            if platform == "linux" or platform == "linux2":
                os.system('clear')
                tprint("NVMe-Assist Toolkit \t \n by \t Ashar Neyaz")
                print("This code is running on a Linux Machine")
            elif platform == "darwin":
                os.system('clear')
                tprint("NVMe-Assist Toolkit \t \n by \t Ashar Neyaz")
                print("This code is running on a mac/Apple Machine")
                # OS X
            elif platform == "win32":
                os.system('cls')
                tprint("NVMe-Assist Toolkit \t \n by \t Ashar Neyaz")
                print("This code is running on a Windows Machine")
                # Windows..

            file_path = input(r"Please enter the path of the file: ")
            os.chdir(file_path)
            
            array = os.listdir(file_path)
            print("The contents of the directory path is listed below: ")
            for count, i in enumerate(os.listdir(file_path)):
                print(count+1,".",i, end='\n')

            imagefile = int(input(r"Please choose the physical acquisition image file (.dd/.raw/.img/.001/.e01) from the directory listing above: ")) -1
            imagefile = array[imagefile]
            print("The file chosen: ", str(imagefile))
           
            if(str(imagefile).endswith(".raw") or str(imagefile).endswith(".001") or str(imagefile).endswith(".img") or str(imagefile).endswith(".dd") or str(imagefile).endswith(".RAW") or str(imagefile).endswith(".IMG") or str(imagefile).endswith(".DD")):
                os.system("python ashar_nvme_df2.py " + str(imagefile))
            else:
                os.system("python ashar_nvme_df3.py " + str(imagefile))
                
            var = input("Do you want to continue checking (Y or N):")
            var = var.lower()
            
            if(var !="y"):
                print("Thank you for using NVMe-Assist. Good Bye!")
