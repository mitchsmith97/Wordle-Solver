import csv
import random


def list_builder():
    list_of_potential_words = []
    with open('/Users/Mitch/Downloads/Wordle-Solver/Word lists in csv/' + "just_the_potential_words.txt") as file:
            for row in file:
                row = (row.split(","))
                for word in row:
                    word = word.strip('"')
                    list_of_potential_words.append(word)

    return(list_of_potential_words)


def safe_letter_check(letter_info, guess):
    safe_letters = []
    letter_in_word = 0
    for letter in guess:
        if letter_info[letter_in_word] == 'correct' or letter_info[letter_in_word] == 'present' and guess[letter_in_word] not in safe_letters:
            safe_letters.append(guess[letter_in_word])
        
        letter_in_word += 1

    return(safe_letters)

def letter_tester(guess, actual_word):
    letter_info = []
    letter = 0
    for letter in range(len(guess)):
        if guess[letter] == actual_word[letter]:
            letter_info.append("correct")

        elif guess[letter] not in actual_word:
            letter_info.append("absent")

        elif guess[letter] in actual_word:
            letter_info.append('present')

        letter += 1

    return(letter_info)



def word_remover(words, letter_info, guess):
    letter_in_word = 0
    safe_letters = safe_letter_check(letter_info, guess)
    for letter in letter_info:
        if letter == 'correct':
            for word in words[:]:
                if word[letter_in_word] != guess[letter_in_word]:
                    words.remove(word)
        elif letter == 'present':
            for word in words[:]:
                if guess[letter_in_word] not in word:
                    words.remove(word)

        elif letter == 'absent' and guess[letter_in_word] not in safe_letters:
            for word in words[:]:
                if guess[letter_in_word] in word:
                    words.remove(word)

        elif letter == 'absent' and guess[letter_in_word] in safe_letters:
            if word[letter_in_word] == guess[letter_in_word]:
                words.remove(word)
        
        letter_in_word += 1

    return(words)

def create_word_list():
    filename = open('/Users/Mitch/Downloads/Wordle-Solver/Word lists in csv/new.csv', 'r')
    file = csv.reader(filename, delimiter=' ')
    word_list = []

    for row in file:
        word_list.append(row[0])
    return(word_list)


#if __name__ == "__main__":
    word_list = create_word_list()
    print("There are " + str(len(word_list)) + " possible words remaining")
    guess = input("Input word pls ")
    print('/n')
    while True:
        letter_info = input("correct, present, or absent separated by space ")
        letter_info = letter_info.split()
        word_list = word_remover(word_list, letter_info, guess)
        print("There are " + str(len(word_list)) + " possible words remaining")
        print(word_list)
        guess = random.choice(word_list)
        print(guess)
if __name__ == "__main__":
    actual_words = list_builder()
    tries_tally = 0
    for actual_word in actual_words:
        word_list = list_builder()
        #print("There are " + str(len(word_list)) + " possible words remaining")
        solved = False
        tries = 1
        guess = random.choice(word_list)
        #print(guess)
        while not solved:
            letter_info = letter_tester(guess, actual_word)
            word_list = word_remover(word_list, letter_info, guess)
            #print("There are " + str(len(word_list)) + " possible words remaining")
            guess = random.choice(word_list)
            if guess == actual_word:
                solved = True
                print('Solved- Word is ' + guess + ' It took ' + str(tries) + ' tries')
                tries_tally += tries

            else:
                tries += 1
            
    print("Average tries: " + str(tries_tally/len(actual_words)))
