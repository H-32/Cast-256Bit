def add32(a, b):
    return (a + b) & 0xFFFFFFFF


def sub32(a, b):
    return (a - b) & 0xFFFFFFFF


def xor32(a, b):
    return (a ^ b) & 0xFFFFFFFF


def rol(x, n):
    x &= 0xFFFFFFFF
    n &= 31
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


def word_to_bytes(x):
    return list((x & 0xFFFFFFFF).to_bytes(4, byteorder="big"))


def bytes_to_word(b0, b1, b2, b3):
    return int.from_bytes(bytes([b0, b1, b2, b3]), byteorder="big")


def split_block_128(block_bytes):
    if len(block_bytes) != 16:
        raise ValueError("Block must be exactly 16 bytes")

    return tuple(
        int.from_bytes(block_bytes[i:i + 4], byteorder="big")
        for i in range(0, 16, 4)
    )


def join_block_128(a, b, c, d):
    return b"".join(
        (word & 0xFFFFFFFF).to_bytes(4, byteorder="big")
        for word in (a, b, c, d)
    )


def split_key_to_8_words(key_bytes):
    if len(key_bytes) not in (16, 20, 24, 28, 32):
        raise ValueError("Key must be 16, 20, 24, 28, or 32 bytes")

    padded = key_bytes.ljust(32, b"\x00")

    return [
        int.from_bytes(padded[i:i + 4], byteorder="big")
        for i in range(0, 32, 4)
    ]