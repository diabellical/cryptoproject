from random import randint
import kegen ## project module
from foo import legendre
#be sure, (N, y) are imported, as well as p,q.





def int_to_bool_list(n): #list(bools) <- delimited bits <-binary <-integer
    return [b == "1" for b in "{0:b}".format(n)] 

'''
>>>int_to_bool_list(2)
[True, False]
>>>int_to_bool_list(8)
[True,False,False,False]
'''


def bool_list_to_int(bool_list):  # int <- binary  <-delimited bits <- list(bools)
    s = ''.join(['1' if b else '0' for b in bool_list])
    return int(s, 2)
'''
>>> bool_list_to_int([True,True,False])
6
>>> bool_list_to_int([True,True,False,True])
13
>>>
'''

def encrypt(message, pubK):
    bin_m = int_to_bool_list(message)    #message to bools
    N, a = pubK                    #unpacks N, y for use in enclosed def

    def encrypt_bit(bit):                #bit by bit encryption
        x = randint(0, N)
        if bit:
            return ((y * pow(x, 2, N)) % N)   #pow(x,y,z) = x**y mod z
        return pow(x, 2, N)
    return map(encrypt_bit, bin_m)

def decrypt(cipher, privK):
    p, q = privK                   #unpacks p, q for use in enclosed def
    def decrypt_bit(bit):
        e = legendre(bit, p)
        if e == 1:
            return False
        return True

    m = map(decrypt_bit, cipher)
    return bool_list_to_int(m)       #get back plaintext integer.
