import random
from math import gcd
from hashlib import sha1


def fastModular(a, b, c):
    result = 1
    a = a % c
    b = int(b)
    while b:
        if b % 2 == 1:
            result = (result*a) % c
        a = (a*a) % c
        b >>= 1
    return result


def millerRabin(p):
    d = p-1
    s = 0
    i = 0
    a = random.randint(1, p)
    while d % 2 == 0:
        d //= 2
        s += 1
    if fastModular(a, d, p) == 1:
        return True
    else:
        while i < s:
            res = fastModular(a, (2**i)*d, p)
            i += 1
            if(res == p-1):
                return True
        else:
            return False

#Extended Euclidean Algorithm
def exgcd(a, b):
    list = []
    x0, x1, x2 = 1, 0, a
    y0, y1, y2 = 0, 1, b
    n = 0

    while(True):
        if(a % b != 0):
            q1 = a // b
            r2 = a % b
            temp = b
            b = r2
            a = temp

            x = x1 * q1 + x0
            x0 = x1
            x1 = x
            y = y1 * q1 + y0
            y0 = y1
            y1 = y
            n += 1
        else:
            x = pow(-1, n+1) * x
            y = pow(-1, n+2) * y
            list.append(x)
            list.append(y)
            return list

def prime():
    while True:
        a = random.getrandbits(8)
        if a % 2 != 0 and millerRabin(a):
            return a

def encrypt(m, e, n):
    result = []
    # str -> byte
    m = m.encode("utf-8")
    for i in m:
        result.append(str(fastModular(int(i), e, n)))
    c = '-'.join(result)
    print("encrpted message:", c)
    return c

def decrypt(c):
    n = input('n =')
    n = int(n)
    d = input('d =')
    d = int(d)

    result = b''
    for encrypted_byte in c.split('-'):
        decrypted_byte = fastModular(int(encrypted_byte), d, n)
        result += bytes([decrypted_byte])
    result = result.decode('utf-8')
    print(result)
    return result

def sign(hm, d, n):
    result = []
    for encrypted_byte in hm.split('-'):
        signed_byte = fastModular(int(encrypted_byte), d, n)
        result.append(str(signed_byte))
    signature = '-'.join(result)
    print('The signature is:', signature)
    return signature

def verify(m, e, n, signature):
    verified = True
    hm = encrypt(m, e, n)
    for encrypted_byte, signed_byte in zip(hm.split('-'), signature.split('-')):
        decrypted_byte = fastModular(int(signed_byte), e, n)
        if decrypted_byte != int(encrypted_byte):
            verified = False
            break
    return verified

def main():

    while True:
        p = prime()
        q = prime()

        n = p*q
        fn = (p-1)*(q-1)

        if n > 256:
            break

    e = random.randint(1, fn)

    while gcd(fn, e) != 1:
        e = random.randint(1, fn)

    print('e=', e)
    d = exgcd(fn, e)[1] % fn

    while True:
        i = input()
        if i == "en":
            m = input('Please input the message:')
            encrypt(m, e, n)
            print('The private key (n, d) is({},{}):'.format(n, d))

        elif i == 'sign':
            m = input('Please input the message:')
            hm = encrypt(m, e, n)
            signature = sign(hm, d, n)
            print('The public key (n, e) is({},{}):'.format(n, e))

        elif i == 'de':
            c = input('Please input the encrypted message:')
            decrypt(c)
            break

        elif i == 'verify':
            m = input('Please input the message:')
            signature = input('signature =')
            ve = int(input('e ='))
            vn = int(input('n ='))
            if verify(m, ve, vn, signature):
                print('The signature is valid.')
            else:
                print('The signature is invalid.')

        else:
            break


if __name__ == '__main__':
    main()
