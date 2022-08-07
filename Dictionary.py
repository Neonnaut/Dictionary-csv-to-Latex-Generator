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


PREAMBLE = ""\
    + '\\documentclass[12pt,a4paper,twoside]{article}'\
    + '\n\\usepackage[top=2.5cm,bottom=2.5cm,left=2.2cm,right=2.2cm,columnsep=22pt]{geometry}'\
    + '\n\\usepackage{fontspec}\n\\setmainfont{Charis SIL}'\
    + '\n\\newfontfamily\myfont[]{Broadway}'\
    + '\n%\\usepackage{microtype} % Improves spacing'\
    + '\n\\usepackage[bf]{titlesec} % Required for modifying section titles - bold, sans-serif, centered'\
    + '\n\\usepackage{fancyhdr} % Required for modifying headers and footers'\
    + '\n\\fancyhead[L]{\\rightmark} % Top left header'\
    + '\n\\fancyhead[R]{\leftmark} % Top right header'\
    + '\n\\renewcommand{\headrulewidth}{1.4pt} % Rule under the header'\
    + '\n\\setlength{\headheight}{14.5pt}'\
    + '\n\\fancyfoot[C]{\\textsf{\\thepage\\ }} % Bottom center footer'\
    + '\n\\usepackage{multicol} % Required for splitting text into multiple columns'\
    + '\n\\usepackage{ifthen} % provides \ifthenelse test'\
    + '\n\\usepackage{xifthen} % provides \isempty test\n\n'

if darkTheme.casefold() == 'y':
    boldColor = 'white'
    PREAMBLE += ""\
        + '\n\\usepackage{xcolor}'\
        + '\n\\pagecolor[rgb]{0.18,0.18,0.23} %black'\
        + '\n\\color[rgb]{0.84,0.88,0.94} %grey\n\n'\
        + '\n\\usepackage{hyperref}'\
        + '\n\\hypersetup{'\
        + 'colorlinks,'\
        + 'citecolor=white,'\
        + 'filecolor=white,'\
        + 'linkcolor=white,'\
        + 'urlcolor=white'\
        + '}\n\n'
else:
    boldColor = 'black'
    PREAMBLE += ""\
        + '\\usepackage{xcolor}\n'\
        + '\\color[rgb]{0.18,0.18,0.18} %grey\n\n'\
        + '\n\\usepackage{hyperref}'\
        + '\n\\hypersetup{\n'\
        + 'colorlinks,'\
        + 'citecolor=black,'\
        + 'filecolor=black,'\
        + 'linkcolor=black,'\
        + 'urlcolor=black'\
        + '}\n\n'

PREAMBLE += ""\
    + '\\newcommand{\\entry}[5]{\\textbf{\\color{' + boldColor + '}{#1}}\\markboth{#1}{#1}\\ [{\\color{' + boldColor + '}#2}]\\ \\textit{{#3}}\\ {\\color{' + boldColor + '}{#4}}\\\n'\
    + '\\ifthenelse{\\isempty{#5}}\n'\
    + '  {#5}  % if no title option given\n'\
    + '{- {#5} }}\n\n'\
    + '\\newcommand{\\entrySmall}[3]{\\textbf{\\color{' + boldColor + '}{#1}}\\markboth{#1}{#1}\\ {\\color{white}{#2}}\\\n'\
    + '\\ifthenelse{\\isempty{#3}}\n'\
    + '  {#3}  % if no title option given\n'\
    + '{- {#3} }}\n\n'\
    + '\\newcommand\\invisiblesection[1]{%\n'\
    + '  \\refstepcounter{section}%\n'\
    + '  \\addcontentsline{toc}{section}{\\protect\\numberline{\\thesection}#1}\n'\
    + '  \sectionmark{#1}}\n\n'\
    + '  %-----------------------------------------------------\n\n'

TITLE = ''\
    + '\\begin{document}\n'\
    + '\\title{' + conlang + '}\n'\
    + '\\author{' + author + '}\n'\
    + '\\date{' + timeNow + '}\n'\
    + '\\begin{titlepage}\n'\
    + '\\begin{center}\n'\
    + '  \\vspace{10mm}\n'\
    + '  \\vspace{40mm}\n'\
    + '  \\vspace{10mm}\n'\
    + '  \\fontsize{10mm}{7mm}\\selectfont \\textup{' + conlang + '}\\\\\n'\
    + '\\end{center}\n'\
    + '\\vspace{25mm}\n'\
    + '\\centering{\n'\
    + '\\textnormal{\\large{\\bf Author:\\\\}}\n'\
    + '{\\large ' + author + '\\\\ }\n'\
    + '\\vspace{8mm}\n'\
    + '\\textnormal{\\large{\\bf Last Modified:\\\\}}\n'\
    + '{\\large ' + timeNow + '\\\\}\n'\
    + '\\hfill\n'\
    + '}\n'\
    + '\\end{titlepage}\n'\
    + '\\tableofcontents\n'\
    + '\\thispagestyle{empty}\n\n'\
    + '\\clearpage\n'\
    + '%-----------------------------------------------------\n\n'\

DOCUMENT = ""
startOfList = True
with open(inputFilename, 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    if hasHeader == "y":
        next(reader, None)
    your_list = list(reader)
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
        DOCUMENT = DOCUMENT + line
with open(outputFilename, 'a', encoding="utf-8") as myFile:

    myFile.write(PREAMBLE)

    myFile.write(TITLE)

    myFile.write('\\invisiblesection{Lexicon}\n')
    myFile.write('\\pagestyle{fancy} % Use the custom headers and footers\n')
    myFile.write('\\parindent=0em\n')
    myFile.write('\\leftskip 0.1in\n')
    myFile.write('\\parindent -0.1in\n\n')

    myFile.write(DOCUMENT)

    myFile.write('\\end{multicols}\n\\clearpage\n\\end{document}')

os.system(f"xelatex {outputFilename}")
os.system(f"xelatex {outputFilename}")
print(f"Made {outputFilename}")
