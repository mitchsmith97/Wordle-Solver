import csv
import os
import re


cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))

file_list = ['Aword.csv', 'Bword.csv', 'Cword.csv', 'Dword.csv', 'Eword.csv', 'Fword.csv', 'Gword.csv', 'Hword.csv', 'Iword.csv', 'Jword.csv', 'Kword.csv', 'Lword.csv', 'Mword.csv', 'Nword.csv', 'Oword.csv', 'Pword.csv', 'Qword.csv', 'Rword.csv', 'Sword.csv', 'Tword.csv', 'Uword.csv', 'Vword.csv', 'Wword.csv', 'Xword.csv', 'Yword.csv', 'Zword.csv']

with open('/Users/Mitch/Downloads/Wordle-Solver/Word lists in csv/new.csv', 'w') as newfile:
    for file_name in file_list:
        with open('/Users/Mitch/Downloads/Wordle-Solver/Word lists in csv/' + file_name) as csvfile:
            next(csvfile)
            for row in csvfile:
                if len(row) == 7 and not re.search("[\"\'?#]", row) and row[2] != ' ':
                    newfile.write(row)