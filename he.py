#! /usr/bin/python3

import os.path
import sys
import random
from argparse import ArgumentParser
from sympy import randprime

class HE:
    def __init__(self):
        """
            Generate RSA parameters
        """
        N, d, e = self.setup_rsa_parameters()
        self.N = N
        self.d = d
        self.e = e

    def enc(self, m):
        """
            Performs RSA encryption
        """
        return self.fast_exp(m, self.e, self.N)
    
    def dec(self, c):
        """
            Performs RSA decryption
        """
        return self.fast_exp(c, self.d, self.N)
    
    def setup_rsa_parameters(self):
        """
            Generate parameters required for RSA encryption.
            Since our inputs are 32 byte unsigned integers (256 bits), we 
            generate primes such that their product is a number that is less
            than 2**257

            Return:
                N: product of two primes
                d: The private key
                e: The public key (default is 65537)

        """

        p, q = randprime(2 ** 256, 2 ** 257), randprime(2 ** 256, 2 ** 257)
        e = 65537
        
        # Return the appropriate parameters
        return (p * q, self.inv(e, (p - 1) * (q - 1)), e)
    
    def inv(self, a, b):
        """
            Finds the multiplicative inverse of `a` modulo `b`

            Arguments:
                a: The first number
                b: The second number

            Return:
                u: The inverse of a modulo b i.e. a * u = 1 mod b
        """
        u, g, x, y = 1, a, 0, b
        while y:
            q, t = g // y, g % y
            s = u - q * x
            u, g = x, y
            x, y = s, t

        # u and v are such that a*u + b*v = g, where g = gcd(a, b)
        # If g = 1, we may take a^-1 = u
        return u if u > 0 else u % b
    
    def fast_exp(self, base, exponent, modulus):
        """
            Function to do fast exponentiation given a base, exponent and modulus.
            This uses the binary expansion of the exponent and repeated squaring
            modulo the modulus

            Parameters:
                base: The base
                exponent: The exponent
                modulus: The modulus

            Return:
                ans: (base ** exponent) mod modulus
        """
        
        current_square, num, ans = base, exponent, 1
        while num:
            ans = (ans * current_square) % modulus if num % 2 else ans
            current_square = current_square ** 2 % modulus
            num = num // 2

        return ans


def main(filename):
    # Create our Homomorphic Encryption object
    he = HE()

    # Multiplication modulo N
    mult = lambda c1, c2, N: (c1 * c2) % N

    # Check if the CSV file exists
    if not os.path.isfile(filename):
        print("File {} does not exist".format(filename))
        sys.exit(1)
    
    # Create a key-value store (dictionary) to store integer values from the csv file
    value_dict = {}

    # Open and read the contents of the file into the key-value store
    with open(filename, "r") as csv_file:
        for idx, line in enumerate(csv_file):
            value_dict[idx] = int(line)

    
    # Unit tests 
    print("Running some unit tests...")
    
    # Basic check to see if encryption/decryption works correctly
    assert(value_dict[1] == he.dec(he.enc(value_dict[1])))
    assert(value_dict[0] != he.dec(he.enc(value_dict[1])))
    
    # Check to see if m1*m2 = Dec(Enc(m1) * Enc(m2))
    assert(mult(value_dict[1], value_dict[1], he.N) == he.dec(mult(he.enc(value_dict[1]), he.enc(value_dict[1]), he.N)))

    # Pick 3 <= x <= n random values. Multiply them and check if: 
    # m_0*m_1*...*m_x = Dec(Enc(m_0)*Enc(m_1)*...*Enc(m_x))
    n = len(value_dict)
    x = random.randint(3, n)
    sample = random.sample(range(n), x)
    prod, enc_prod = 1, 1
    for idx in sample:
        prod = mult(prod, value_dict[idx], he.N)
        enc_prod = mult(enc_prod, he.enc(value_dict[idx]), he.N)

    assert(prod == he.dec(enc_prod))
    print("All unit tests passed!")


if __name__ == "__main__":
    # Make an argument parser
    parser = ArgumentParser()
    
    # Require the user to pass a csv file
    parser.add_argument("filename", help="Name of the csv file")
    args = parser.parse_args()
    
    # Call main with the provided csv file
    main(args.filename)