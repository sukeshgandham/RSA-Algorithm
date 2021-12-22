import random
import math
from types import CodeType, UnionType


#Generates p,q,N,e,d
def key_generation():
    p = gene_randomprime()
    print ("\n 16 bit prime number generated at random (p): ",p)

    q = gene_randomprime()
    print ("\n 16 bit prime number generated at random (q): ",q)

    
    N=p*q
    print ("\n Computed N = p*q =",N)

    #calculating ϕ(n) 
    Phi = (p-1)*(q-1)
    print ("\n the computed value of ϕ(n) = (p-1)*(q-1) =",Phi)

    e = generate_rand_val_e(Phi)
    print("\n The Generated value of ϕ(n) is:", Phi)
    print("\n The randomly generated value if e is: ", e)

    d= cal_mod_inverse(e,Phi)
    print ("The computed d : =",d)


def gene_randomprime():
    while(1):
      intd = 0
      int_prime_numb = random.randint(32769, 65535) # Considering 16 bit integer, in the range signed bit ushort 32768, short 65535
      for i in range(1, int_prime_numb):
         if (int_prime_numb % i == 0):
            intd= intd+1
      if (intd ==1):
         return int_prime_numb



def generate_rand_val_e(Phi):
  while(1):
      varphi= round(Phi/2)
      e = random.randint(3, varphi)
      e = (e*2) +1
      if (e%2 == 1 and e < Phi):
         x = Phi
         y = e
         while(y):
             x,y = y, x%y
             if(y == 1):
                 return e



#This method calculates the secret key "d", such that (e*d) mod Phi(N)=1
def cal_mod_inverse(e, aPhi) : 
    m0 = aPhi 
    y = 0
    x = 1
  
    if (aPhi == 1) : 
        return 0
  
    while (e > 1) : 

        q = e // aPhi 
        t = aPhi 
        aPhi = e % aPhi 
        e = t 
        t = y 
        y = x - q * y 
        x = t   
   
    if (x < 0) : 
        x = x + m0 
    return x  



#Start the encryption here.
def start_encryption():

     print("Enter Your Partner's Public Key N:")
     strN = int(input())
     print("Enter Your Partner's Public Key e:")
     strE = int(input())
     print("Please enter the message you want to enrypt seperated by spaces")
     strmsgtoencrypt = str(input())
     char_array = []
     arr_msg = []
     strbuilder = ''
     for i in range(0, len(strmsgtoencrypt), 3):
        if (len(strmsgtoencrypt) - i > 3): 
            substring = strmsgtoencrypt[i:i+3]
            char_array.append(substring)
        else:
            substring = strmsgtoencrypt[i :]
            char_array.append(substring)
     print(char_array)
     for x in char_array:
        messages = perform_encryption(x, strN, strE)
        arr_msg.append(messages)
     for i in arr_msg:
        strbuilder = strbuilder+str(i)+','
     strbuilder = strbuilder[0:-1]
     print('['+strbuilder+']')

#Used to perform encryption 
def perform_encryption(str, N, e):
     strbuilder = ''
     for i in str:
        ascii = ord(i)
        strhex=hex(ascii)
        strbuilder +=strhex.replace('0x','')
     value = int(strbuilder,16)
     squrmult2=squaremult(value,e,N)
     return squrmult2

#Used to perform decryption
def start_decryption():
     print("Enter Your Public Key N:")
     stringN = int(input())
     print("Enter Your Private key d:")
     stringD = int(input())
     print("Please enter the message you want to Decrypt")
     msg_array = []
     values = str(input()).split(",") 
     for i in values:
        msg_chunk = int(i)
        decryp_msg = perform_decryption(msg_chunk, stringD, stringN)
        msg_array.append(decryp_msg)
     print(msg_array)
     concat = ''.join(msg_array)
     print(concat)

def perform_decryption(str, D, N):
    strbuilder=''
    decryptedMessage = squaremult(str, D, N)
    strhex = hex(decryptedMessage)
    strbuilder +=strhex.replace('0x','')
    strbytes = bytes.fromhex(strbuilder)
    dec_message = strbytes.decode("ASCII")
    return dec_message

#Used to convert string to hexadecimal
#args: string:hex
def hexstring(arghex):
    if arghex[:2] == '0x':
        strhex = arghex[2:]
        stringhexdecval = bytes.fromhex(strhex).decode('utf-8')
    return stringhexdecval


#Used to perform square nd multiply
#args : str,e,N (string)
def squaremult(str,e,N):

    str_msg_encrypt = 1
    while e > 0:
        if e % 2 == 1:
            str_msg_encrypt = (str_msg_encrypt * str) % N
        e = e // 2  
        str = (str * str) % N

    return str_msg_encrypt

#Used to create signature
def create_Signature():
     strsba =''
     print("Enter your Public key N")
     stringN = int(input())
     print("Enter your Private key D below:")
     stringE = int(input())
     print(" Enter Your Signature to be encrypted")
     struimsg = str(input())
     arr_msg = []
     arr_data=[]
     for i in range(0, len(struimsg), 3):
        if (len(struimsg) - i > 3): 
            substring = struimsg[i:i+3]
            arr_msg.append(substring)
        else:
            substring = struimsg[i :]
            arr_msg.append(substring)
     print(arr_msg)
     for x in arr_msg:
        strmsg= perform_encryption(x, stringN, stringE)
        arr_data.append(strmsg)
     for i in arr_data:
        strsba= strsba+str(i)+','
     strsba = strsba[0:-1]
     print('The Encrypted signature is as follows: ')
     print('['+strsba+']')


#Used to perform the signature verification

def perform_verification():
     print("Please enter the Partner's Public key N")
     intN = int(input())
     print("Please enter the Partner's Public key e")
     intD = int(input())
     print("Please enter the patners sign : ")
     strsign = str(input())
     print("Please enter the patners ecrypted signature : ")
     arr_messages = []
     values = str(input()).split(",") 
     for i in values:
        int_msg = int(i)
        msg = perform_decryption(int_msg, intD, intN)
        arr_messages.append(msg)
     concat = ''.join(arr_messages)
     if(strsign == concat):
         print('Signature is verified')
     else:
         print('Signature is not verified')
     print(concat)


print('Key Generation,Encryption and decryption is done here')
print('select: \n 1 Key generation \n 2 for Encryption \n 3 for Decryption \n 4 for Signature \n 5 for verifying signature')
selection = int(input())
if selection ==1:
    key_generation()
if selection ==2:
    start_encryption()
if selection ==3:
    start_decryption()
if selection ==4:
    create_Signature()
if selection ==5:
    perform_verification()
else:
    print('select a valid option')