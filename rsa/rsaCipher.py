'''
Created on 4 Mei 2014

@author: angga
'''
from __future__ import print_function
import sys,os

DEFAULT_BLOCK_SIZE = 128
BYTE_SIZE = 256

def main():
    #testing enkripsi atau deskripsi
    filename = 'encrypted_file.txt'
    mode = 'encrypt'
    
    if mode == 'encrypt':
        message = '''"Journalists belong in the gutter because that is where the ruling classes throw their guilty secrets." -Gerald Priestland "The Founding Fathers gave the free 
        press the protection it must have to bare the secrets of government and inform the people." -Hugo Black'''
        pubKeyFilename = 'key_pubkey.txt'
        print('Encrypting and writing to %s... ' %(filename))
        encryptedText = encryptAndWriteToFile(filename,pubKeyFilename,message)
        
        print('Encrypted text : ')
        print(encryptedText)
        
    elif mode == 'decrypt':
        privKeyFilename = 'key_privkey.txt'
        print('Reading from %s and decrypting...' % (filename))
        decryptedText = readFromFileAndDecrypt(filename,privKeyFilename)
        
        print('Decrypted text : ')
        print(decryptedText)

def getBlocksFromText(message,blockSize=DEFAULT_BLOCK_SIZE):
    #convert string message ke blok integer 
    messageBytes = message.encode('ascii') #convert string kedalam byte
    
    blockInts = []
    for blockStart in range(0, len(messageBytes),blockSize):
        #hitung ukuran block integer yang diperlukan
        blockInt = 0
        for i in range (blockStart,min(blockStart + blockSize, len(messageBytes))):
            blockInt += messageBytes[i]*(BYTE_SIZE ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts

def getTextFromBlock(blockInts,messageLength,blockSize=DEFAULT_BLOCK_SIZE):
    #convert blok integer ke string
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize-1,-1,-1):
            if len(message) + i < messageLength:
                #Decode message string
                asciiNumber = blockInt //(BYTE_SIZE ** i)
                blockInt = blockInt % (BYTE_SIZE ** i)
                blockMessage.insert(0,chr(asciiNumber))
        message.extend(blockMessage)
    return ''.join(message)

def encryptMessage(message,key,blockSize=DEFAULT_BLOCK_SIZE):
    #Convert the message string into block int
    #enkrip tiap blok integer. Pass PUBLIC key to encrypt
    encryptedBlocks = []
    n,e = key
    
    for block in getBlocksFromText(message, blockSize):
        #cipher text = plaintext ^ e mod n
        encryptedBlocks.append(pow(block,e,n))
    return encryptedBlocks

def decryptMessage(encryptedBlocks,messageLength,key,blockSize=DEFAULT_BLOCK_SIZE):
    decryptedBlocks = []
    n,d = key
    
    for block in encryptedBlocks:
        #plaintext = chipertext ^ d mod n
        decryptedBlocks.append(pow(block,d,n))
    return getTextFromBlock(decryptedBlocks, messageLength, blockSize)

def readKeyFile(keyFilename):
    #return the key 
    fo = open(keyFilename)
    content = fo.read()
    fo.close()
    keySize,n,EorD = content.split(',')
    return (int(keySize),int (n), int (EorD))

def encryptAndWriteToFile(messageFilename,keyFilename,message,blockSize = DEFAULT_BLOCK_SIZE):
    #menggunakan key dari file,enkrip pesan,dan tulis ke file
    #return encrypted message string
    keySize,n,e = readKeyFile(keyFilename)
    #check ukuran key size dengan blocksize
    if keySize < blockSize * 8: #8 convert bytes to bit
        sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or less than the key size. Either increase the block size or use different keys.' % (blockSize * 8, keySize))
        
    #encrypt message
    encryptedBlocks = encryptMessage(message, (n,e), blockSize)
    
    #convert integer terakhir ke string
    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ','.join(encryptedBlocks)
    
    #writeout encrypted string to a file
    encryptedContent = '%s_%s_%s' % (len(message),blockSize,encryptedContent)
    
    fo = open(messageFilename,'w')
    fo.write(encryptedContent)
    fo.close()
    
    return encryptedContent
    
def readFromFileAndDecrypt(messageFilename,keyFilename):
    #using a key from a key file ,read an encrypted message from afile then decrypted it
    #return the decrypted message string
    keySize,n,d = readKeyFile(keyFilename)
    
    #read in the message length and the encrypted message from the file
    fo = open(messageFilename)
    content = fo.read()
    messageLength,blockSize,encryptMessage = content.split('_')
    messageLength = int(messageLength)
    blockSize = int(blockSize)
    
    ## cek ukuran key size dan block size.
    if keySize < blockSize * 8: # * 8 artinya : convert bytes kedalam bits
        sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or less than the key size. Did you specify the correct key file and encrypted file?' % (blockSize * 8, keySize))
        
    #convert encrypted message ke nilai big int
    encryptedBlocks = []
    for block in encryptMessage.split('_'):
        encryptedBlocks.append(int(block))
        
    #Decrypt nilai big int
    return decryptMessage(encryptedBlocks, messageLength, (n,d), blockSize)

if __name__ == '__main__':
    main()
    
    