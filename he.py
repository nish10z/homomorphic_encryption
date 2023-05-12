#! /usr/bin/python3

import os.path
import sys
from argparse import ArgumentParser
from sympy import randprime

def inv(a, b):
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

def setup_rsa_parameters():
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
    return (p * q, inv(e, (p - 1) * (q - 1)), e)


def fast_exp(base, exponent, modulus):
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
    # Generate RSA parameters
    N, d, e = setup_rsa_parameters()
    
    # Define our encryption and decryption functions
    encrypt = lambda m, e, N: fast_exp(m, e, N)
    decrypt = lambda c, d, N: fast_exp(c, d, N)

    # Function that multiplies two ciphertexts
    fhe_multiply = lambda c1, c2, N: (c1 * c2) % N

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

    # Test to see if FHE works    
    assert(value_dict[1] == decrypt(encrypt(value_dict[1], e, N), d, N))
    assert(value_dict[0] != decrypt(encrypt(value_dict[1], e, N), d, N))
    assert(value_dict[1] * value_dict[1] == decrypt(fhe_multiply(encrypt(value_dict[1], e, N), encrypt(value_dict[1], e, N), N), d, N))


if __name__ == "__main__":
    # Make an argument parser
    parser = ArgumentParser()
    
    # Require the user to pass a csv file
    parser.add_argument("filename", help="Name of the csv file")
    args = parser.parse_args()
    
    # Call main with the provided csv file
    main(args.filename)