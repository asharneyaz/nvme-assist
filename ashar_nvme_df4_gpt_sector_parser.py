#ashar_nvme_df4_gpt_sector_parser.py

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

total_partition_present = 0 #CHECK LINE NO. 63

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

var = "y"

if(len(sys.argv) == 2):
    if(sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "/?"):
        print("****************MANUAL PAGE OF NVMe-Assist****************\n")
        print("Description: Checks and parses GPT partition header. \n")
        print("Help manual for GPT parser: python gpt_sector_parser.py --help or python gpt_sector_parser.py -h or python gpt_sector_parser.py /? \n") 
        print("Usage: python gpt_sector_parser.py")
else:
    while(var == "y" or var=="yes" or var=="Y"):
            if platform == "linux" or platform == "linux2":
                os.system('clear')
                tprint("GPT sector parser \t \n by \t Ashar Neyaz")
                print("This code is running on a Linux Machine")
            elif platform == "darwin":
                os.system('clear')
                tprint("GPT sector parser \t \n by \t Ashar Neyaz")
                print("This code is running on a mac/Apple Machine")
                # OS X
            elif platform == "win32":
                os.system('cls')
                tprint("GPT sector parser \t \n by \t Ashar Neyaz")
                print("This code is running on a Windows Machine")
                # Windows..

            file_path = input(r"Please enter the path of the file: ")
            os.chdir(file_path)
                        
            array = os.listdir(file_path)
            print("The contents of the directory path is listed below: ")
            for count, i in enumerate(os.listdir(file_path)):
                print(count+1,".",i, end='\n')
            
            print("---------------------------------------------------------------------------------------------------------------")
            imagefile = int(input(r"Please choose the physical acquisition image file (.dd/.raw/.img/.001) from the directory listing above: ")) -1
            imagefile = array[imagefile]
            
            print("The file chosen: ", str(imagefile))

            #imagefile = r"D:\dd_gpt_ssd64g.001"
            
            ###### MAKING SURE IF THE IMAGE IS GPT STYLE, IF NOT PRINT THE MESSAGE OF MBR AND EXIT######
            with open(imagefile,"rb") as f:
                f.read(512) 
                
                a = []
                for _ in range(0,8):        #TAKING 8 BYTES HERE
                    b = f.read(1)
                    b = b.hex()
                    a.append(b)
                a= ' '.join(a)
                a = bytes.fromhex(a).decode('ascii')
                
                if a != "EFI PART":
                    sys.exit("This is not a GPT style RAW partition image. Please re-run the program.") 
                else:
                    print("Proceeding with " + str(imagefile) + " file.")

