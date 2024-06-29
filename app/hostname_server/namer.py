import re
from datetime import date


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # нумерация с 1
base = len(alphabet)

def code(year, month):
    yy = year%100 # 20|23 -> 23
    mm = month if ((yy//base)%2 == 0) else (month + 12) # 0-25 0; 26-51 1; 52-77 2; 78-103 3
    by = (yy%base-1) # 23%26-1 # A-1 B-2 ... Z-26
    bm = (mm%base-1)
    ey = alphabet[by]
    em = alphabet[bm]
    print(year, month, yy, mm, by, bm)
    return ey + em

def prefix():
    today = date.today()
    px = code(today.year,today.month)
    return px

def hostname(prex, id, client = "", postx = ""):
    name = "{:04d}".format(id)
    return f'{prex}{name}{client}{postx}'

def mac_to_int(mac):
    res = re.match("^((?:(?:[0-9a-f]{2})[:-]){5}[0-9a-f]{2})$", mac.lower())
    if res is None:
        raise ValueError("invalid mac address")
    return int(res.group(0).replace(":", ""), 16)

def int_to_mac(mac_int):
    if type(mac_int) != int:
        raise ValueError("invalid integer")
    return ":".join(
        ["{}{}".format(a, b) for a, b in zip(*[iter("{:012x}".format(mac_int))] * 2)]
    )