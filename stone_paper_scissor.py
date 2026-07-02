import random
print("Stone, Paper, Scissor Game")
options = ["stone","paper","scissor"]
user = input("enter your choice: " ).lower()
computer = random.choice(options)
print("computer: ",computer)

# Tie Case
if(computer == user):
    print("Game is Tie")

# Winning Case
elif(computer == 'scissor' and user == 'stone'):
    print('You Win')
elif(computer == 'stone' and user == 'paper'):
    print('You win')        
elif(computer == 'paper' and user == 'scissor'):
    print('You win')

# Loosing case
elif(computer == 'stone' and user == 'scissor'):
    print('You Loose')
elif(computer == 'paper' and user == 'stone'):
    print('You Loose')                     
elif(computer == 'scissor' and user == 'paper'):
    print('You Loose')
else:
    print('Invalid input')         
print('Thankyou for Playing the game ')    