#################################### HEADER PARSING STARTS HERE ####################################

            ###### BYTE RANGE 0-7 SIGNATURE VALUE("EFI PART"): STRING VALUE ######
            with open(imagefile,"rb") as f:
                f.read(512) 
                #print(f.read(512))
                
                a = []
                for _ in range(0,8):        #TAKING 8 BYTES HERE
                    b = f.read(1)
                    b = b.hex()
                    a.append(b)
                a= ' '.join(a)
                #print("before conversion", a)
                a = bytes.fromhex(a).decode('ascii')
                #print("after conversion",a)
                #print(type(a))
                
                if a == "EFI PART":
                    print("Information:" + str(imagefile) + " acquired from GPT style storage device.")
                else:
                    print("Information:" + str(imagefile) + " acquired from MBR style storage device.")
                    
            ############### FOR THE PURPOSE OF COUNTING PARTITIONS ##############################
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
            #print(tabulate(data,headers = ["Address","Description","Start Sector #", "End Sector #", "Length of Partition MB", "Start Byte offset (dec)", "End Byte Offset (dec)"],floatfmt=".9f"))
            print("--------------------------------------Counting Total Number of Partitions--------------------------------------")
            print("Total partitions in " + str(imagefile) + ": " + str(int(address)-4))
            total_partition_present = int(address)-4
            ##########################################################################################

            #print("---------------------------------------------------------------------------------------------------------------")
            print("---------------------------------------------------GPT HEADER--------------------------------------------------")
            ###### BYTE RANGE 8-11 GPT REVISION VERSION: STRING VALUE ######
            with open(imagefile,"rb") as f:
                f.read(520) 
                
                a = []
                for _ in range(0,4):        #TAKING 4 BYTES HERE
                    b = f.read(1)
                    b = b.hex()
                    a.append(b)
                a= ' '.join(a)
                #print("before conversion", a)
                a = bytes.fromhex(a).decode('ascii')
                #print("after conversion",a)
                
                if a == "\x00\x00\x01\x00":
                    print("GPT version: \t \t \t \t \t \t Revision 1.0 for UEFI 2.8.")
                else:
                    print("This is not a GPT style partition.")
                    
            ###### BYTE RANGE 12-15 SIZE OF GPT HEADER IN BYTES: INTEGER VALUE ######
            with open(imagefile,"rb") as f:
                f.read(524) #from byte no. 524 to byte no. 527 
                
                a = []
                for _ in range(0,4):        #TAKING 4 BYTES HERE
                    b = f.read(1)
                    b = b.hex()
                    a.append(b)
                a= ''.join(a)
                #print("Information: LE for Size of GPT Header in bytes: ", a)
              
                ###CALLING BIG ENDING FUNCTION FROM THE TOP IN THE below statements.###
            
                #print("Information: BE for Size of GPT Header in bytes: ", to_big_endian(a))
                print("Size of GPT Header: \t \t \t \t \t", int(to_big_endian(a),16), "bytes")                
                #print("Int values: ", int(a,16))
                #a = bytes.fromhex(a).decode('ascii')
                #print(a) #STRING TYPE
                
                #a = bytearray.fromhex(a)
                #a.reverse()
                #print("reversed string", a)
                
                #a = bytes.fromhex(a).decode('ascii')
                #print("after conversion",a)
                
            ###### BYTE RANGE 16-19 CRC CHECKSUM OF GPT HEADER: STRING VALUE ######
            with open(imagefile,"rb") as f:
                f.read(528)
                
                a = []
                for _ in range(0,4):        #TAKING 4 BYTES HERE
                    b = f.read(1)
                    b = b.hex()
                    a.append(b)
                a= ''.join(a)
                print("CRC32 Checksum of GPT Header: \t \t \t \t",a.upper())

                '''
                a = bytes.fromhex(a).decode('ascii')
                print("Information: CRC Checksum of GPT Header: ", str(a))
                '''
            ###### BYTE RANGE 20-23 RESERVED: NO NEED TO CALCULATE IT ######
            
            ###### BYTE RANGE 24-31 LBA OF CURRENT GPT HEADER STRUCTURE: INTEGER VALUE ######
            with open(imagefile,"rb") as f:
                f.read(536) 
                
                a = []
                for _ in range(0,8):        #TAKING 8 BYTES HERE
                    b = f.read(1)
                    b = b.hex()
                    a.append(b)
                a= ''.join(a)
                
                #print("Information: BE for Current GPT Header Structure: ", to_big_endian(a))
                print("SECTOR OF GPT Header Structure: \t \t \t", int(to_big_endian(a),16))

            ###### BYTE RANGE 32-39 LBA OF BACKUP GPT HEADER STRUCTURE: INTEGER VALUE ######
            with open(imagefile,"rb") as f:
                f.read(544) 
                
                a = []
                for _ in range(0,8):        #TAKING 8 BYTES HERE
                    b = f.read(1)
                    b = b.hex()
                    a.append(b)
                a= ''.join(a)
                
                #print("Information: BE for BACKUP GPT Header Structure: ", to_big_endian(a))
                print("SECTOR OF BACKUP GPT Header Structure: \t \t \t", int(to_big_endian(a),16))

            ###### BYTE RANGE 40-47 LBA OF START OF PARTITION AREA: INTEGER VALUE ######
            with open(imagefile,"rb") as f:
                f.read(552) 
                
                a = []
                for _ in range(0,8):        #TAKING 8 BYTES HERE
                    b = f.read(1)
                    b = b.hex()
                    a.append(b)
                a= ''.join(a)
                
                #print("Information: BE for LBA OF START OF PARTITION AREA: ", to_big_endian(a))
                print("SECTOR OF LBA OF START OF PARTITION AREA: \t \t", int(to_big_endian(a),16))
            
            ###### BYTE RANGE 48-55 LBA OF END OF PARTITION AREA: INTEGER VALUE ######
            with open(imagefile,"rb") as f:
                f.read(560) 
                
                a = []
                for _ in range(0,8):        #TAKING 8 BYTES HERE
                    b = f.read(1)
                    b = b.hex()
                    a.append(b)
                a= ''.join(a)
                
                #print("Information: BE for LBA OF END OF PARTITION AREA: ", to_big_endian(a))
                print("SECTOR OF LBA OF END OF PARTITION AREA: \t \t", int(to_big_endian(a),16))
                
            ###### BYTE RANGE 56-71 DISK GUID: STRING VALUE ######
            with open(imagefile,"rb") as f:
                f.read(568)
                
                a = []
                for _ in range(0,16):        #TAKING 16 BYTES HERE
                    b = f.read(1)
                    b = b.hex()
                    a.append(b)
                a= ''.join(a)
                print("DISK Globally Unique Identifier (GUID): \t \t",a.upper())
            
            ###### BYTE RANGE 72-79 LBA OF START OF THE PARTITION TABLE: INTEGER VALUE ######
            with open(imagefile,"rb") as f:
                f.read(584) 
                
                a = []
                for _ in range(0,8):        #TAKING 8 BYTES HERE
                    b = f.read(1)
                    b = b.hex()
                    a.append(b)
                a= ''.join(a)
                
                #print("Information: BE for LBA OF START OF THE PARTITION TABLE: ", to_big_endian(a))
                print("SECTOR OF LBA OF START OF THE PARTITION TABLE: \t \t", int(to_big_endian(a),16))
            
            ###### BYTE RANGE 80-83 NUMBER OF ENTRIES IN THE PARTITION TABLE: INTEGER VALUE ######
            with open(imagefile,"rb") as f:
                f.read(592) 
                
                a = []
                for _ in range(0,4):        #TAKING 4 BYTES HERE
                    b = f.read(1)
                    b = b.hex()
                    a.append(b)
                a= ''.join(a)
                
                #print("Information: BE for NUMBER OF ENTRIES IN THE PARTITION TABLE: ", to_big_endian(a))
                print("NUMBER OF ENTRIES IN THE PARTITION TABLE: \t \t", int(to_big_endian(a),16))
                
            ###### BYTE RANGE 84-87 SIZE OF EACH ENTRY IN THE PARTITION TABLE: INTEGER VALUE ######
            with open(imagefile,"rb") as f:
                f.read(596) 
                
                a = []
                for _ in range(0,4):        #TAKING 4 BYTES HERE
                    b = f.read(1)
                    b = b.hex()
                    a.append(b)
                a= ''.join(a)
                
                #print("Information: BE for SIZE OF EACH ENTRY IN THE PARTITION TABLE: ", to_big_endian(a))
                print("SIZE OF EACH ENTRY IN THE PARTITION TABLE: \t \t", int(to_big_endian(a),16), "bytes")
                
            ###### BYTE RANGE 88-91 CRC32 OF THE PARTITION TABLE: STRING VALUE ######
            with open(imagefile,"rb") as f:
                f.read(600)
                
                a = []
                for _ in range(0,4):        #TAKING 4 BYTES HERE
                    b = f.read(1)
                    b = b.hex()
                    a.append(b)
                a= ''.join(a)
                print("CRC32 Checksum of partition table: \t \t \t",a.upper())
            
            #print("---------------------------------------------------------------------------------------------------------------")
            
            #os.system("python ashar_nvme_df5_gpt_partition_parser.py " + str(imagefile))
            
            if(total_partition_present ==1):
                os.system("python ashar_nvme_df5_gpt_partition_parser1.py " + str(imagefile))
                print("---------------------------------------------------------------------------------------------------------------")
                var = input("Do you want to continue checking (Y or N):")
                var = var.lower()
                if(var !="y"):
                    print("Thank you for using GPT Sector Parser of NVMe-Assist toolkit. Good Bye!")
            
            elif(total_partition_present ==2):
                os.system("python ashar_nvme_df5_gpt_partition_parser1.py " + str(imagefile))
                os.system("python ashar_nvme_df5_gpt_partition_parser2.py " + str(imagefile))
                print("---------------------------------------------------------------------------------------------------------------")
                var = input("Do you want to continue checking (Y or N):")
                var = var.lower()
                if(var !="y"):
                    print("Thank you for using GPT Sector Parser of NVMe-Assist toolkit. Good Bye!")
                    
            elif(total_partition_present ==3):
                os.system("python ashar_nvme_df5_gpt_partition_parser1.py " + str(imagefile))
                os.system("python ashar_nvme_df5_gpt_partition_parser2.py " + str(imagefile))
                os.system("python ashar_nvme_df5_gpt_partition_parser3.py " + str(imagefile))
                print("---------------------------------------------------------------------------------------------------------------")
                var = input("Do you want to continue checking (Y or N):")
                var = var.lower()
                if(var !="y"):
                    print("Thank you for using GPT Sector Parser of NVMe-Assist toolkit. Good Bye!")
            
            elif(total_partition_present ==4):
                os.system("python ashar_nvme_df5_gpt_partition_parser1.py " + str(imagefile))
                os.system("python ashar_nvme_df5_gpt_partition_parser2.py " + str(imagefile))
                os.system("python ashar_nvme_df5_gpt_partition_parser3.py " + str(imagefile))
                os.system("python ashar_nvme_df5_gpt_partition_parser4.py " + str(imagefile))
                print("---------------------------------------------------------------------------------------------------------------")
                var = input("Do you want to continue checking (Y or N):")
                var = var.lower()
                if(var !="y"):
                    print("Thank you for using GPT Sector Parser of NVMe-Assist toolkit. Good Bye!")
            elif(total_partition_present ==5):
                os.system("python ashar_nvme_df5_gpt_partition_parser1.py " + str(imagefile))
                os.system("python ashar_nvme_df5_gpt_partition_parser2.py " + str(imagefile))
                os.system("python ashar_nvme_df5_gpt_partition_parser3.py " + str(imagefile))
                os.system("python ashar_nvme_df5_gpt_partition_parser4.py " + str(imagefile))
                os.system("python ashar_nvme_df5_gpt_partition_parser5.py " + str(imagefile))
                print("---------------------------------------------------------------------------------------------------------------")
                var = input("Do you want to continue checking (Y or N):")
                var = var.lower()
                if(var !="y"):
                    print("Thank you for using GPT Sector Parser of NVMe-Assist toolkit. Good Bye!")
            else:
                print("---------------------------------------------------------------------------------------------------------------")
                var = input("Do you want to continue checking (Y or N):")
                var = var.lower()
            
                if(var !="y"):
                    print("Thank you for using GPT Sector Parser of NVMe-Assist toolkit. Good Bye!")
            
            
            
            
            




            '''
            #THIS COMMENTED PORTION IS WRITTEN AGAIN IN ashar_nvme_df5_gpt_part_parser.py FILE FOR CLARITY
            
            print("-----------------------------------------------GPT PARTITION TABLE---------------------------------------------")
            
            #################################### GPT PARSING STARTS HERE ####################################
            
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
                for _ in range(0,64):        #TAKING 4 BYTES HERE
                    b = f.read(1)
                    b = b.hex()
                    a.append(b)
                a= ' '.join(a)
                a = bytes.fromhex(a).decode('ascii')
                print("Partition name in Unicode: \t \t \t \t",a)
            
            print("---------------------------------------------------------------------------------------------------------------")
            var = input("Do you want to continue checking (Y or N):")
            var = var.lower()
            
            if(var !="y"):
                print("Thank you for using GPT Sector Parser of NVMe-Assist toolkit. Good Bye!")
            '''