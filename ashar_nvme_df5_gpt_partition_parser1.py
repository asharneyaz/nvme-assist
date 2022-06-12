#ashar_nvme_df5_gpt_partition_parser1.py

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

sector_jumper = 0
e1_part_type = 1024
e2_part_guid = 1040
e3_part_st_lba = 1056
e4_part_en_lba = 1064
e5_part_attrib = 1072
e5_part_name = 1080

def to_big_endian(le_string):
    big_hex = bytearray.fromhex(le_string)
    big_hex.reverse()
    #print("Byte array format: ", big_hex)
    str_big = ''.join(format(x,'02x') for x in big_hex)
    return str_big

def to_lil_endian(be_string):
    le_hex = bytearray.fromhex(be_string)
    le_hex.reverse()
    #print("Byte array format: ", le_hex)
    str_lil = ''.join(format(x,'02x') for x in le_hex)
    return str_lil

imagefile = sys.argv[1]


print("-----------------------------------------------GPT PARTITION TABLE---------------------------------------------")
print("---------------------------------------------1st GPT PARTITION ENTRY------------------------------------------")
# 1 ################################### GPT PARSING STARTS HERE FOR MICROSOFT RESERVED PARTITIION####################################

###### BYTE RANGE 0-15 PARTITION TYPE GUID: STRING VALUE ######
with open(imagefile,"rb") as f:
    f.read(1024) 
    
    a = []
    for _ in range(0,16):        #TAKING 16 BYTES HERE
        b = f.read(1)
        b = b.hex()
        a.append(b)
    a= ''.join(a)
    print("Partition Type GUID: \t \t \t \t \t", a)
 
###### BYTE RANGE 16-31 UNIQUE PARTITION GUID: STRING VALUE ######
with open(imagefile,"rb") as f:
    f.read(1040) 
    
    a = []
    for _ in range(0,16):        #TAKING 16 BYTES HERE
        b = f.read(1)
        b = b.hex()
        a.append(b)
    a= ''.join(a)
    print("Unique Partition GUID: \t \t \t \t \t", a)

###### BYTE RANGE 32-39 STARTING LBA OF PARTITION: INTEGER VALUE ######
with open(imagefile,"rb") as f:
    f.read(1056) 
    
    a = []
    for _ in range(0,8):        #TAKING 8 BYTES HERE
        b = f.read(1)
        b = b.hex()
        a.append(b)
    a= ''.join(a)
    print("Starting LBA SECTOR of the Partition: \t \t \t", int(to_big_endian(a),16))
    sector_jumper = int(to_big_endian(a),16) * 512 
    
    with open(imagefile, "rb") as f:
        f.read(sector_jumper)
        data_jump_int = f.read(3)
        
        a = []
        for _ in range(0,8):        #TAKING 8 BYTES HERE
            b = f.read(1)
            b = b.hex()
            a.append(b)
        a= ''.join(a)
        #print(a.upper())
        #print(type(a))
        
        if(a.upper() == "4E54465320202020"):
            print("**********This Basic Partition Type is NTFS File System.")
        elif(a.upper() == "4D5357494E342E31" or a.upper() == "4D53444F53352E30"):
            print("**********This Basic Partition Type is FAT File System.")
        else:
            print("**********Microsoft Reserved Partition.")
        
        #data_oem = f.read(8) # read 3 characters at a time, while f.read() means read all characters at once.
        #data_oem = data_oem.decode("utf-8") #utf-8
        #print("**********OEM ID of the partition: ", data_oem)
        
        #if(data_oem == "\x4E\x54\x46\x53\x20\x20\x20\x20"):
        #    print("**********This Basic Partition Type is NTFS.")
            
        #elif(data_oem == "\x4D\x53\x57\x49\x4E\x34\x2E\x31"):
        #    print("**********This Basic Partition Type is FAT-16.")
        
        #elif(data_oem == "\x4D\x53\x44\x4F\x53\x35\x2E\x30"):
        #    print("**********This Basic Partition Type is FAT-32.")
        #else:
        #    print("**********Microsoft Reserved Partition.")

###### BYTE RANGE 40-47 ENDING LBA OF PARTITION: INTEGER VALUE ######
with open(imagefile,"rb") as f:
    f.read(1064) 
    
    a = []
    for _ in range(0,8):        #TAKING 8 BYTES HERE
        b = f.read(1)
        b = b.hex()
        a.append(b)
    a= ''.join(a)
    print("Ending LBA SECTOR of the Partition: \t \t \t", int(to_big_endian(a),16)) 

###### BYTE RANGE 48-55 PARTITION ATTRIBUTES: NO NEED TO CALCULATE IT ######

###### BYTE RANGE 56-127 GPT REVISION VERSION: STRING VALUE ######
with open(imagefile,"rb") as f:
    f.read(1080) 
    
    a = []
    for _ in range(0,64):        #TAKING 64 BYTES HERE
        b = f.read(1)
        b = b.hex()
        a.append(b)
    a= ' '.join(a)
    a = bytes.fromhex(a).decode('ascii')
    #print("Partition name in Unicode: \t \t \t \t",a)
    
    #CHECKING FOR THE PRESENCE FOR MORE PARTITIONS
    with open(imagefile, "rb") as f:
        f.read(1152)
        
        a = []
        for _ in range(0,8):        #TAKING 8 BYTES HERE
            b = f.read(1)
            b = b.hex()
            a.append(b)
        a= ''.join(a)
        
        #if(a == "\x00\x00\x00\x00\x00\x00\x00\x00"):
        if(a == "0000000000000000"):
            sys.exit("No other partition exists.")   
        else:
            #print("There are more partitions present.")
            print("---------------------------------------------2nd GPT PARTITION ENTRY------------------------------------------")   
            
            # 2 ################################### GPT PARSING STARTS HERE FOR THE SECOND PARTITION####################################