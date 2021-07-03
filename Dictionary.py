import csv
import operator
import subprocess
import os

f_old_char = ""
f_cur_char = ""
s_old_char = ""
s_cur_char = ""
index_letter = ""

inputFilename = 'RQR-shouldgood.csv'
outputFilename = 'RQR-Output.tex'
extraLetters = ["p'", "t'", "k'", "ng"]
author = "Name"
documentCreation = "Nov 2021"
documentUpdate = "Dec 2021"
conlang = "Oppie"

startOfList = True
with open(inputFilename, 'r') as f:
    reader = csv.reader(f)
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
with open(outputFilename, 'a') as myFile:
    myFile.write('\\documentclass[12pt,a4paper,twoside]{article}\n')
    myFile.write(
        '\\usepackage[top=2.5cm,bottom=2.5cm,left=2.2cm,right=2.2cm,columnsep=22pt]{geometry}\n')
    myFile.write(
        '\\usepackage{fontspec}\n\\setmainfont{Charis SIL}\n\\newfontfamily\myfont[]{Broadway}\n')
    myFile.write('\\usepackage{microtype} % Improves spacing\n')
    myFile.write(
        '\\usepackage[bf,sf]{titlesec} % Required for modifying section titles - bold, sans-serif, centered\n')
    myFile.write(
        '\\usepackage{fancyhdr} % Required for modifying headers and footers\n')
    myFile.write('\\fancyhead[L]{\\textsf{\\rightmark}} % Top left header\n')
    myFile.write('\\fancyhead[R]{\\textsf{\leftmark}} % Top right header\n')
    myFile.write(
        '\\renewcommand{\headrulewidth}{1.4pt} % Rule under the header\n')
    myFile.write(
        '\\fancyfoot[C]{\\textsf{\\thepage\\ }} % Bottom center footer\n\n')
    myFile.write(
        '\\usepackage{multicol} % Required for splitting text into multiple columns\n')
    myFile.write('\\usepackage{ifthen} % provides \ifthenelse test\n')
    myFile.write('\\usepackage{xifthen} % provides \isempty test\n\n')

    myFile.write(
        '\\newcommand{\entry}[4]{\\textbf{#1}\\markboth{#1}{#1}\\ \\textit{{#2}}\\ {#3}\\\n')
    myFile.write('\\ifthenelse{\\isempty{#4}}\n')
    myFile.write('{#4}               % if no title option given\n')
    myFile.write('{{#4} }}\n\n')

    myFile.write('\\begin{document}\n')
    myFile.write('\\title{' + conlang + '}\n')
    myFile.write('\\author{' + author + '}\n')
    myFile.write('\\date{' + documentUpdate + '}\n')
    myFile.write('\\begin{titlepage}\n')
    myFile.write('\\begin{center}\n')
    myFile.write('\\vspace{10mm}\n')
    myFile.write('A description of the constructed language... \\\\\n')
    myFile.write('\\vspace{40mm}\n')
    myFile.write('\\textnormal{ \\LARGE{\\myfont {' + conlang + '}\\\\}}\n')
    myFile.write('\\vspace{10mm}\n')
    myFile.write(
        '\\fontsize{10mm}{7mm}\\selectfont \\textup{' + conlang + '}\\\\\n')
    myFile.write('\\end{center}\n')

    myFile.write('\\vspace{25mm}\n')
    myFile.write('\\centering{\n')
    myFile.write('\\textnormal{\\large{\\bf Author:\\\\}}\n')
    myFile.write('{\\large ' + author + '\\\\ }\n')
    myFile.write('\\vspace{8mm}\n')
    myFile.write('\\textnormal{\\large{\\bf Date:\\\\}}\n')
    myFile.write(
        '{\\large Started: ' + documentCreation + ' \\\\ Last modified: ' + documentUpdate + '\\\\ }\n')
    myFile.write('\\hfill\n')
    myFile.write('}\n')
    myFile.write('\\end{titlepage}\n')

    myFile.write('\\tableofcontents\n\n')
    myFile.write('\\clearpage\n')
    myFile.write('\\thispagestyle{empty}\n')

    myFile.write('\\section{Lexicon}\n')
    myFile.write('This is the dictionary section.\n')
    myFile.write('\\clearpage\n')
    myFile.write(
        '\\pagestyle{fancy} % Use the custom headers and footers throughout the document\n')
    myFile.write('\\parindent=0em\n')
    myFile.write('\\leftskip 0.1in\n')
    myFile.write('\\parindent -0.1in\n\n')

    myFile.write(document)

    myFile.write('\\end{multicols}\n\\clearpage\n\\end{document}')

    print('Excellent')
