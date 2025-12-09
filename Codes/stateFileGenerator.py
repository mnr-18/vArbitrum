import os
from Crypto.Hash import keccak
import binascii

folder_path = "D:\Arb_code_test\input_files"  # replace with the path to your folder


def hashFunction(input_string):
    #input_bytes = input_string.encode()
    #keccak256 = keccak.new(data=input_bytes, digest_bits=256).digest()
    keccak256 = keccak.new(data=input_string.encode(), digest_bits=256).digest()
    output_hash = binascii.hexlify(keccak256)

    #print(output_hash)

    return output_hash

    # hash_object = keccak.new(digest_bits=256)
    # hash_object.update(input_bytes)
    # digest = hash_object.digest()
    # print(digest)


def writeToFile(output_filename, output_string):
    with open(output_filename, 'wb') as f:
        f.write(output_string.encode())

file_name_counter = 98
# loop through all files in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        # process the file
        with open(file_path, 'r') as file:
            # do something with the file contents
            file_contents = file.read()

            file_contents_list = file_contents.split("\n")
            #print(file_contents_list)
            split_index = file_contents_list.index("")

            instruction_set = file_contents_list[:split_index]
            #print("Instruction set: ", instruction_set)
            data_set = file_contents_list[split_index + 1:]
            #print("Data set: ", data_set)

            instruction_set_hash = dict()
            data_set_hash = dict()

            # if (filename == "state2.txt"):
            print(filename)
            print()
            # instruction_set_hash["H"+str(len(instruction_set))] = "H(None)"
            instruction_set_hash["H" + str(len(instruction_set))] = hashFunction("None")

            output_is_ds_string = ""

            for i in range(len(instruction_set) - 1, 0, -1):
                # print(instruction_set[i], i)
                key = "H" + str(i)
                #print("Key: ", key)

                # print(i)
                if (len(instruction_set) == 2 and instruction_set[len(instruction_set) - 1] == "STOP"):
                    key = "IS"
                    instruction_set_hash[key] = ("STOP" + " || " + instruction_set_hash["H" + str(i + 1)].decode()).encode()
                    instruction_set_hash.pop("H" + str(i + 1))
                    break
                else:
                    '''
                    if (i == len(instruction_set) - 1):
                        print("1st if under else", i)
                        # instruction_set_hash[key] =  instruction_set[i]
                        #prevHashValue = instruction_set_hash["H" + str(i+1)].decode()
                        instruction_set_hash[key] = hashFunction(instruction_set[i])
                        continue
                    '''
                    if (i == len(instruction_set) - 1):
                        # instruction_set_hash[key] =  "H (" + instruction_set[i+1] + " || " + instruction_set_hash["H"+str(i+2)] + ")"
                        instruction_set_hash[key] = hashFunction(
                            instruction_set[i] + instruction_set_hash["H" + str(i + 1)].decode())
                        continue

                    if (i != 1):
                        # instruction_set_hash[key] = "H (" + instruction_set[i+1] + " || " + instruction_set_hash["H"+str(i+1)] + ")"
                        instruction_set_hash[key] = hashFunction(
                            instruction_set[i] + instruction_set_hash["H" + str(i + 1)].decode())
                    else:
                        key = "IS"
                        # instruction_set_hash[key] =   "H (" + instruction_set[i+1] + " || " + instruction_set_hash["H"+str(i+1)]
                        #print("For IS: ",key, instruction_set[i + 1], instruction_set_hash["H" + str(i + 1)].decode())
                        #instruction_set_hash[key] = hashFunction(instruction_set[i + 1] + instruction_set_hash["H" + str(i + 1)].decode())
                        instruction_set_hash[key] = (instruction_set[i] + " || " + instruction_set_hash["H" + str(i + 1)].decode()).encode()
                        final_insStack = instruction_set[i] + instruction_set_hash["H" + str(i + 1)].decode()
                        print("instruction stack: ",final_insStack)

            for key, value in instruction_set_hash.items():
                #print(key, value)
                output_is_ds_string = output_is_ds_string + key + " = " + value.decode() + "\n"
                if (key == "IS"):
                    i_stack = key + " = " + value.decode() + "\n"
            #print()

            for i in range(len(data_set) - 1, -1, -1):
                if (data_set[len(data_set) - 1] == "None") and len(data_set) == 2:
                    key = "DS"
                    # data_set_hash[key] = "H(None)"
                    data_set_hash[key] = data_set[len(data_set) - 1].encode()
                    final_dataStack = data_set[len(data_set) - 1]
                else:
                    key = "DH" + str(i)
                    if (i == len(data_set) - 1):
                        # data_set_hash[key] = "H(None)"
                        data_set_hash[key] = hashFunction("None")
                        continue

                    if (i != 0):
                        # data_set_hash[key] = "H (" + data_set[i+1] + " || " + data_set_hash["DH"+str(i+1)] + ")"
                        data_set_hash[key] = hashFunction(data_set[i + 1] + data_set_hash["DH" + str(i + 1)].decode())
                    else:
                        key = "DS"
                        # data_set_hash[key] =   "H (" + data_set[i+1] + " || " + data_set_hash["DH"+str(i+1)] + ")"
                        data_set_hash[key] = (data_set[i + 1] + " || " + data_set_hash["DH" + str(i + 1)].decode()).encode()
                        final_dataStack = data_set[i + 1]+data_set_hash["DH" + str(i + 1)].decode()
                        print("data stack: ", final_dataStack)

            for key, value in data_set_hash.items():
                print(key, value)
                output_is_ds_string = output_is_ds_string + key + " = " + value.decode() + "\n"
                if (key == "DS"):
                    d_stack = key + " = " + value.decode() + "\n"

            #IS_DS = instruction_set_hash["IS"].decode() + data_set_hash["DS"].decode()
            IS_DS = final_insStack + final_dataStack
            print("IS||DS: ",IS_DS)
            IS_DS_hash = hashFunction(IS_DS)

            print()

            IS_DS_hash_output = "0x" + IS_DS_hash.decode()

            print("IS_DS_hash", IS_DS_hash_output)
            print()

            output_file_path = "D:\Arb_code_test\state_files" # replace with the path to your folder
            filenameSplitList = filename.split(".txt")
            output_is_ds_output_file_name = output_file_path + "/" + filenameSplitList[0] + "_is_ds.txt"
            print(output_is_ds_output_file_name)

            writeToFile(output_is_ds_output_file_name, output_is_ds_string)

            state_hash_file_path = "D:\Arb_code_test\state_hashes" # replace with the path to your folder
            output_is_ds_hash_filename = state_hash_file_path + "/" + filenameSplitList[0] + "_hash.txt"
            print(output_is_ds_hash_filename)
            writeToFile(output_is_ds_hash_filename, IS_DS_hash_output)


            call_stack = "CS = None" + "\n"
            static_stack = "Static = None" + "\n"
            register_stack = "Register = None" + "\n"

            #final_state = [instruction_set_hash["IS"].decode(), data_set_hash["DS"].decode(), call_stack, static_stack, register_stack]
            final_state_file_path = "D:\Arb_code_test\states"  # replace with the path to your folder
            is_ds_file_name = final_state_file_path + "/" + filenameSplitList[0] + "_val.txt"
            f = open(is_ds_file_name, "w")
            f.write(i_stack)
            f.write(d_stack)
            f.write(call_stack)
            f.write(static_stack)
            f.write(register_stack)
            f.close()

            file_name_counter = file_name_counter + 1
            extra_file_names1 = final_state_file_path + "/" + str(file_name_counter) + "_val.txt"
            f = open(extra_file_names1, "w")
            f.write(i_stack)
            f.write(d_stack)
            f.write(call_stack)
            f.write(static_stack)
            f.write(register_stack)
            f.close()












