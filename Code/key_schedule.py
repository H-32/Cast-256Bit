from Code.helpers import add32, split_key_to_8_words
from Code.round_functions import f1, f2, f3


CM = 0x5A827999
MM = 0x6ED9EBA1
CR = 19
MR = 17


def generate_tm_tr():
    tm = []
    tr = []

    cm = CM
    cr = CR

    for _ in range(24):
        tm_row = []
        tr_row = []

        for _ in range(8):
            tm_row.append(cm)
            tr_row.append(cr)
            cm = add32(cm, MM)
            cr = (cr + MR) % 32

        tm.append(tm_row)
        tr.append(tr_row)

    return tm, tr


def forward_octave(kappa, tr_row, tm_row):
    a, b, c, d, e, f, g, h = kappa

    g ^= f1(h, tr_row[0], tm_row[0])
    f ^= f2(g, tr_row[1], tm_row[1])
    e ^= f3(f, tr_row[2], tm_row[2])
    d ^= f1(e, tr_row[3], tm_row[3])
    c ^= f2(d, tr_row[4], tm_row[4])
    b ^= f3(c, tr_row[5], tm_row[5])
    a ^= f1(b, tr_row[6], tm_row[6])
    h ^= f2(a, tr_row[7], tm_row[7])

    return [x & 0xFFFFFFFF for x in (a, b, c, d, e, f, g, h)]


def _extract_round_keys(kappa):
    a, b, c, d, e, f, g, h = kappa

    kr_i = [a & 0x1F, c & 0x1F, e & 0x1F, g & 0x1F]
    km_i = [h & 0xFFFFFFFF, f & 0xFFFFFFFF, d & 0xFFFFFFFF, b & 0xFFFFFFFF]

    return kr_i, km_i


def key_schedule(key_bytes):
    tm, tr = generate_tm_tr()
    kappa = split_key_to_8_words(key_bytes)

    kr = []
    km = []

    for i in range(12):
        kappa = forward_octave(kappa, tr[2 * i], tm[2 * i])
        kappa = forward_octave(kappa, tr[2 * i + 1], tm[2 * i + 1])

        kr_i, km_i = _extract_round_keys(kappa)
        kr.append(kr_i)
        km.append(km_i)

    return kr, km