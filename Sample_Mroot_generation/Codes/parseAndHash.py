import os
from Crypto.Hash import keccak
import binascii

folder_path = "D:\Arb_code_test\input1" # replace with the path to your folder


def hashFunction(input_string):

    input_bytes = input_string.encode()

    keccak256 = keccak.new(data= input_bytes, digest_bits=256).digest()
    output_hash = binascii.hexlify(keccak256)

    # print(output_hash)

    return output_hash.hex()

    
    # hash_object = keccak.new(digest_bits=256)
    # hash_object.update(input_bytes)
    # digest = hash_object.digest()
    # print(digest)

def writeToFile(output_filename, output_string):
    with open(output_filename, 'w') as f:
        f.write(output_string)

# loop through all files in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        # process the file
        with open(file_path, 'r') as file:
            # do something with the file contents
            file_contents = file.read()

            file_contents_list = file_contents.split("\n")
            print(file_contents_list)
            split_index = file_contents_list.index("")

            instruction_set = file_contents_list[:split_index]
            print("Instruction set: ", instruction_set)
            data_set = file_contents_list[split_index+1:]
            print("Data set: ", data_set)

            instruction_set_hash = dict()
            data_set_hash = dict()

        # if (filename == "state2.txt"):
            print(filename)
            print()
            # instruction_set_hash["H"+str(len(instruction_set))] = "H(None)"
            instruction_set_hash["H"+str(len(instruction_set))] = hashFunction("None")

            output_is_ds_string = ""

            for i in range(len(instruction_set)-1, -1, -1):
                # print(instruction_set[i], i)
                key = "H"+str(i)

                # print(i)
                if(len(instruction_set) == 2 and instruction_set[len(instruction_set)-1] == "STOP"):
                    key = "IS"
                    instruction_set_hash[key] = hashFunction("STOP" + instruction_set_hash["H"+str(i+1)])
                    instruction_set_hash.pop("H"+str(i+1))
                    

                    break
                else:
                    if (i == len(instruction_set)-1):
                        # instruction_set_hash[key] =  instruction_set[i] 
                        instruction_set_hash[key] =  hashFunction(instruction_set[i])
                        continue

                    if (i == len(instruction_set)-2):
                        # instruction_set_hash[key] =  "H (" + instruction_set[i+1] + " || " + instruction_set_hash["H"+str(i+2)] + ")"
                        instruction_set_hash[key] =  hashFunction(instruction_set[i+1] + instruction_set_hash["H"+str(i+2)] ) 
                        continue

                    if (i != 0):
                        # instruction_set_hash[key] = "H (" + instruction_set[i+1] + " || " + instruction_set_hash["H"+str(i+1)] + ")"
                        instruction_set_hash[key] = hashFunction(instruction_set[i+1] +  instruction_set_hash["H"+str(i+1)] ) 
                    else:
                        key = "IS"
                        # instruction_set_hash[key] =   "H (" + instruction_set[i+1] + " || " + instruction_set_hash["H"+str(i+1)]
                        instruction_set_hash[key] =   hashFunction(instruction_set[i+1]  + instruction_set_hash["H"+str(i+1)])  

            for key,value in instruction_set_hash.items():
                print(key,value)

                output_is_ds_string = output_is_ds_string + key + " = " + value + "\n"
            print()

            for i in range(len(data_set)-1, -1, -1):
                if (data_set[len(data_set)-1] == "None") and len(data_set) == 2:
                    key = "DS"
                    # data_set_hash[key] = "H(None)"
                    data_set_hash[key] = hashFunction("None")
                else:
                    key = "DH"+str(i)
                    if (i == len(data_set)-1):
                        # data_set_hash[key] = "H(None)"
                        data_set_hash[key] =  hashFunction("None")
                        continue

                    if (i != 0):
                        # data_set_hash[key] = "H (" + data_set[i+1] + " || " + data_set_hash["DH"+str(i+1)] + ")"
                        data_set_hash[key] =  hashFunction(data_set[i+1] + data_set_hash["DH"+str(i+1)])  
                    else:
                        key = "DS"
                        # data_set_hash[key] =   "H (" + data_set[i+1] + " || " + data_set_hash["DH"+str(i+1)] + ")"
                        data_set_hash[key] =  hashFunction(data_set[i+1] +  data_set_hash["DH"+str(i+1)] ) 

            
            for key,value in data_set_hash.items():
                print(key,value)
                output_is_ds_string = output_is_ds_string + key + " = " + value + "\n"

            IS_DS = instruction_set_hash["IS"] + data_set_hash["DS"]
            IS_DS_hash = hashFunction(IS_DS)

            print()

            IS_DS_hash_output = "0x"+ IS_DS_hash

            print("IS_DS_hash", IS_DS_hash_output)
            print()


            output_file_path = "D:\Adib_code_test\output1"
            filenameSplitList = filename.split(".txt")
            output_is_ds_output_file_name = output_file_path+"/" +filenameSplitList[0]+"_is_ds.txt"
            print(output_is_ds_output_file_name)

            writeToFile(output_is_ds_output_file_name, output_is_ds_string )


            output_is_ds_hash_filename = output_file_path+"/" +filenameSplitList[0]+"_hash.txt"
            print(output_is_ds_hash_filename)
            writeToFile(output_is_ds_hash_filename, IS_DS_hash_output)



                        
                







