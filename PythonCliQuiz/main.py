import os
import sys
import random
import msvcrt
import time 
import csv


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def delete_last_line():
    "Use this function to delete the last line in the STDOUT"

    #cursor up one line
    sys.stdout.write('\x1b[1A')

    #delete last line
    sys.stdout.write('\x1b[2K')

def delete_n_lines(n):
    for i in range(n):
        delete_last_line()

def exit_sequence():
    print("Goodbye", end="", flush=True)
    for _ in range(5):
        time.sleep(0.2)
        print(".", end="", flush=True)
    sys.exit()

with open("quiz.csv", newline ='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    questions = list(reader)



score = 0    
print("Welcome to the quiz game, to continue press any key, to exit press Esc")
delete_last_line()
key = msvcrt.getch()
if key == b'\r':
    print("To input your answer press the corrosponding letter, press any key if you understand the rules")
    delete_last_line()
if key == b'\x1b':
    exit_sequence()


lines_to_del = 0
while True:
    lines_to_del = 0
    key = msvcrt.getch()
    if key == b'\x1b':
        exit_sequence()
    print("Score:", score)    
    randomQuestion = random.choice(questions)
    print(randomQuestion["question"])
    print("A)", randomQuestion["optionA"])
    print("B)", randomQuestion["optionB"])
    print("C)", randomQuestion["optionC"])
    print("D)", randomQuestion["optionD"])

    lines_to_del += 6

    while True:
        key = msvcrt.getch()
        lines_to_del += 3
        ans = None
        if key in [b'a', b'A']:
            print("You pressed A")
            ans = 'A'
            break
        elif key in [b'b', b'B']:
            print("You pressed B")
            ans = 'B'
            break
        elif key in [b'c', b'C']:
            print("You pressed C")
            ans = 'C'
            break
        elif key in [b'd', b'D']:
            print("You pressed D")
            ans = 'D'
            break
        else:
            if key == b'\x1b':
                exit_sequence()
            print("Please input a valid answer")

    if ans == randomQuestion["answer"]:
        print("Which is the correct answer, congratulations, your score increased by 10")
        score += 10
    else:
        print("Which is not the correct answer, unfortunately, your score will stay the same")
    delete_n_lines(lines_to_del)
    

    
    
