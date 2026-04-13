from Code.helpers import add32, sub32, xor32, rol, word_to_bytes
from Code.sboxes import S1, S2, S3, S4


def _split_after_rotate(value, kr):
    return word_to_bytes(rol(value, kr))


def f1(d, kr, km):
    ia, ib, ic, id_ = _split_after_rotate(add32(km, d), kr)
    return add32(sub32(S1[ia] ^ S2[ib], S3[ic]), S4[id_])


def f2(d, kr, km):
    ia, ib, ic, id_ = _split_after_rotate(xor32(km, d), kr)
    return xor32(add32(sub32(S1[ia], S2[ib]), S3[ic]), S4[id_])


def f3(d, kr, km):
    ia, ib, ic, id_ = _split_after_rotate(sub32(km, d), kr)
    return sub32((add32(S1[ia], S2[ib]) ^ S3[ic]), S4[id_])