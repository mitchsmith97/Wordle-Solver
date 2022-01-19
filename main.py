import csv

file_list = [Aword.csv, Bword.csv, Cword.csv, Dword.csv, Eword.csv, Fword.csv, Gword.csv, Hword.csv, Iword.csv, Jword.csv, Kword.csv, Lword.csv, Mword.csv, Nword.csv, Oword.csv, Pword.csv, Qword.csv, Rword.csv, Sword.csv, Tword.csv, Uword.csv, Vword.csv, Wword.csv, Xword.csv, Yword.csv, Zword.csv]

with open('new.csv', 'w') as newfile:
    for file_name in file_list:
        with open(file_name) as csvfile:
            next(csvfile)
            for row in csvfile:
                if len(row) == 5:
                    print(row)