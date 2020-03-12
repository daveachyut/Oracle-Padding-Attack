#!/usr/bin/python3

# Import necessary libraries
import requests
import sys


# Converts the ciphertext into blocks of 16 bytes.
def split_blocks(data):
    lenght = len(data)
    blocks = []
    for i in range(lenght//16):
        blocks.append(data[i*16:(i+1)*16])
    return blocks

# Used to find the XOR result of two blocks. 
def byte_xor(ba1, ba2):
    return bytearray([_a ^ _b for _a, _b in zip(ba1, ba2)])

# The main function where the logic of Oracle Padding Attack is implemented. 
def find_bytes(block, all_blocks, index):
    oracle_url = "https://project1.ecen4133.org/acda7163/paddingoracle/verify"
    print(block)

    plaintext_bytes = bytearray([0 for _ in range(16)])
    c = bytearray([random.randint(0,16) for b in range(0,16)])
    for i in range(16):
        expected_padding = bytearray([0 for _ in range(16-i)] + [(i+1) for _ in range(i)])
        print("expected_padding=",expected_padding)
        c_prime = byte_xor(byte_xor(expected_padding, plaintext_bytes), c)
        for byte in range(1,256):
            c_prime[15 - i] = byte
            cipher_temp = ""
            for k  in all_blocks[:index]:
                cipher_temp+=str(k.hex())
            cipher_temp += str(c_prime.hex()) + str((all_blocks[index+1]).hex())
             
            r = requests.get("%s?message=%s" % (oracle_url, bytes.fromhex(cipher_temp).hex()))
            r.raise_for_status()
            obj = r.json()
            
            if i==10:
                plaintext_bytes[15-i] = (byte ^ (i+1) ^ block[15-i])
#               print("dc byte",(byte^(i+1)).hex())
                print("plaintext_bytes = ",plaintext_bytes)
#               print(" ciphertext = ", cipher_temp)
                print("c_prime",c_prime)
#               print("")
                break
    
            
            else:
                if obj['status'] == 'invalid_mac':
                    plaintext_bytes[15-i] = (byte ^ (i+1) ^ block[15-i])
#                   print("dc byte",(byte^(i+1)).hex())
                    print("plaintext_bytes = ",plaintext_bytes)
#                   print(" ciphertext = ", cipher_temp)
                    print("c_prime",c_prime)
#                   print("")
                    break
    
    return "".join([chr(b) for b in plaintext_bytes if b > 16])
            
        

# Used to convert the final outcome of the Oracle Padding Attack from hexadecimal blocks to readable English.
def find_plaintext(ciphertext):
    ciphertext = bytearray.fromhex(ciphertext)
    blocks = split_blocks(ciphertext)
    plaintext = ""
    for i in range(len(blocks)-2,-1,-1):
        plaintext = find_bytes(blocks[i], blocks, i) + plaintext
        break
        print(plaintext)
    

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: %s ORACLE_URL CIPHERTEXT_HEX" % (sys.argv[0]), file=sys.stderr)
        sys.exit(-1)
    oracle_url = sys.argv[1]
    ciphertext = sys.argv[2]
    
    #ciphertext = "64693d54753558f3eeb3df4270df19e456b6a6d9979c270e25e61d9e9b694dbdb2bb87cb11c9fed11db692f4cccef6e2b21fe103a4bb3e3d1fae5decd8526f788ab53c79263fa21c2ec5e5f24835b827a47c6b0c539febf0b1927009fa4cdb18"
    #find_plaintext(ciphertext)
   
    # Example check of ciphertext at the oracle URL:
#     r = requests.get("%s?message=%s" % (oracle_url, bytes.fromhex(ciphertext).hex()))
#     r.raise_for_status()
#     obj = r.json()
#     print(obj)










