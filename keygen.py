
#Bingham & Fournier Presents:
#                   THE GOLDWASSER MICALI CRYPTOSYSTEM
#An asymmetric public key probabilistic partially homomorphic cryptosystem.
#
#Here we demonstrate the public key generation, encryption, and decryption
#of a bit. Typically large (~2^500) p, q are created by a PRNG, checked for
#primality by Miller-Rabin test. This is standard across many cryptosystems,
# so instead we are just fixing prime p, q and actually implementing the more
#unique aspects of the cryptosystem. First is establishing an a that is a
#quadratic nonresidue mod p and mod q as part of public key (N,a). Hence we
#give the following algorithm that generates random a and calculates it's
#legendre symbol until we find one with (a/p)=(a/q)=-1.
from random import randint # for randint number generator

p = 5545545544607
q = 97846352783659
N = p * q

#This is for use in generating possible a's
m=max(p, q)

# Since the legendre symbol is multiplicative, we will break off the even
# part of a and then use quadratic reciprocity (QR) to calculate the symbols
# of even and odd parts and multiply them together to find (a/p). This
# function returns a Boolean that tells us whether to divide by two.
def isEven(x):
    return x % 2 == 0

# Calculates the legendre symbol (a, n), n is prime.
def legendre(a, n):

    if a == 0:
        return 0
    if a == 1:
        return 1
    e = 0                   #Tracks how many powers of two divide a
    a1 = a                  #a1 will be the odd part of of a once
    while isEven(a1):       #this loop completes. Then 2^e*a1=a
        e += 1
        a1 /= 2

    s = 0                   #s will be the eventual legendre symbol

#Cacluate even part of Legendre Symbol
    if isEven(e):     # Since (2/n)=1 or -1, if e is even,
        s = 1         # (2^e/n)=(2/n)^e =1
    elif n % 8 in {1, 7}:   #otherwise, (2^e/n)=(2/n)
        s = 1               #which we calculate according to QR here
    elif n % 8 in {3, 5}:
        s = -1

#Calculate odd part of Legendre according to QR.
    if n % 4 == 3 and a1 % 4 == 3:
        s *= -1     # update s

    n1 = n % a1     # reduce in anticipation of flip

    if a1 == 1:     # once we are totally reduced we are done.
        return s
    else:           # calls the function again on the reduced flipped
        return s * legendre(n1, a1) # pair until finished.
#end legendre def

# This function generates possible values of a and evaluates their
# legendre symbols, until we find a suitable a for the public key.
def isNonresidue(p, q):
    a = 0
    while legendre(a, p) != -1 or legendre (a, q) != -1:
        a = randint(1, m)
    return a

a=isNonresidue(p,q)
keys = {'pubKey': (N, a), 'privKey': (p, q)}

print(keys['pubKey'])
pubKey_out = keys['pubKey']
priKey_out = keys['privKey']
