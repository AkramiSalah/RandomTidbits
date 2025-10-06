import random
import msvcrt
import time 

print("To toss the coin press Enter, to exit the program press Esc...")

frames = [" Heads", " Tails"]


while True:
    key = msvcrt.getch()
    if key == b'\r':
        res = random.choice(["Heads", "Tails"])
        print("Flipping the coin")
        for i in range(5):
            for f in frames:
                print(f"\r{f}", end = "", flush = True)
                time.sleep(0.2)
        print("\rYou got", res, "!")
        time.sleep(0.5)
        print("To toss the coin again press Enter or press Esc to exit the program press...")
    elif key == b'\x1b':
        print("I hope you won the bet, goodbye", end="", flush=True)
        for _ in range(5):
            time.sleep(0.2)
            print(".", end="", flush=True)
        
        break
    else:
        print("To toss the coin press Enter, to exit the program press Esc...")
        print("you pressed", key)
