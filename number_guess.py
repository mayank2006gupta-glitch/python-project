import random
n = random.randint(1,100)
a=0
guesses = 0
while(a!=n):
    guesses +=1
    a = int(input("enter a no.: "))
    if(a>n):
        print("enter small no.: ")
    else:
        print("enter greater no.: ")    
print(f"you have guessed the no. {n} in {guesses} attempts ")        