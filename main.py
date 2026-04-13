#Libraries
from Code.helpers import *
from Code.sboxes import S1, S2, S3, S4
from Code.round_functions import *
from Code.key_schedule import key_schedule
from Code.cipher import encrypt_block, decrypt_block
from Code.text_cipher import *
##Verify helper functions
# x = 0x12345678
# print(word_to_bytes(x))
# print(hex(bytes_to_word(0x12, 0x34, 0x56, 0x78)))

# block = bytes.fromhex("00112233445566778899AABBCCDDEEFF")
# a, b, c, d = split_block_128(block)

# print(hex(a), hex(b), hex(c), hex(d))
# print(join_block_128(a, b, c, d).hex().upper())

##Verify S-boxes
# print(len(S1), len(S2), len(S3), len(S4))
# print(hex(S1[0]), hex(S4[255]))

##Verify round functions
# d = 0x12345678
# kr = 5
# km = 0xAABBCCDD

# print(hex(f1(d, kr, km)))
# print(hex(f2(d, kr, km)))
# print(hex(f3(d, kr, km)))

##Verify key schedule generation
# key = bytes.fromhex("000102030405060708090A0B0C0D0E0F")
# kr, km = key_schedule(key)

# print(len(kr), len(km))
# print(kr[0])
# print([hex(x) for x in km[0]])

##Verify encryption and decryption
# plaintext = bytes.fromhex("00112233445566778899AABBCCDDEEFF")
# key = bytes.fromhex("000102030405060708090A0B0C0D0E0F")

# ciphertext = encrypt_block(plaintext, key)
# recovered = decrypt_block(ciphertext, key)

# print("Plaintext :", plaintext.hex().upper())
# print("Key       :", key.hex().upper())
# print("Ciphertext:", ciphertext.hex().upper())
# print("Recovered :", recovered.hex().upper())
# print("OK?       :", recovered == plaintext)

# Test vector from https://www.cosic.esat.kuleuven.be/nessie/testvectors/bc/serpent-128-ecb-opt64.txt
# key = bytes.fromhex("2342BB9EFA38542C0AF75647F29F615D")
# pt = bytes.fromhex("00000000000000000000000000000000")

# kr, km = key_schedule(key)
# ct = encrypt_block(pt, key)
# rt = decrypt_block(ct, key)

# print("KR[0] =", [hex(x)[2:].zfill(2) for x in kr[0]])
# print("KM[0] =", [hex(x)[2:].zfill(8) for x in km[0]])
# print("CT    =", ct.hex())
# print("RT    =", rt.hex())
# print("OK?   =", rt == pt)


##Main Code : 
def main():
    plaintext = input("Enter plaintext: ")
    key = input("Enter key text: ")
    choice = input("Choose key size (16 or 32): ").strip()

    try:
        if choice not in ("16", "32"):
            raise ValueError("Key size must be 16 or 32")

        key_size = int(choice)
        normalized_key = normalize_key(key, key_size)

        ciphertext_hex = encrypt_text_to_hex_with_size(plaintext, key, key_size)
        recovered_text = decrypt_hex_to_text_with_size(ciphertext_hex, key, key_size)

        print("\n========== RESULT ==========")
        print("Plaintext            :", plaintext)
        print("Original key text    :", key)
        print("Chosen key size      :", key_size, "bytes")
        print("Normalized key bytes :", normalized_key)
        print("Normalized key text  :", normalized_key.decode('utf-8', errors='ignore'))
        print("Normalized key HEX   :", normalized_key.hex().upper())
        print("Ciphertext (HEX)     :", ciphertext_hex)
        print("Recovered            :", recovered_text)
        print("OK?                  :", recovered_text == plaintext)

    except Exception as e:
        print("\nError:", str(e))


if __name__ == "__main__":
    main()