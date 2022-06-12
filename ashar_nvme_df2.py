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

imagefile = sys.argv[1]

if platform == "win32":
    creation_time = os.path.getctime(imagefile)
    date_created = datetime.datetime.fromtimestamp(creation_time)
    print("The creation time of ", str(imagefile), " file:", date_created)

    modified_time = os.path.getmtime(imagefile)
    date_modified = datetime.datetime.fromtimestamp(modified_time)
    print("The modification time of ", str(imagefile), " file:", date_modified)
    
elif platform == "linux" or platform == "linux2" or platform == "darwin":
    creation_time = imagefile.stat().st_ctime
    date_created = datetime.datetime.fromtimestamp(creation_time)
    print("The creation time of ", str(imagefile), " file:", date_created)

    modified_time = imagefile.stat().st_mtime
    date_modified = datetime.datetime.fromtimestamp(modified_time)
    print("The modification time of ", str(imagefile), " file:", date_modified, "\n")
    
#imagefile = r"C:\Users\Ashar-LabPC\Desktop\a6. DF Ashar's MP NVM_in_USB_Enclosure Image Codes-Pending\3_ashar_code_may2022\image_03_one.dd"

def calculate_md5_hash(imagefile):
    hash_function1 = None
    hash_function1 = hashlib.md5()
        
    with open(imagefile,"rb") as f:
        chunk = 0
        while chunk != b'':
            chunk = f.read(1024)
            hash_function1.update(chunk)
    computed_hash1 = hash_function1.hexdigest()
    return computed_hash1

def calculate_sha1_hash(imagefile):
    hash_function2 = None
    hash_function2 = hashlib.sha1()
            
    with open(imagefile,"rb") as f:
        chunk = 0
        while chunk != b'':
            chunk = f.read(1024)
            hash_function2.update(chunk)
    computed_hash2 = hash_function2.hexdigest()
    return computed_hash2

with open(imagefile,"rb") as f:
    f.read(512)   #we did 512 because python takes decimal offset and not hex offset
    hex_list = []
    for _ in range(0,8):
        taking_single_hex_values = f.read(1)
        taking_single_hex_values = taking_single_hex_values.hex()
        hex_list.append(taking_single_hex_values)
    hex_list = ' '.join(hex_list)
    hex_list = bytes.fromhex(hex_list).decode('ascii')
    #print(hex_list)
    #print(type(hex_list))
    
    if hex_list == "EFI PART":
        print("Partition scheme for image acquired: GPT")
    else:
        print("Partition scheme for image acquired: MBR")

print("PARTITION TABLE IS PRINTED BELOW")
print("----------------------------------------------------------------------------------------------------------------------------------------------","\n")

imagehandle = pytsk3.Img_Info(imagefile)
partitionTable = pytsk3.Volume_Info(imagehandle)

data = []

for partition in partitionTable:
    #print(type(partition.desc))
    address = partition.addr
    
    description = partition.desc
    
    sector_num = (partition.start, (partition.len + partition.start - 1))
    
    partition_length = (((partition.len*512)/1024)/1024)

    byte_offset_dec = ((partition.start*512),((partition.len + partition.start - 1)*512))

    data.append(
        [
            address,
            description,
            sector_num[0],
            sector_num[1],
            partition_length,
            byte_offset_dec[0],
            byte_offset_dec[1]
        ]
    )

print(tabulate(data,headers = ["Address","Description","Start Sector #", "End Sector #", "Length of Partition MB", "Start Byte offset (dec)", "End Byte Offset (dec)"],floatfmt=".9f"))

print("----------------------------------------------------------------------------------------------------------------------------------------------")
    
    #print(partition.addr, partition.desc, "| start sector no.: %s | end sector no. : %s |" % (partition.start, partition.len + partition.start - 1), " length of partition->", ((partition.len*512)/1024)/1024, "MB", "| start byte offset in decimal : %s | end byte offset in decimal : %s -->" % (partition.start*512, (partition.len + partition.start - 1)*512), "\n")

#print("----------------------------------------------------------------------------------------------------------------------------------------------")
print("Calculating HASHES now, this depends on the size of the file. Please wait.")
print("The calculated MD5 hash: ", calculate_md5_hash(imagefile))
print("The calculated SHA1 hash: ", calculate_sha1_hash(imagefile))       