# -*- coding: utf-8 -*-
# Ugly hack to allow absolute import from the root folder
# whatever its name is. Please forgive the heresy.
if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "examples"
    
from pymaancrypt.encoder import EncoderEN, EncoderSV
from pymaancrypt.monoalphasubstitution import MonoAlphaSubstitution
from pymaancrypt.transposition import ColumnTranspositionCipher
from pymaancrypt.caesar import Caesar
from pymaancrypt.onetimepad import OneTimePad
from pymaancrypt.rsa import RSA

def getDecryptOrEncrypt():
    a = input("Encrypt(e) or decrypt(d)? ")
    return a in ("decrypt", "d")

def getEncryptorClass():
    while(True):
        a = input("Choose chipher caesar(c), onetimepad(o), monoalphasubstitution(m), rsa(r) or columntransposition(t)? ").lower()

        if a in ("c", "caesar"):
            return Caesar
        elif a in ("m", "monoalphasubstitution"):
            return MonoAlphaSubstitution
        elif a in ("t", "columntransposition"):
            return ColumnTranspositionCipher
        elif a in ("o", "onetimepad"):
            return OneTimePad
        elif a in ("r", "rsa"):
            return RSA

def getEncoderClass():
    while(True):
        a = input("What encoding language do you want to use (english(en), swedish(sv))? ").lower()
        
        if a in ("en", "english"):
            return EncoderEN
        elif a in ("sv", "swedish"):
            return EncoderSV

def getKey(encryptorClass, encoderClass, decrypt):
    if encryptorClass is Caesar:
            
        if encoderClass is EncoderEN:
            while True:
                try:
                    return int(input("Enter key [0-25]: ").lower()) % 26
                except:
                    print("Not a valid key, try again")

        elif encoderClass is EncoderSV:
            while True:
                try:
                    return int(input("Enter key [0-28]: ").lower()) % 29
                except:
                    print("Not a valid key, try again")

        else:
            raise AssertionError("Unknown encoder class!")

    elif encryptorClass is OneTimePad:
        
        if encoderClass is EncoderEN:
            while True:
                try:
                    tmp = input("Enter key [A-Z]: ").upper()
                    if tmp.isalpha():
                        return tmp
                except:
                    print("Not a valid key, try again")

        elif encoderClass is EncoderSV:
            while True:
                try:
                    tmp = input("Enter key [A-Ö]: ").upper()
                    if tmp.isalpha():
                        return tmp
                except:
                    print("Not a valid key, try again")

        else:
            raise AssertionError("Unknown encoder class!")

    elif encryptorClass is MonoAlphaSubstitution:
        a = ""
        while a not in ("1", "2"):
            a = input("Type key into promt(1) or generate random key(2)? ").lower()

        if a == "1":
            while True:
                try:
                    return MonoAlphaSubstitution().makeKey(encoderClass(input("Enter key: ")))
                except:
                    print("Not a valid key, try again")
        else:
            keyobj = MonoAlphaSubstitution().generateRandomKey(encoderClass)
            print("Generated key: ", sep='', end='')
            for k in sorted(keyobj['key'].keys()):
                print(keyobj['key'][k], sep='', end='')
            print("")
            return keyobj

    elif encryptorClass is ColumnTranspositionCipher:
        return input("Key: ")

    elif encryptorClass is RSA:
            
        if decrypt:
            while True:
                n = input("Enter N: ").lower()
                if n.isdigit():
                    message = ""
                    if decrypt:
                        message = "Enter d: "
                    else:
                        message = "Enter e: "
                        
                    k = input(message).lower()
                    if k.isdigit():
                        return [int(n), int(k)]
                        
                print("Not a valid key, try again")
        else:
            a = ""
            while a not in ("1", "2"):
                a = input("Type key into promt(1) or generate random key(2)? ").lower()
                if a == "1":
                    while True:
                        n = input("Enter N: ").lower()
                        if n.isdigit():
                            message = ""
                            if decrypt:
                                message = "Enter d: "
                            else:
                                message = "Enter e: "
                                
                            k = input(message).lower()
                            if k.isdigit():
                                return [int(n), int(k)]
                                
                        print("Not a valid key, try again")
                else:
                    while True:
                        keyLength = input("Enter key length (in bits): ").lower()
                        if keyLength.isdigit():
                            keyGen = RSA()
                            key = keyGen.generatePrivatePublicKey(int(keyLength))
                            print("Generated key: ")
                            print("N: " + str(key.getN()))
                            print("e: " + str(key.getPublicKey()))
                            print("d: " + str(key.getPrivateKey()))
                            if decrypt:
                                return [key.getN(), key.getPrivateKey()]
                            else:
                                return [key.getN(), key.getPublicKey()]
                        else:
                            print("Not a valid key length, try again")
                 
    else:
        raise AssertionError("Unknown encryptor class!")

def doAction(decrypt, encryptorClass, encoderClass, keyobj, data):
    
    if encryptorClass is Caesar:
        encoder = encoderClass(data)
        e = Caesar(encoder.getAlphabet())
        if decrypt:
            print("Result: " + e.decrypt(keyobj, data))
        else:
            print("Result: " + e.encrypt(keyobj, encoder))
            
    elif encryptorClass is OneTimePad:
        encoder = encoderClass(data)
        e = OneTimePad(encoder.getAlphabet())
        if decrypt:
            print("Result: " + e.decrypt(keyobj, data))
        else:
            print("Result: " + e.encrypt(keyobj, encoder))

    elif encryptorClass is MonoAlphaSubstitution:
        e = MonoAlphaSubstitution()
        if decrypt:
            print("Result: " + e.decrypt(keyobj, data))
        else:
            print("Result: " + e.encrypt(keyobj, encoderClass(data)))

    elif encryptorClass is ColumnTranspositionCipher:
        e = ColumnTranspositionCipher()
        if decrypt:
            print("Result: " + e.decrypt(keyobj, data))
        else:
            print("Result: " + e.encrypt(keyobj, encoderClass(data)))
    elif encryptorClass is RSA:
        e = RSA()
        if decrypt:
            print("Result: " + str(e.decrypt(keyobj[0], keyobj[1], int(data))))
        else:
            print("Result: " + str(e.encrypt(keyobj[0], keyobj[1], encoderClass(data).getIntegerEncoded())))
        

def main():
    try:
        decrypt = getDecryptOrEncrypt()
        encryptorClass = getEncryptorClass()
        encoderClass = getEncoderClass()
        keyobj = getKey(encryptorClass, encoderClass, decrypt)
        data = input("Data: ")
        doAction(decrypt, encryptorClass, encoderClass, keyobj, data)
        input("Press enter to exit")
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()