from argparse import Action
import csv
from selenium import webdriver
from pyshadow.main import Shadow
from random import choice
from selenium.webdriver.common.action_chains import ActionChains
import time


def create_word_list():
    filename = open('/Users/Mitch/Downloads/Wordle-Solver/python_code/new.csv', 'r')
    file = csv.reader(filename, delimiter=' ')
    word_list = []

    for row in file:
        word_list.append(row[0])
    return(word_list)

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

def close_overlay(driver):
    button = driver.execute_script('return document.querySelector("game-app").shadowRoot.querySelector("game-theme-manager").querySelector("#game").querySelector("game-modal").shadowRoot.querySelector("div.overlay > div.content > div.close-icon > game-icon").shadowRoot.querySelector("svg")')

    time.sleep(.2)
    ActionChains(driver).move_to_element(button).click(button).perform()

def turnOnHardMode(driver):
    time.sleep(.25)
    button = driver.execute_script('return document.querySelector("game-app").shadowRoot.querySelector("game-theme-manager").querySelector("header > div.menu-right").querySelector("#settings-button > game-icon").shadowRoot.querySelector("svg")')
    ActionChains(driver).move_to_element(button).click(button).perform()
    time.sleep(.25)
    switch = driver.execute_script('return document.querySelector("game-app").shadowRoot.querySelector("game-theme-manager > #game > game-page > game-settings").shadowRoot.querySelector("div.sections > section > div.setting > div.control > game-switch").shadowRoot.querySelector("div.container > div.switch > span")')
    ActionChains(driver).move_to_element(switch).click(switch).perform()
    time.sleep(.25)
    close_out_settings = driver.execute_script('return document.querySelector("game-app").shadowRoot.querySelector("game-theme-manager > #game > game-page").shadowRoot.querySelector("div.overlay > div.content > header > game-icon").shadowRoot.querySelector("svg")')
    ActionChains(driver).move_to_element(close_out_settings).click(close_out_settings).perform()

    return()


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


def expand_shadow_element(element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root


def keyboard_input(driver, row, key):
    button = driver.execute_script('return document.querySelector("game-app").shadowRoot.querySelector("game-theme-manager").querySelector("#game").querySelector("game-keyboard").shadowRoot.querySelector("div").querySelectorAll("div.row")[' + row + '].querySelector("button[data-key=' + key + ']")')
    button.click()
    driver.implicitly_wait(1)
    return()

def retrieve_evaluations(driver, guess_number):
    eval_list = []
    for i in range(0,5):
        tile = driver.execute_script('return document.querySelector("game-app").shadowRoot.querySelector("game-theme-manager > #game > #board-container > #board").querySelectorAll("game-row")[' + str(guess_number-1) + '].shadowRoot.querySelector("div.row").querySelectorAll("game-tile")[' + str(i) + '].getAttribute("evaluation")')
        eval_list.append(tile)
    return(eval_list)
        


            
def enter_guess(guess, driver, shadow):
    row_0 = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']
    row_1 = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']
    row_2 = ['z', 'x', 'c', 'v', 'b', 'n', 'm']
    row = '0'
    
    for letter in range(len(guess)):
        if guess[letter] in row_0:
            row = '0'
        elif guess[letter] in row_1:
            row = '1'
        elif guess[letter] in row_2:
            row = '2'

        keyboard_input(driver, row, guess[letter])
        # button = driver.execute_script('return document.querySelector("game-app").shadowRoot.querySelector("game-theme-manager").querySelector("#game").querySelector("game-keyboard").shadowRoot.querySelector("div").querySelectorAll("div.row")[' + row + '].querySelector("button[data-key=' + guess[letter] + ']")')
    
    row = '2'
    enter = '↵'
    keyboard_input(driver, row, enter)
    #button = driver.execute_script('return document.querySelector("game-app").shadowRoot.querySelector("game-theme-manager").querySelector("#game").querySelector("game-keyboard").shadowRoot.querySelector("div").querySelectorAll("div.row")[' + row + '].querySelector("button[data-key=' + enter + ']")')
    return()





if __name__ == "__main__":
    word_bank = create_word_list()
    driver = webdriver.Chrome()    #('C:\Users\Mitch\AppData\Local\ChromeDriver')
    driver.get("https://www.powerlanguage.co.uk/wordle/")
    #root1 = driver.find_element(By.XPATH, "/html/body/game-app")
    #print(root1.text)
    shadow = Shadow(driver)
    shadow.set_explicit_wait(50, 10)

    close_overlay(driver)

    

    turnOnHardMode(driver)

    actual_words = list_builder()
    letter_frequency_list = letter_frequency_counter(actual_words)
    sorting_aid = letter_frequency_sorter(actual_words, letter_frequency_list)
    sorted_words = zip_and_sort(actual_words, sorting_aid)

    word_list = sorted_words
    solved = False
    tries = 1
    guess =  choice(word_list[-20:])  
    
    
    #print(guess)
    while not solved:
        enter_guess(guess, driver, shadow)
        time.sleep(2)
        letter_info = retrieve_evaluations(driver, tries)
        
        # wrapped = wrapper(letter_tester, guess, actual_word)
        #print(timeit.timeit(wrapped, number=100000))

        #print("There are " + str(len(word_list)) + " possible words remaining")
        
        if 'present' not in letter_info and 'absent' not in letter_info:
            solved = True
            print("Solved!")
            #print('Solved- Word is ' + guess + ' It took ' + str(tries) + ' tries')
            

        else:
            word_list = word_remover(word_list, letter_info, guess)
            letter_frequency_list = letter_frequency_counter(word_list)
            sorting_aid = letter_frequency_sorter(word_list, letter_frequency_list)
            word_list = zip_and_sort(word_list, sorting_aid)
            guess = word_list[-1]
            tries += 1
            #guess = random.choice(word_list)
            

    #letter = 'y'
    #root1 = driver.execute_script('return document.querySelector("game-app").shadowRoot.querySelector("game-theme-manager").querySelector("#game").querySelector("game-keyboard").shadowRoot.querySelector("div").querySelector("div").querySelector("button[data-key=' + letter + ']")')
    #root1.click()

    #element = shadow.find_element(By.XPATH, "game_theme_manager")
    #text = element.text

#    root1 = driver.find_element(By.XPATH, "/html/body/game-app")
#    shadow_root1 = expand_shadow_element(root1)
#    shadow.set_explicit_wait(20, 5)
#    root2 = shadow_root1.find_element(By.TAG_NAME, 'game-theme-manager')
#    shadow_root2 = expand_shadow_element(root2) """