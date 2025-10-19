from sympy import primerange
import random

primes = list(primerange(50000, 100000))
fermat_primes = [3, 5, 17, 257, 65537]

def find_d(euler: int, e: int) -> int:
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, y = extended_gcd(e, euler)
    if gcd != 1:
        raise ValueError("e и φ(n) не взаимно просты")
    return x % euler

        
def create_key(first_prime_num:int,second_prime_num:int)->dict:
    if(first_prime_num==second_prime_num):
        raise Exception("first !=second")
    n=first_prime_num*second_prime_num
    euler_func=(second_prime_num-1)*(first_prime_num-1)
    if(euler_func<3):
        raise Exception("enter another numbers")
    
    e:int=0
    d:int=0
    for i in range (0,len(fermat_primes)):
        e=fermat_primes[i]
        try:
            d=find_d(euler_func,e)
            break  
        except:
            continue
    return {'open': (e,n), 'close':(d,n)}

     

def encryption(open_key,mess:int)->int:
      return pow(mess,open_key[0],open_key[1])
  
def decryption(close_key,encr:int)->int:
    return pow(encr,close_key[0],close_key[1])


def text_to_number(text):
    number = 0
    for char in text:
        number = (number << 8) + ord(char) 
    return number


def encryption_for_signature(close_key,mess:int):
    return pow(mess,close_key[0],close_key[1])
def check_signature(open_key,encrypted_sign)->int:
      return pow(encrypted_sign,open_key[0],open_key[1])
  
if __name__=="__main__":
    try:        
        keys=create_key(primes[random.randint(1,5)],primes[random.randint(6,10)])
        
    except:
        keys=create_key(primes[random.randint(1,10)],primes[random.randint(1,10)])
    print(f"Enter number to encrypt(<{keys['open'][1]-1}):")
    num:int
    num=int(input())
    encrypted=encryption(keys["open"],num)
    decrypted=decryption(keys['close'],encrypted)
    print(f"Encrypted:{encrypted}\nDecrypted:{decrypted}\n")
    
    print("Enter message for secret signature:")
    mess_for_signature:str
    mess_for_signature= input()
    encrypted_sign:int=encryption_for_signature(keys["close"],text_to_number(mess_for_signature))
    print(f"Signature message:{text_to_number(mess_for_signature)%keys['open'][1]}")
    print(f"Encrypted signature:{encrypted_sign}")
    print(f"Decryption:{check_signature(keys['open'],encrypted_sign)}")