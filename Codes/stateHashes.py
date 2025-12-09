import os
from Crypto.Hash import keccak
import binascii

folder_path = "D:\Adib_code_test\state_hashes" # replace with the path to your folder


def hashFunction(input_string):
    #input_bytes = input_string.encode()
    #keccak256 = keccak.new(data=input_bytes, digest_bits=256).digest()
    keccak256 = keccak.new(data=input_string.encode(), digest_bits=256).digest()
    output_hash = binascii.hexlify(keccak256)
    #print(output_hash)
    return output_hash

# empty list to hold all the state hashes in a single list
state_hashes = []
file_name_counter = 0
# loop through all files in the folder
for filename in os.listdir(folder_path):
    filename = "state"+str(file_name_counter)+"_hash.txt"
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        # process the file
        with open(file_path, 'r') as file:
            # do something with the file contents
            file_contents = file.read()
            #file_contents_list = file_contents.split("\n")
            file_contents_list = file_contents
            #print(filename)
            #print(file_contents_list)
            state_hashes.append(file_contents_list)
            file_name_counter = file_name_counter + 1

print(state_hashes) # This will print all the state hashes with each having 0x at the start: ['0x....', '0x....']
#convert all items of a list to a string
state_hashes_str = ''.join(map(str, state_hashes))

# File write
mRoot_hash_file_path = "D:\Adib_code_test\merkleRoot" # replace with the path to your folder
state_hashes_for_mRoot_filename = mRoot_hash_file_path + "/" + "state_hashes_for_mRoot.txt"
#print(state_hashes_for_mRoot_filename)
with open(state_hashes_for_mRoot_filename, 'w') as fp:
    fp.write("\n".join(str(item) for item in state_hashes))
