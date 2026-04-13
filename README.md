# CAST-256 Implementation in Python

This repository contains a Python implementation of the **CAST-256** block cipher, including:

- 32-bit helper operations
- Round functions (`f1`, `f2`, `f3`)
- Key schedule generation
- Block encryption/decryption
- Text encryption/decryption with PKCS#7 padding
- CAST-256 S-boxes

## Overview

CAST-256 is a symmetric block cipher that operates on:

- **Block size:** 128 bits (16 bytes)
- **Supported key sizes:** 128, 160, 192, 224, and 256 bits  
  (16, 20, 24, 28, or 32 bytes)

This implementation is organized into several modules to keep the code clean and easy to understand.

---

## Project Structure

```text
Code/
├── helpers.py
├── round_functions.py
├── sboxes.py
├── key_schedule.py
├── cipher.py
└── text_cipher.py
```

---

## 1. Helper Functions

The `helpers.py` module contains the low-level operations used throughout the implementation.

### Bitwise and Arithmetic Operations

The implementation relies on the following basic operations:

- `^` = XOR
- `&` = AND
- `|` = OR

### Functions

#### `add32(a, b)`
Performs addition modulo `2^32`.

```python
return (a + b) & 0xFFFFFFFF
```

This ensures the result always stays within **32 bits**.

#### `sub32(a, b)`
Performs subtraction modulo `2^32`.

```python
return (a - b) & 0xFFFFFFFF
```

#### `xor32(a, b)`
Performs XOR and keeps the result within 32 bits.

```python
return (a ^ b) & 0xFFFFFFFF
```

#### `rol(x, n)`
Rotates a 32-bit word to the left by `n` bits.

```python
return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF
```

#### `word_to_bytes(x)`
Converts a 32-bit word into 4 bytes using **big-endian** byte order.

#### `bytes_to_word(b0, b1, b2, b3)`
Combines 4 bytes into a 32-bit word using **big-endian** format.

#### `split_block_128(block_bytes)`
Splits a 16-byte block into four 32-bit words.

#### `join_block_128(a, b, c, d)`
Combines four 32-bit words into a 16-byte block.

#### `split_key_to_8_words(key_bytes)`
Accepts a key of length:

- 16 bytes
- 20 bytes
- 24 bytes
- 28 bytes
- 32 bytes

Then pads it with zero bytes up to 32 bytes and splits it into **8 words** of 32 bits each.

---

## 2. Round Functions

The `round_functions.py` module implements the three CAST-256 round functions:

- `f1`
- `f2`
- `f3`

These functions use:

- 32-bit arithmetic
- Rotation
- Four S-boxes: `S1`, `S2`, `S3`, `S4`

### Internal Helper

#### `_split_after_rotate(value, kr)`
Rotates the input value left by `kr` bits, then splits it into 4 bytes.

### `f1(d, kr, km)`

```python
ia, ib, ic, id_ = _split_after_rotate(add32(km, d), kr)
return add32(sub32(S1[ia] ^ S2[ib], S3[ic]), S4[id_])
```

### `f2(d, kr, km)`

```python
ia, ib, ic, id_ = _split_after_rotate(xor32(km, d), kr)
return xor32(add32(sub32(S1[ia], S2[ib]), S3[ic]), S4[id_])
```

### `f3(d, kr, km)`

```python
ia, ib, ic, id_ = _split_after_rotate(sub32(km, d), kr)
return sub32((add32(S1[ia], S2[ib]) ^ S3[ic]), S4[id_])
```

Each function produces a 32-bit output based on the data word `d`, rotation key `kr`, masking key `km`, and the S-box values.

---

## 3. S-boxes

The `sboxes.py` module defines the four substitution tables used by CAST-256:

- `S1`
- `S2`
- `S3`
- `S4`

### `_parse_sbox(text)`
Parses a block of hexadecimal values into a Python list.

Each S-box must contain exactly **256 values**.

---

## 4. Key Schedule

The `key_schedule.py` module generates the round subkeys used during encryption and decryption.

### Constants

```python
CM = 0x5A827999
MM = 0x6ED9EBA1
CR = 19
MR = 17
```

### `generate_tm_tr()`
Generates two tables:

- `tm`
- `tr`

Each table contains parameters used during the key expansion process.

### `forward_octave(kappa, tr_row, tm_row)`
Transforms the 8-word key state using the round functions in a forward sequence.

### `_extract_round_keys(kappa)`
Extracts:

- `kr_i`: rotation subkeys
- `km_i`: masking subkeys

from the current key state.

### `key_schedule(key_bytes)`
Builds the full set of subkeys for CAST-256.

It returns:

- `kr`: 12 round rotation key groups
- `km`: 12 round masking key groups

Each round contains 4 subkeys.

---

## 5. Block Cipher

The `cipher.py` module performs encryption and decryption of a single 128-bit block.

### Internal Utilities

#### `_mask_words(*words)`
Forces all words to remain within 32-bit range.

