def gcd(a,b):
    while(b!=0):
        a,b = b,a%b
    return a

def lcm(a,b):
    return (a*b)//gcd(a,b)

def prime(a):
    for i in range(2,a):
        if (a%i ==0):
            return False
    return True

def inverse_mod(base,m):
    for i in range(1,base):
        if (((i*m)%base)==1):
            return i

def makeblocks(message,length):
    messagenum = ""
    separator = 0
    for i in range(len(message)):
        if (i > 0 and len(messagenum)%length==separator):
            messagenum += ","
            separator += 1
        if (ord(message[i])%97<10):
            messagenum += "0"
        messagenum += str(ord(message[i])%97)
        if (separator==length):
            separator = 0
    blocks = messagenum.split(",")
    return blocks

def blockstotext(blocks):
    decryptednum, decrypted = "", ""
    for numbers in blocks:
        decryptednum += str(numbers)
    current = ""
    for i in range (len(decryptednum)):
        current += str(decryptednum[i])
        if (i % 2 != 0):
            decrypted += chr(int(current)+97)
            current = ""
    return decrypted

def ersa1(p,q):
    if(not prime(p)):
        print("p not prime")
        return (0,0)
    if(not prime(q)):
        print("q not prime")
        return (0,0)
    n = p*q
    toitent = (p-1)*(q-1)
    return (n,toitent)

def ersa2(n,e,message):
    if (gcd(n,e)!=1):
        print("e is not coprime with n")
        return []
    valid = False
    length = len(str(n))
    while (not valid):
        currentlength = length
        blocks = makeblocks(message,length)
        for i in range(len(blocks)):
            if (int(blocks[i])>=n-1):
                length -= 1
        if (length==currentlength):
            valid = True      
    for i in range(len(blocks)):
        blocks[i] = (int(blocks[i])**e) % n
    encrypted = ""
    for i in range(len(blocks)):
        if (i==len(blocks)-1):
            encrypted += str(blocks[i])
            break
        encrypted += str(blocks[i]) + " "
    return encrypted

def elgamalkey(p,g,x):
    if (g<p and 1<x<=p-2):
        return (g**x) % p
    else:
        print("value not valid")

def eelgamal(y,p,g,k,message):
    if (1<=k<=p-2):
        valid = False
        length = len(str(p))
        while (not valid):
            currentlength = length
            blocks = makeblocks(message,length)
            for i in range(len(blocks)):
                if (int(blocks[i])>=p-1):
                    length -= 1
            if (length==currentlength):
                valid = True
        enc1 = []
        enc2 = []
        for i in range(len(blocks)):
            enc1.append((g**k) % p)
            enc2.append((((y**k) * int(blocks[i])) % p))
        return(enc1,enc2)
    else:
        print("k tidak valid")
        return([],[])

def paillierkey(p,q,g):
    if(not prime(p)):
        print("p not prime")
        return (0,0)
    if(not prime(q)):
        print("q not prime")
        return (0,0)
    if(gcd(p,q)!=1):
        print("not co prime")
        return (0,0)
    n = p*q
    yss = lcm(p-1,q-1)
    myu = inverse_mod(n,(((g**yss)%(n**2))-1)/n)
    return n,yss,myu

def epaillier(p,g,n,r,message):
    if(r<0 or r>n or gcd(r,n)!=1):
        print("r not valid")
        return (0,0)
    blocks = makeblocks(message,2)
    enc = []
    for i in range(len(blocks)):
        enc.append(((g**int(blocks[i]))*(r**n))%(n**2))
    return enc

def dpaillier(p,n,yss,myu,enc):
    blocks = []
    for i in range(len(enc)):
        plainnumber = ((((((enc[i]**yss)%(n**2))-1)/n)*myu)%n)
        blockselem = str(int(plainnumber))
        if (i==len(enc)-1):
            if (len(blockselem)<2):
                blockselem = "0" + blockselem 
        while (len(blockselem)<2):
            blockselem = "0" + blockselem

        blocks.append(blockselem)
    return blockstotext(blocks)

def delgamal(x,p,enc1,enc2):
    blocks = []
    for i in range(len(enc1)):
        plainnumber = (enc2[i]*(enc1[i]**(p-1-x)) % p) % p
        blockselem = str(plainnumber)
        valid = False
        if (i==len(enc1)-1):
            if (len(blockselem) % 2 != 0):
                blockselem = "0" + blockselem
            valid = True   
        while (not valid):
            if(len(blockselem)<len(str(p))):
                blockselem = "0" + blockselem
            else:
                valid = True
        blocks.append(blockselem)
    return blockstotext(blocks)

def drsa(n,toitent,e,encrypted):
    d = inverse_mod(toitent,e)
    blocks = encrypted.split(" ")
    for i in range(len(blocks)):
        blocks[i] = (int(blocks[i])**d) % n
        if (len(str(blocks[i]))==len(str(n))-1):
            blocks[i] = "0" + str(blocks[i])
    return blockstotext(blocks)

'''
print("rsa")
p = int(input())
q = int(input())
(n,toitent) = ersa1(p,q)
message1 = input("input pteks\n")
message = message1.lower().replace(" ","")
e = int(input())
encrypt = ersa2(n,e,message)
print(encrypt)
decrypt = drsa(n,toitent,e,encrypt)
print(decrypt)


print("elgamal")
p = int(input("p\n"))
g = int(input("g\n"))
x = int(input("x\n"))
y = elgamalkey(p,g,x)
k = int(input("k\n"))
message = input("m\n")
enc1, enc2 = eelgamal(y,p,g,k,message)
print(enc1)
print(enc2)
decrypted = delgamal(x,p,enc1,enc2)
print(decrypted)


print("paillier")
p = int(input("p\n"))
q = int(input("q\n"))
g = int(input("g\n"))
n, yss, myu = paillierkey(p,q,g)
print(n)
print(yss)
print(myu)
r = int(input("r\n"))
message = input("m\n")
enc = epaillier(p,g,n,r,message)
print(enc)
decrypted = dpaillier(p,n,yss,myu,enc)
print(decrypted)
'''