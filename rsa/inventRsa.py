from __future__ import print_function
import random,rabinMiller,cryptomath,sys,os

def main():
    #create public key dengan 1024 bit
    print('Create file key...')
    makeKeyFiles('key',1024)
    print('Key Files Made.')
    
def generateKey(keySize):
    #create pasangan public key dan private key
    #Step 1,generate bilangan prima , n = p * q
    print('Create bilangan prima p...')
    p = rabinMiller.generateLargePrime(keySize)
    print('Create bilangan prima q...')
    q =  rabinMiller.generateLargePrime(keySize)
    n = p * q
    
    #Step 2,generate bilangan e (relatif prima) dengan (p-1)*(q-1)
    print('Create e(relatif prima) ...')
    while True:
        #looping terus hingga di dapat bilangan e yang valid
        e = random.randrange(2 **(keySize-1), 2 ** (keySize))
        if cryptomath.gcd(e , (p-1)*(q-1)) == 1:
            break
        
    #Step 3,hitung d,mod inverse dari e
    print('Generate d,mod inverse e...')
    d = cryptomath.findModInverse(e, (p-1)&(q-1))
    
    publicKey = (n,e)
    privateKey = (n,d)
    
    print('Public key : ',publicKey)
    print('Private key : ',privateKey)
    
    return (publicKey,privateKey)

def makeKeyFiles(name,keySize):
    #create file public key dan private key
    if os.path.exists('%s_pubkey.txt' %(name)) or os.path.exists('%s_prikey.txt' %(name)):
        sys.exit('Warning : The file %s_pubkey.txt or %s_privkey.txt already exist! Use a different name or delete these files and re-run this program.' %(name,name))
        
    publicKey,privateKey = generateKey(keySize)
    
    print()
    print('The public key is a %s and a %s digit number.' % (len(str(publicKey[0])),len(str(publicKey[1]))))
    print('Writing public key to file %s_pubkey.txt...' %(name))
    fo = open('%s_pubkey.txt' % (name),'w')
    fo.write('%s,%s,%s' % (keySize,publicKey[0],publicKey[1]))
    fo.close()
    
    print()
    print('The private key is a %s and a %s digit number.' % (len(str(publicKey[0])),len(str(publicKey[1]))))
    print('Writing private key to file %s_private.txt...' % (name))
    fo = open('%s_privkey.txt' % (name), 'w')
    fo.write('%s,%s,%s' % (keySize,privateKey[0],privateKey[1]))
    fo.close()
        
if __name__ == '__main__':
    main()