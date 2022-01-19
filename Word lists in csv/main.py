import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pyshadow.main import Shadow




def create_word_list():
    filename = open('/Users/Mitch/Downloads/Wordle-Solver/Word lists in csv/new.csv', 'r')
    file = csv.reader(filename, delimiter=' ')
    word_list = []

    for row in file:
        word_list.append(row[0])
    return(word_list)


def word_remover(words, letter_info, guess):
    letter_in_word = 0
    for letter in letter_info:
        if letter == 'correct':
            for word in words:
                if word[letter_in_word] != guess[letter_in_word]:
                    words.remove(word)
        elif letter == 'present':
            for word in words:
                if guess[letter_in_word] not in word:
                    words.remove(word)

        elif letter == 'absent':
            if guess[letter_in_word] in word:
                words.remove(word)
        
        letter_in_word += 1

    return(words)

            





if __name__ == "__main__":
    word_bank = create_word_list()
    driver = webdriver.Firefox()
    driver.get("https://www.powerlanguage.co.uk/wordle/")
    shadow = Shadow(driver)
    element = shadow.find_element(By.XPATH, 'game-keyboard')