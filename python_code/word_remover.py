import csv
import random
import timeit
from matplotlib import pyplot as plot

def wrapper(func, *args, **kwargs):
    def wrapped():
         return func(*args, **kwargs)
    return wrapped



def alternate_sorter(word_list):
    words_removed_totals = []
    sim_percent_comp = 0
    for word in word_list:
        editable_word_list = word_list[:]
        words_removed = 0
        for i in range(0, len(word)):
            for editable_word in editable_word_list:
                if word[i] in editable_word:
                    words_removed = words_removed + 1
                    editable_word_list.remove(editable_word)
                    
                    
        words_removed_totals.append(words_removed)
        sim_percent_comp += 1
    #print(words_removed_totals)
    return(words_removed_totals)



def zip_and_sort(unsorted_list, sort_values):
    zipped_lists = zip(sort_values, unsorted_list)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    sort_values, sorted_list = [ list(tuple) for tuple in  tuples]
    return(sorted_list)
        


def letter_frequency_counter(word_list):
    letter_frequency_list = [0]*26
    
    for word in word_list:
        for i in range(0, len(word)):
            letter_frequency_list[ord(word[i])-97] = letter_frequency_list[ord(word[i])-97] + 1

    return(letter_frequency_list)

def letter_frequency_sorter(word_list, letter_frequency_list):
    word_list_corresponding_value = []
    unsorted_list = word_list[:]
    for word in word_list:
        word_letter_value = 0
        safe_letters = []
        for i in range(0, len(word)):
            if word[i] not in safe_letters:
                word_letter_value += letter_frequency_list[ord(word[i])-97]
                safe_letters.append(word[i])
        

        word_list_corresponding_value.append(word_letter_value)

    return(word_list_corresponding_value)




def list_builder():
    list_of_potential_words = []
    with open('/Users/Mitch/Downloads/Wordle-Solver/python_code/' + "just_the_potential_words.txt") as file:
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
                if guess[letter_in_word] not in word or guess[letter_in_word] == word[letter_in_word]:
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

# Manual Entry Test, replaced by automated test 
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
#if __name__ == "__main__":
    actual_words = list_builder()
    letter_frequency_list = letter_frequency_counter(actual_words)
    sorting_aid = letter_frequency_sorter(actual_words, letter_frequency_list)
    sorted_words = zip_and_sort(actual_words, sorting_aid)

    list_of_average_tries = []
    tries_tally = 0
    best_average = 20.0
    best_word = 'not a real word'
    subset_of_words = actual_words[:]
    sim_percent_comp = 0
    best_words = sorted_words[-40:]
    for starting_guess in best_words:
        
        print(str((sim_percent_comp/len(best_words))*100) + ' percent complete')
        guess = starting_guess
        

        for actual_word in subset_of_words:
            word_list = sorted_words[:]
            #print("There are " + str(len(word_list)) + " possible words remaining")
            solved = False
            tries = 1
            #guess = 'react'#word_list[-1]
            #print(guess)
            while not solved:
                letter_info = letter_tester(guess, actual_word)
                word_list = word_remover(word_list, letter_info, guess)
                # wrapped = wrapper(letter_tester, guess, actual_word)
                #print(timeit.timeit(wrapped, number=100000))

                #print("There are " + str(len(word_list)) + " possible words remaining")
                
                if guess == actual_word:
                    solved = True
                    #print('Solved- Word is ' + guess + ' It took ' + str(tries) + ' tries')
                    tries_tally += tries
                    
                    guess = starting_guess

                else:
                    tries += 1
                    #guess = random.choice(word_list)
                    letter_frequency_list = letter_frequency_counter(word_list)
                    sorting_aid = letter_frequency_sorter(word_list, letter_frequency_list)
                    word_list = zip_and_sort(word_list, sorting_aid)
                    guess = word_list[-1]
        
        print("Starting word = " + starting_guess + " : " + "Average tries: " + str(tries_tally/len(subset_of_words)))
        list_of_average_tries.append(tries_tally/len(subset_of_words))

        tries_tally = 0
        sim_percent_comp += 1
    
    x = range(0, len(list_of_average_tries))
    plot.scatter(x, list_of_average_tries)
    plot.xlabel('Sorted Starting Guesses')
    plot.ylabel('Average Guesses to Solve')
    plot.title('Sort Everytime')
    plot.show()

"""  if (tries_tally/len(subset_of_words)) < best_average:
        best_word = starting_guess
        best_average = tries_tally/len(subset_of_words)
        
    tries_tally = 0
    sim_percent_comp += 1
    print("Best word so far is " + str(best_word) + " which took an average of " + str(best_average) + ' tries')
"""       
    


if __name__ == "__main__":
    actual_words = list_builder()
    letter_frequency_list = letter_frequency_counter(actual_words)
    sorting_aid = alternate_sorter(actual_words)
    sorted_words = zip_and_sort(actual_words, sorting_aid)
    print(sorted_words)
    sim_percent_comp = 0

    subset_of_words = actual_words[:]
    tries_tally = 0

    for actual_word in subset_of_words:
        word_list = sorted_words[:]
            #print("There are " + str(len(word_list)) + " possible words remaining")
        solved = False
        tries = 1
        guess = word_list[-1]
        print(str((sim_percent_comp/len(subset_of_words))*100) + ' percent complete')
        #print(guess)
        while not solved:
            letter_info = letter_tester(guess, actual_word)
            word_list = word_remover(word_list, letter_info, guess)
            # wrapped = wrapper(letter_tester, guess, actual_word)
            #print(timeit.timeit(wrapped, number=100000))

            #print("There are " + str(len(word_list)) + " possible words remaining")
            
            if guess == actual_word:
                solved = True
                #print('Solved- Word is ' + guess + ' It took ' + str(tries) + ' tries')
                tries_tally += tries
                

            else:
                tries += 1
                #guess = random.choice(word_list)
                sorting_aid = alternate_sorter(word_list)
                word_list = zip_and_sort(word_list, sorting_aid)
                guess = word_list[-1]

        sim_percent_comp += 1
    
    print("Average tries: " + str(tries_tally/len(subset_of_words)))


    tries_tally = 0
    sim_percent_comp += 1