### Forward Round: `q(beta, kr_i, km_i)`

This applies one forward CAST-256 round transformation.

### Reverse Round: `qbar(beta, kr_i, km_i)`

This applies the reverse form used in the second half of the algorithm.

### `_process_rounds(beta, kr, km)`

- First 6 rounds use `q`
- Last 6 rounds use `qbar`

### `encrypt_block(block_bytes, key_bytes)`

Encrypts a single 16-byte plaintext block.

Checks:
- block must be exactly 16 bytes

Steps:
1. Generate round keys
2. Split block into four 32-bit words
3. Process 12 rounds
4. Join words back into 16 bytes

### `decrypt_block(block_bytes, key_bytes)`

Decrypts a single 16-byte ciphertext block.

Checks:
- block must be exactly 16 bytes

Steps:
1. Generate round keys
2. Reverse the round keys
3. Process rounds
4. Rebuild the plaintext block

---

## 6. Text Encryption Utilities

The `text_cipher.py` module extends the block cipher to support full text encryption and decryption.

### Constants

```python
BLOCK_SIZE = 16
VALID_KEY_SIZES = (16, 20, 24, 28, 32)
```

### Key Validation

#### `validate_key_bytes(key_bytes)`
Ensures the key length is one of the supported CAST-256 sizes.

---

## 7. PKCS#7 Padding

Since CAST-256 works on fixed 16-byte blocks, plaintext must be padded before encryption.

### `pkcs7_pad(data, block_size=16)`
Adds PKCS#7 padding.

### `pkcs7_unpad(data, block_size=16)`
Removes PKCS#7 padding and validates it.

---

## 8. Multi-block Processing

### `split_blocks(data, block_size=16)`
Splits data into blocks of 16 bytes.

### `_process_blocks(blocks, key_bytes, block_func)`
Processes all blocks using either:

- `encrypt_block`
- `decrypt_block`

---

## 9. Byte-level Encryption Functions

### `encrypt_bytes(data, key_bytes)`
Encrypts raw bytes.

### `decrypt_bytes(ciphertext, key_bytes)`
Decrypts raw bytes.

Checks that ciphertext length is a multiple of 16 bytes.

---

## 10. Text-level Encryption Functions

### `encrypt_text(text, key_text, encoding="utf-8")`
Encrypts a string and returns ciphertext as bytes.

### `decrypt_text(ciphertext, key_text, encoding="utf-8")`
Decrypts ciphertext bytes and returns the original string.

### `encrypt_text_to_hex(text, key_text, encoding="utf-8")`
Encrypts text and returns the ciphertext as an uppercase hexadecimal string.

### `decrypt_hex_to_text(ciphertext_hex, key_text, encoding="utf-8")`
Decrypts a hexadecimal ciphertext string back into text.

---

## 11. Key Normalization

### `normalize_key(key_text, target_length=16, encoding="utf-8")`

Converts a text key into a byte key of the desired length.

Rules:
- If the key is shorter than the target size, it is padded with `0x00`
- If it is longer, it is truncated

Supported target sizes:
- 16
- 20
- 24
- 28
- 32 bytes

---

## 12. Variable Key Size Helpers

### `encrypt_text_with_size(text, key_text, key_size=16, encoding="utf-8")`
Encrypts text using a normalized key of the selected size.

### `decrypt_text_with_size(ciphertext, key_text, key_size=16, encoding="utf-8")`
Decrypts ciphertext using the selected key size.

### `encrypt_text_to_hex_with_size(text, key_text, key_size=16, encoding="utf-8")`
Encrypts text and returns uppercase hexadecimal output.

### `decrypt_hex_to_text_with_size(ciphertext_hex, key_text, key_size=16, encoding="utf-8")`
Decrypts hexadecimal ciphertext using the selected key size.

---

## Example Usage

```python
from Code.text_cipher import (
    encrypt_text_to_hex_with_size,
    decrypt_hex_to_text_with_size
)

plaintext = "Hello CAST-256"
key = "mysecretkey"

cipher_hex = encrypt_text_to_hex_with_size(plaintext, key, key_size=16)
print("Ciphertext (HEX):", cipher_hex)

decrypted = decrypt_hex_to_text_with_size(cipher_hex, key, key_size=16)
print("Decrypted:", decrypted)
```

---

## Notes

- This implementation supports **128-bit block encryption**
- Supported key sizes are **128/160/192/224/256 bits**
- Text encryption uses **PKCS#7 padding**
- Key material can be provided either as raw bytes or as text
- Hex helpers are included for easier testing and display

---

## Error Handling

The code raises `ValueError` in cases such as:

- invalid block size
- invalid key size
- invalid ciphertext length
- invalid padding
- empty padded input

---

## Educational Purpose

This project is useful for understanding the internal structure of CAST-256, including:

- 32-bit modular arithmetic
- S-box-based transformations
- round functions
- key schedule generation
- block encryption/decryption
- text handling with padding

---

## License

This project can be used for educational and academic purposes.
