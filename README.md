# Simple Homomorphic Encryption using RSA

We show a simple homomorphic encryption scheme that is homomorphic over multiplication using the popular RSA scheme.
Our input is a file with unsigned 32-byte (256 bit) integers. Given any two inputs from the file, our goal is to show that
we can perform multiplication on the encryptions of those two inputs, and the decryption of this product will equal to the
product of the the two inputs. We show this rigorously using an example:

Let `m1` and `m2` be any two integers and let `Enc(...)` and `Dec(...)` be our encryption and decryption functions. Our goal is to show that:
`m1 * m2 = Dec(Enc(m1) * Enc(m2))`

Let us see how to do this using RSA. Let our RSA parameters be `N` (modulus), `e` (public key) and `d` (private key). Using standard RSA we have:
    
    c = Enc(m) = m^e (mod N)
    m = Dec(c) = c^d (mod N)

Now, if `c1 = Enc(m1)` and `c2 = Enc(m2)`, then:
    
    c1 * c2 = (m1^e (mod N)) * (m2^e (mod N))
            = (m1 * m2)^e (mod N)

    Dec(c1 * c2) = (m1 * m2)^(e * d) (mod N)
                 = m1 * m2 mod N

Thus we have our homomorphic encryption scheme over multiplication.


This repository implements this scheme in Python. The `Dockerfile` provides an Ubuntu image with the required dependencies.
In order build the Docker image, run the `Dockerfile` as:
    
    $ git clone https://github.com/nish10z/homomorphic_encryption.git 
    $ cd homomorphic_encryption
    $ docker build -t h_enc_image .

Once the docker image is built, you may run the code as follows:
    
    $ docker run --rm -ti h_enc_image
    $ cd homomorphic_encryption
    $ python3 create_csv.py test1.csv
    $ python3 he.py test1.csv

