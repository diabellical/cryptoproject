#functnames and skels no defs

#!/usr/bin/env python
# encoding: utf8

#imports (etc) 
from unicodedata import normalize 
from string import ascii_letters
from random import randint
#

    #primality test of your choise
def miller_rabin(n, t):

def is_prime(n):
    
def nearest_prime(n):
    
def big_prime(size):
    
def is_even(x):
    
def jacobi(a, n):
    
def quadratic_non_residue(p):

def gauss_crt(a, n): 
    ''' returns a solution to a Chinese remainder theorem (crt) system
    of congruences, where n is a list of pairwise relative primes and
    a is a list of numbers 
    '''
def pseudosquare(p, q): 
    ''' return gauss_crt([a, b], [p, q]) '''

############
#KEYGENS
def generate_key(prime_size = 6):
    

    
######
#Encrypt//Decrypt

#primitives: 
def int_to_bool_list(n):

def bool_list_to_int(n):

#
def encrypt(m, pub_key):
    #calls int_to_bool
    def encrypt_bit
    
def decrypt(m, pri_key):
    def decrypt_bit
    return bool_list_to_int(m)

##cypertext format
def normalize_str(s):
    return un.encode('ascii', 'ignore')

def int_encode_char(c):
    return "%02d" % val

def int_encode_str(s):
    return int(''.join(int_encode_char(c) for c in normalize_str(s)))



'''calling the above functs
key = generate_key()
print (key)
m = int_encode_str('abcd')
print (m)
enc = encrypt(m, key['pub'])
print(en)
dec = decrypt(enc, key['priv'])
print (dec)
'''
