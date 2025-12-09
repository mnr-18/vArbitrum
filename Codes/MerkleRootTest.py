import os
from Crypto.Hash import keccak
import binascii


def hashFunction(input_string):
    # input_bytes = input_string.encode()
    # keccak256 = keccak.new(data=input_bytes, digest_bits=256).digest()
    keccak_256 = keccak.new(data=input_string.encode(), digest_bits=256).digest()
    output_hash = binascii.hexlify(keccak_256)
    # print(output_hash)
    return output_hash.decode()


def generateRoot(input_hash_list):
    prevLayer = input_hash_list
    while len(prevLayer) > 1:
        half = int((len(prevLayer) + 1) / 2)
        nextLayer = []
        for i in range(0, half - 1, 1):
            if 2 * i + 1 < len(prevLayer):
                input_hash = prevLayer[2 * i] + prevLayer[2 * i + 1]
                keccak256 = hashFunction(input_hash)
                nextLayer.insert(i, keccak256)
            else:
                nextLayer.insert(i, prevLayer[2 * i])
        prevLayer = nextLayer
    return prevLayer[0]


test_list_hashes = ['0x4c484c5abf1242117409a8cbd4b813525abc5c205c90b8a1d5134ceb13f5adc2',
                    '0xe6ee84de3127f87df8f8833da0ab79cf5eae3ebc88ae76bfd4d308ab7e78e572',
                    '0x83ee6fc9e3f5923721ee0af5a2ed3e6f3762e1151dcda770c809527607ceb107',
                    '0x949e31820165e1d462d8949fa57db9795fb1b6873c00fc6fc182bc31542a6286',
                    '0x2cf62fce1d60654adf21ba130ac46f18db6c70fbdd175474867ce70c07bc09e8',
                    '0xb6061828b550b29e16cdc2e98967bf43a292cdd69c45374643c9230c3e3ef3e6',
                    '0x4414facf7c7e4fbd46950a3b23362cb11faa026c01afef8630f548054aed4fcc']
output = generateRoot(test_list_hashes)
print("MRoot = ", output)

concat_hash = '4c484c5abf1242117409a8cbd4b813525abc5c205c90b8a1d5134ceb13f5adc2' + 'e6ee84de3127f87df8f8833da0ab79cf5eae3ebc88ae76bfd4d308ab7e78e572'
hash_val = hashFunction(concat_hash)
print("Hash: ", hash_val)