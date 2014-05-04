'''
Created on 2 Mei 2014

@author: angga
'''
def gcd(a, b):
    # return gcd(fpb) menggunakan algoritma euclid
    while a != 0:
        a, b = b % a, a
    return b


def findModInverse(a, m):
    # Return nilai modular inverse dari a % m, 
    # misal pada bilangan x pada contoh berikut a*x % m = 1

    if gcd(a, m) != 1:
        return None # jika a dan m bukan relatif prima,tidak ada mod inverse

    # Extended Euclidean Algorithm:
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m