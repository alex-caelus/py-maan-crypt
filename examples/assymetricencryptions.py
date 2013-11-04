# -*- coding: utf-8 -*-
# Ugly hack to allow absolute import from the root folder
# whatever its name is. Please forgive the heresy.
if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "examples"
    
import pymaancrypt
from pymaancrypt.rsa import RSA

def getDecryptOrEncrypt():
    a = input("Encrypt(e) or decrypt(d)? ")
    return a in ("decrypt", "d")

def getKey(decrypt):
    choice = ""
    while choice not in ("a", "m", "f"):
        choice = input("Input key manualy(m), "
                        + "read from file(f) or "
                        + "auto-generate key(a) ?"
                        ).lower()

    if choice == "m":
        while True:
            n = input("Enter N: ").lower()
            if n.isdigit():
                if decrypt:
                    d = input("Enter private key: ").lower()
                    if d.isdigit():
                        return RSA().makeKeyObject(n, private=d)
                else:
                    e = input("Enter public key: ").lower()
                    if e.isdigit():
                        return RSA().makeKeyObject(n, public=e)
                        
                k = input(message).lower()
                if k.isdigit():
                    return [int(n), int(k)]
                        
            print("Not a valid key, try again")

    elif choice == "a":
        while True:
            keyLength = input("Enter key length (in bits): ").lower()
            if keyLength.isdigit():
                keyGen = RSA()
                key = keyGen.generatePrivatePublicKey(int(keyLength))
                print("Generated key: ")
                print("N: " + str(key.getN()))
                print("e: " + str(key.getPublicKey()))
                print("d: " + str(key.getPrivateKey()))
                a = input("Do you want to save this key to a key-file (y/n)?: ")
                if a == "y":
                    f = open(input("Path to file (warning: file will be overwritten if it exists): "), "w")
                    try:
                        f.writelines([str(key.getN())+'\n', str(key.getPublicKey())+'\n', str(key.getPrivateKey())+'\n'])
                    except Exception as e:
                        print("Error: " + str(e))
                    finally:
                        f.close()
                return key
            else:
                print("Not a valid key length, try again")

    elif choice == "f":
        while True:
            f = open(input("Enter path to key file: "), "r")

            try:
                lines = f.readlines()
                N = int(lines[0])
                priv = int(lines[1])
                pub = int(lines[2])

                return RSA().makeKeyObject(N, pub, priv)

            except Exception as e:
                print("Error: " + str(e))
            finally:
                f.close()

def getData():
    while True:
        a = input("Read data from console(c) or file(f)?").lower()
        
        if a == "c":
            return input("Type data as one line, end with ENTER: ")
        elif a == "f":
            while True:
                f = open(input("Enter path to data file: "), "rb")

                try:
                    return bytearray(f.read())

                except Exception as e:
                    print("Error: " + str(e))
                finally:
                    f.close()

def doAction(decrypt, keyobj, data):
    
    e = RSA()
    
    if decrypt:
        decrypted = e.decrypt(data, keyobj)

        if input("print data to screen (y)?") == "y":
            print()
            print(decrypted.decode())

        if input("Write data to file (y)?") == "y":
            f = open(input("Enter path to data file: "), "wb")

            try:
                f.write(decrypted)

            except:
                print("Error: " + str(e))
            finally:
                f.close()


    else:
        encrypted = e.encrypt(data, keyobj)

        if input("print data to screen (y)?") == "y":
            print()
            print(':'.join("{0:x}".format(x) for x in encrypted))

        if input("Write data to file (y)?") == "y":
            f = open(input("Enter path to data file: "), "wb")

            try:
                f.write(encrypted)

            except:
                print("Error: " + str(e))
            finally:
                f.close()


def main():
    try:
        decrypt = getDecryptOrEncrypt()
        keyobj = getKey(decrypt)
        data = getData()
        doAction(decrypt, keyobj, data)
        input("Press enter to exit")
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()