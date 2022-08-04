import csv
import operator
import os
from datetime import datetime as dt

conlang = "Conlang Name"
author = "John Smith"
inputFilename = 'lexicon.csv'

# Extra-ASCI letters in the language that will form a category of words
extraLetters = ["p'", "t'", "k'", "ʎ", "ʔ", "ʙ", "ʦ", "ʣ"]

darkTheme = input("Use dark theme? (y/n) ")
hasHeader = input("Does the csv file have a header? (y/n) ")

outputFilename = conlang.replace(" ", "_")+'_dictionaryx.tex'
timeNow = dt.today().strftime('%A %d %B %Y')
f_old_char = ""
f_cur_char = ""
s_old_char = ""
s_cur_char = ""
index_letter = ""

startOfList = True
with open(inputFilename, 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    if hasHeader == "y":
        next(reader, None)
    your_list = list(reader)
    document = ""
    your_list = sorted(your_list, key=operator.itemgetter(0))
    for row in your_list:
        num = 0
        for i in row:
            if (num == 0):
                if row[num] != "":
                    # get up to the first character in the first item in the list
                    f_cur_char = row[0][:1]
                    s_cur_char = row[0][:2]
                    index_letter = ""

                    if s_old_char != s_cur_char:
                        if s_cur_char in extraLetters:
                            if your_list[0] == row:
                                index_letter = "\\section*{"+s_cur_char.upper(
                                ) + "}%--------- SECTION " + s_cur_char.upper(
                                ) + "\n"+"\\begin{multicols}{2}"+"\n\n"
                                startOfList = False
                            else:
                                index_letter = "\\end{multicols}"+"\n"+"%\\newpage"+"\n"+"\\section*{"+s_cur_char.upper(
                                ) + "}%--------- SECTION " + s_cur_char.upper(
                                ) + "\n"+"\\begin{multicols}{2}"+"\n\n"
                            s_old_char = s_cur_char
                        elif f_old_char != f_cur_char:
                            if your_list[0] == row:
                                index_letter = "\\section*{"+f_cur_char.upper(
                                ) + "}%--------- SECTION " + f_cur_char.upper(
                                ) + "\n"+"\\begin{multicols}{2}"+"\n\n"
                            else:
                                index_letter = "\\end{multicols}"+"\n"+"%\\newpage"+"\n"+"\\section*{"+f_cur_char.upper(
                                ) + "}%--------- SECTION " + f_cur_char.upper(
                                ) + "\n"+"\\begin{multicols}{2}"+"\n\n"
                            f_old_char = f_cur_char
                    row[num] = "\\entry" + "{" + row[num] + "}"
                    row[num] = index_letter + row[num]
            elif (num == 5):
                if row[num] != "":
                    row[num] = "\\two" + "{" + row[num] + "}"
                else:
                    row[num] = ""
            else:
                row[num] = "{" + row[num] + "}"
            num += 1
        line = "".join(row) + "\n\n"
        document = document + line
with open(outputFilename, 'a', encoding="utf-8") as myFile:
    myFile.write('\\documentclass[12pt,a4paper,twoside]{article}\n')
    myFile.write(
        '\\usepackage[top=2.5cm,bottom=2.5cm,left=2.2cm,right=2.2cm,columnsep=22pt]{geometry}\n')
    myFile.write(
        '\\usepackage{fontspec}\n\\setmainfont{Charis SIL}\n\\newfontfamily\myfont[]{Broadway}\n')
    myFile.write('%\\usepackage{microtype} % Improves spacing\n')
    myFile.write(
        '\\usepackage[bf]{titlesec} % Required for modifying section titles - bold, sans-serif, centered\n')
    myFile.write(
        '\\usepackage{fancyhdr} % Required for modifying headers and footers\n')
    myFile.write('\\fancyhead[L]{\\rightmark} % Top left header\n')
    myFile.write('\\fancyhead[R]{\leftmark} % Top right header\n')
    myFile.write(
        '\\renewcommand{\headrulewidth}{1.4pt} % Rule under the header\n')
    myFile.write(
        '\\setlength{\headheight}{14.5pt}\n')
    myFile.write(
        '\\fancyfoot[C]{\\textsf{\\thepage\\ }} % Bottom center footer\n\n')
    myFile.write(
        '\\usepackage{multicol} % Required for splitting text into multiple columns\n')
    myFile.write('\\usepackage{ifthen} % provides \ifthenelse test\n')
    myFile.write('\\usepackage{xifthen} % provides \isempty test\n\n')

    boldColor = ''
    if darkTheme.casefold() == 'y':
        myFile.write('\\usepackage{xcolor}\n')
        myFile.write('\\pagecolor[rgb]{0.18,0.18,0.23} %black\n')
        myFile.write('\\color[rgb]{0.84,0.88,0.94} %grey\n\n')
        boldColor = 'white'

        myFile.write('\\usepackage{hyperref}')
        myFile.write('\\hypersetup{\n')
        myFile.write('colorlinks,')
        myFile.write('citecolor=white,')
        myFile.write('filecolor=white,')
        myFile.write('linkcolor=white,')
        myFile.write('urlcolor=white')
        myFile.write('}\n\n')
    else:
        myFile.write('\\usepackage{xcolor}\n')
        myFile.write('\\color[rgb]{0.18,0.18,0.18} %grey\n\n')
        boldColor = 'black'

        myFile.write('\\usepackage{hyperref}\n')
        myFile.write('\\hypersetup{\n')
        myFile.write('colorlinks,')
        myFile.write('citecolor=black,')
        myFile.write('filecolor=black,')
        myFile.write('linkcolor=black,')
        myFile.write('urlcolor=black')
        myFile.write('}\n\n')

    myFile.write(
        '\\newcommand{\\entry}[5]{\\textbf{\\color{' + boldColor + '}{#1}}\\markboth{#1}{#1}\\ [{\\color{' + boldColor + '}#2}]\\ \\textit{{#3}}\\ {\\color{' + boldColor + '}{#4}}\\\n')
    myFile.write('\\ifthenelse{\\isempty{#5}}\n')
    myFile.write('  {#5}  % if no title option given\n')
    myFile.write('{- {#5} }}\n\n')

    myFile.write('\\newcommand\\invisiblesection[1]{%\n')
    myFile.write('  \\refstepcounter{section}%\n')
    myFile.write(
        '  \\addcontentsline{toc}{section}{\\protect\\numberline{\\thesection}#1}\n')
    myFile.write('  \sectionmark{#1}}\n\n')

    myFile.write('%-----------------------------------------------------\n\n')

    myFile.write('\\begin{document}\n')
    myFile.write('\\title{' + conlang + '}\n')
    myFile.write('\\author{' + author + '}\n')
    myFile.write('\\date{' + timeNow + '}\n')
    myFile.write('\\begin{titlepage}\n')
    myFile.write('\\begin{center}\n')
    myFile.write('  \\vspace{10mm}\n')
    myFile.write('  \\vspace{40mm}\n')
    myFile.write('  \\vspace{10mm}\n')
    myFile.write(
        '  \\fontsize{10mm}{7mm}\\selectfont \\textup{' + conlang + '}\\\\\n')
    myFile.write('\\end{center}\n')

    myFile.write('\\vspace{25mm}\n')
    myFile.write('\\centering{\n')
    myFile.write('\\textnormal{\\large{\\bf Author:\\\\}}\n')
    myFile.write('{\\large ' + author + '\\\\ }\n')
    myFile.write('\\vspace{8mm}\n')
    myFile.write('\\textnormal{\\large{\\bf Last Modified:\\\\}}\n')
    myFile.write(
        '{\\large ' + timeNow + '\\\\}\n')
    myFile.write('\\hfill\n')
    myFile.write('}\n')
    myFile.write('\\end{titlepage}\n')

    myFile.write('\\tableofcontents\n')
    myFile.write('\\thispagestyle{empty}\n\n')
    myFile.write('\\clearpage\n')

    myFile.write('%-----------------------------------------------------\n\n')

    myFile.write(
        '\\pagestyle{fancy} % Use the custom headers and footers throughout the document\n')
    myFile.write('\\parindent=0em\n')
    myFile.write('\\leftskip 0.1in\n')
    myFile.write('\\parindent -0.1in\n\n')

    myFile.write('\\invisiblesection{Lexicon}\n')
    myFile.write(document)

    myFile.write('\\end{multicols}\n\\clearpage\n\\end{document}')

os.system(f"xelatex {outputFilename}")
os.system(f"xelatex {outputFilename}")
print(f"Made {outputFilename}")
