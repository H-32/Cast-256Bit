from Code.helpers import split_block_128, join_block_128
from Code.round_functions import f1, f2, f3
from Code.key_schedule import key_schedule


def _mask_words(*words):
    return [word & 0xFFFFFFFF for word in words]


def q(beta, kr_i, km_i):
    a, b, c, d = beta

    c ^= f1(d, kr_i[0], km_i[0])
    b ^= f2(c, kr_i[1], km_i[1])
    a ^= f3(b, kr_i[2], km_i[2])
    d ^= f1(a, kr_i[3], km_i[3])

    return _mask_words(a, b, c, d)


def qbar(beta, kr_i, km_i):
    a, b, c, d = beta

    d ^= f1(a, kr_i[3], km_i[3])
    a ^= f3(b, kr_i[2], km_i[2])
    b ^= f2(c, kr_i[1], km_i[1])
    c ^= f1(d, kr_i[0], km_i[0])

    return _mask_words(a, b, c, d)


def _process_rounds(beta, kr, km):
    for i in range(6):
        beta = q(beta, kr[i], km[i])

    for i in range(6, 12):
        beta = qbar(beta, kr[i], km[i])

    return beta


def encrypt_block(block_bytes, key_bytes):
    if len(block_bytes) != 16:
        raise ValueError("Plaintext block must be exactly 16 bytes")

    kr, km = key_schedule(key_bytes)
    beta = list(split_block_128(block_bytes))
    beta = _process_rounds(beta, kr, km)

    return join_block_128(*beta)


def decrypt_block(block_bytes, key_bytes):
    if len(block_bytes) != 16:
        raise ValueError("Ciphertext block must be exactly 16 bytes")

    kr, km = key_schedule(key_bytes)
    beta = list(split_block_128(block_bytes))
    beta = _process_rounds(beta, list(reversed(kr)), list(reversed(km)))

    return join_block_128(*beta)