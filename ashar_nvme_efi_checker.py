import os
import hashlib

#ASCII ONLY WORKS ON INTEGERS.

os.system('cls')
with open("gpt_header_sample", "rb") as f:
    data_efi = f.read(8) # read 3 characters at a time, while f.read() means read all characters at once.
    data_efi = data_efi.decode("utf-8")
    print(data_efi)

    data_bdp = f.read(176) # skipping 176 bytes
    data_bdp = f.read(39) #then reading 39 bytes 
    data_bdp = data_bdp.decode("utf-8")
    print(data_bdp)

    data_nt = f.read(68)
    data_nt = f.read(4)
    data_nt = data_nt.decode("utf-8")
    print(data_nt)

    if( (data_bdp == "\x42\x00\x61\x00\x73\x00\x69\x00\x63\x00\x20\x00\x64\x00\x61\x00\x74\x00\x61\x00\x20\x00\x70\x00\x61\x00\x72\x00\x74\x00\x69\x00\x74\x00\x69\x00\x6F\x00\x6E") and (data_nt == "\x4E\x54\x46\x53")):
        print("There is an NTFS Partition present.")
    else:
        print("There isn't any NTFS Partition present.")