# Simple Homomorphic Encryption using RSA

We show a simple homomorphic encryption scheme that is homomorphic over multiplication.
Our input is a file with unsigned 32-byte (256 bit) integers. Given any number of inputs from the file, our goal is to show that
we can perform multiplication on the encryptions of those inputs and the decryption of this product will equal the
product of all the inputs. We show the scheme using a two-input example. The scheme easily generalizes to more than two inputs. We note that by multiplication we mean \`multiplication modulo `N`\`, where `N` in our case is roughly `2^512`.

Let `m1` and `m2` be any two integers and let `Enc(...)` and `Dec(...)` be our encryption and decryption functions. Our goal is to show that:
`m1 * m2 = Dec(Enc(m1) * Enc(m2)) (mod N)`

Let us see how to do this using the RSA cryptosystem. Let our RSA parameters be `N` (modulus), `e` (public key) and `d` (private key). Using standard RSA we have:
    
    c = Enc(m) = m^e (mod N)
    m = Dec(c) = c^d (mod N)

Now, if `c1 = Enc(m1)` and `c2 = Enc(m2)`, then:
    
    c1 * c2 = (m1^e (mod N)) * (m2^e (mod N))
            = (m1 * m2)^e (mod N)

    Dec(c1 * c2) = (m1 * m2)^(e * d) (mod N)
                 = m1 * m2 (mod N)

This gives us our homomorphic encryption scheme over multiplication.


This repository implements the RSA-based scheme in Python. There are two Python scripts. The first one `he.py` takes as input a file containing up to 100 32-byte integers. It then runs a few unit tests to check if our homomorphic encryption scheme works. The repository also provides a helper script `create_csv.py` that creates a csv file with integers.


Also included is a `Dockerfile` that provides an Ubuntu image with the required dependencies to run the two python scripts.
In order build the Docker image please run:
    
    $ git clone https://github.com/nish10z/homomorphic_encryption.git 
    $ cd homomorphic_encryption
    $ docker build -t he_image .

Once the docker image is built, you may run the code as follows:
    
    $ docker run --rm -ti he_image
    $ cd homomorphic_encryption
    $ python3 create_csv.py test1.csv 100
    $ python3 he.py test1.csv

