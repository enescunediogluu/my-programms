# password creator
import random
import string
 
numbers = '0123456789'
symbols = '_-/#&^!'
wordsUpper = string.ascii_uppercase
wordsSmall = string.ascii_lowercase
password = []

def pick(list):
    for i in range(3):
        a = random.choice(list)
        password.append(a)
        i += 1

pick(numbers)
pick(wordsSmall)
pick(symbols)
pick(wordsUpper)

for i in range(11):      
    toplam = str(0)
    toplam += password[i]
    i += 1

random.shuffle(password)
random.shuffle(password)

print("here is your password :")
print(''.join(password))


