from Code.cipher import encrypt_block, decrypt_block


BLOCK_SIZE = 16
VALID_KEY_SIZES = (16, 20, 24, 28, 32)


def validate_key_bytes(key_bytes):
    if len(key_bytes) not in VALID_KEY_SIZES:
        raise ValueError("Key must be 16, 20, 24, 28, or 32 bytes")


def pkcs7_pad(data, block_size=BLOCK_SIZE):
    pad_len = block_size - (len(data) % block_size)
    if pad_len == 0:
        pad_len = block_size
    return data + bytes([pad_len] * pad_len)


def pkcs7_unpad(data, block_size=BLOCK_SIZE):
    if not data:
        raise ValueError("Data is empty")

    if len(data) % block_size != 0:
        raise ValueError("Invalid padded data length")

    pad_len = data[-1]

    if pad_len < 1 or pad_len > block_size:
        raise ValueError("Invalid padding")

    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Invalid padding")

    return data[:-pad_len]


def split_blocks(data, block_size=BLOCK_SIZE):
    return [data[i:i + block_size] for i in range(0, len(data), block_size)]


def _process_blocks(blocks, key_bytes, block_func):
    return b"".join(block_func(block, key_bytes) for block in blocks)


def encrypt_bytes(data, key_bytes):
    validate_key_bytes(key_bytes)
    padded = pkcs7_pad(data, BLOCK_SIZE)
    return _process_blocks(split_blocks(padded, BLOCK_SIZE), key_bytes, encrypt_block)


def decrypt_bytes(ciphertext, key_bytes):
    validate_key_bytes(key_bytes)

    if len(ciphertext) == 0 or len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Ciphertext length must be a multiple of 16 bytes")

    padded_plaintext = _process_blocks(
        split_blocks(ciphertext, BLOCK_SIZE),
        key_bytes,
        decrypt_block
    )
    return pkcs7_unpad(padded_plaintext, BLOCK_SIZE)


def encrypt_text(text, key_text, encoding="utf-8"):
    return encrypt_bytes(text.encode(encoding), key_text.encode(encoding))


def decrypt_text(ciphertext, key_text, encoding="utf-8"):
    return decrypt_bytes(ciphertext, key_text.encode(encoding)).decode(encoding)


def encrypt_text_to_hex(text, key_text, encoding="utf-8"):
    return encrypt_text(text, key_text, encoding).hex().upper()


def decrypt_hex_to_text(ciphertext_hex, key_text, encoding="utf-8"):
    return decrypt_text(bytes.fromhex(ciphertext_hex), key_text, encoding)


def normalize_key(key_text, target_length=16, encoding="utf-8"):
    if target_length not in VALID_KEY_SIZES:
        raise ValueError("Target key length must be 16, 20, 24, 28, or 32 bytes")

    key_bytes = key_text.encode(encoding)

    if len(key_bytes) < target_length:
        return key_bytes.ljust(target_length, b"\x00")

    return key_bytes[:target_length]


def encrypt_text_with_size(text, key_text, key_size=16, encoding="utf-8"):
    return encrypt_bytes(text.encode(encoding), normalize_key(key_text, key_size, encoding))


def decrypt_text_with_size(ciphertext, key_text, key_size=16, encoding="utf-8"):
    return decrypt_bytes(ciphertext, normalize_key(key_text, key_size, encoding)).decode(encoding)


def encrypt_text_to_hex_with_size(text, key_text, key_size=16, encoding="utf-8"):
    return encrypt_text_with_size(text, key_text, key_size, encoding).hex().upper()


def decrypt_hex_to_text_with_size(ciphertext_hex, key_text, key_size=16, encoding="utf-8"):
    return decrypt_text_with_size(bytes.fromhex(ciphertext_hex), key_text, key_size, encoding)