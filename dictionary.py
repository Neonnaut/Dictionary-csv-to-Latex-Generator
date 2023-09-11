import csv
import os
from datetime import datetime

import document

def create_section(section_char, has_ender=False):
    ender = '%\\end{multicols}'+'\n'+'\\end{hangparas}'+'\n'+'%\\newpage' if has_ender else ''
    return ender + '\n'+'\\section*{'+section_char.capitalize()\
    + '}%--------- SECTION ' + section_char.capitalize()\
    + '\n'+'%\\begin{multicols}{2}'\
    + '\n\\begin{hangparas}{.2in}{1}'+'\n\n'
    

from pyuca.collator import Collator
collator = Collator('pyuca/allkeys.txt')

language = 'Conlang Name'
author = 'John Smith'
inputFilename = 'lexicon.csv'

# Extra letters - digraphs - in the language, that will form a category of words
extraLetters = ['ch',"p'", "t'", "k'", 'ʎ', 'ʔ', 'ʙ', 'ʦ', 'ʣ']

darkTheme = 'y'
hasHeader = 'y'

outputFilename = f'{language.replace(" ", "_")}_dictionary.tex'
f_old_char = ''
f_cur_char = ''
s_old_char = ''
s_cur_char = ''
index_letter = ''

VARS = """
\\def\\myAuthor{"""+author+"""}
\\def\\myDate{"""+datetime.today().strftime('%A %d %B %Y')+"""}
\\def\\myLanguage{"""+language+"""}
"""

if darkTheme.casefold() in ['y','yes']:
    THEME = document.DARKTHEME
else:
    THEME = document.LIGHTTHEME

LEXICON = ''
startOfList = True
with open(inputFilename, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    if hasHeader.casefold() in ['y','yes']:
        next(reader, None)
    your_list = list(reader)

    your_list = sorted(your_list, key=collator.sort_key)
    #your_list = sorted(your_list, key=operator.itemgetter(0))
    for row in your_list:
        num = 0
        for i in row:
            if (num == 0):
                if row[num] != '':
                    # get up to the first character in the first item in the list
                    f_cur_char = row[0][:1]
                    s_cur_char = row[0][:2]
                    index_letter = ''

                    if s_old_char != s_cur_char:
                        if s_cur_char in extraLetters:
                            if your_list[0] == row:
                                index_letter = create_section(s_cur_char)
                                startOfList = False
                            else:
                                index_letter = create_section(s_cur_char,True)
                            s_old_char = s_cur_char
                        elif f_old_char != f_cur_char:
                            if your_list[0] == row:
                                index_letter = create_section(f_cur_char)
                            else:
                                index_letter = create_section(f_cur_char,True)
                            f_old_char = f_cur_char
                    row[num] = '\\entry' + '{' + row[num] + '}'
                    row[num] = index_letter + row[num]
            elif (num == 5):
                if row[num] != '':
                    row[num] = '\\two' + '{' + row[num] + '}'
                else:
                    row[num] = ''
            else:
                row[num] = '{' + row[num] + '}'
            num += 1
        line = ''.join(row) + '\n\n'
        LEXICON += line
LEXICON = "\\begin{multicols}{2}\n" + LEXICON +\
"""\\end{hangparas}
\\end{multicols}
\\clearpage"""

with open(outputFilename, 'w', encoding='utf-8') as myFile:
    myFile.write(document.PREAMBLE)
    myFile.write(VARS)
    myFile.write(THEME)
    myFile.write(document.COMMANDS)
    myFile.write(document.TITLE)
    myFile.write(document.LEXICON_PREAMBLE)
    myFile.write(LEXICON)
    myFile.write('\\end{document}')

os.system(f'xelatex {outputFilename}')
os.system(f'xelatex {outputFilename}')
print(f'Made {outputFilename}')
