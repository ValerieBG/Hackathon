from random import random

print("Hello! I'm your therapyst! How are you feeling today?")

userresp = input()

while userresp != "Q":
    print("wow vv interesting. tell me more! (Q to end session)")
    randnum = random()
    if randnum > .8:
        print("also btw u suck haha")
    userresp = input()

print("hope you enjoyed your session!")
