import csv
import operator
import os
from datetime import datetime as dt

language = "Conlang Name"
author = "John Smith"
inputFilename = 'lexicon.csv'

# Extra letters - digraphs in the language that will form a category of words
extraLetters = ["p'", "t'", "k'", "ʎ", "ʔ", "ʙ", "ʦ", "ʣ"]

darkTheme = input("Use dark theme? (y/n) ")
hasHeader = input("Does the csv file have a header? (y/n) ")

outputFilename = language.replace(" ", "_")+'_dictionaryx.tex'
timeNow = dt.today().strftime('%A %d %B %Y')
f_old_char = ""
f_cur_char = ""
s_old_char = ""
s_cur_char = ""
index_letter = ""


PREAMBLE = """
\\documentclass[12pt,a4paper,twoside]{article}
\\usepackage[top=2.5cm,bottom=2.5cm,left=2.2cm,right=2.2cm,columnsep=22pt]{geometry}
\\usepackage{fontspec}\n\\setmainfont{Charis SIL}
\\newfontfamily\myfont[]{Broadway}
%\\usepackage{microtype} % Improves spacing
\\usepackage[bf]{titlesec} % Required for modifying section titles - bold, sans-serif, centered
\\usepackage{fancyhdr} % Required for modifying headers and footers
\\fancyhead[L]{\\rightmark} % Top left header
\\fancyhead[R]{\leftmark} % Top right header
\\renewcommand{\headrulewidth}{1.4pt} % Rule under the header
\\setlength{\headheight}{14.5pt}
\\fancyfoot[C]{\\textsf{\\thepage\\ }} % Bottom center footer
\\usepackage{multicol} % Required for splitting text into multiple columns
\\usepackage{ifthen} % provides \ifthenelse test
\\usepackage{xifthen} % provides \isempty test

"""

if darkTheme.casefold() == 'y':
    boldColor = 'white'
    PREAMBLE += """
\\usepackage{xcolor}
\\pagecolor[rgb]{0.18,0.18,0.23} %black
\\color[rgb]{0.84,0.88,0.94} %grey

\\usepackage{sectsty}

\\chapterfont{\\color{white}}  % sets colour of chapters
\\sectionfont{\\color{white}}

\\usepackage{hyperref}
\\hypersetup{
  colorlinks,citecolor=white,filecolor=white,linkcolor=white,urlcolor=white
}

"""
else:
    boldColor = 'black'
    PREAMBLE += """
\\usepackage{xcolor}

\\color[rgb]{0.18,0.18,0.18} %grey

\\usepackage{hyperref}
\\hypersetup{
  colorlinks,citecolor=black,filecolor=black,linkcolor=black,urlcolor=black
}

"""

PREAMBLE += """
\\newcommand{\\entry}[5]{\\textbf{\\color{""" + boldColor + """}{#1}}\\markboth{#1}{#1}\\ [{\\color{""" + boldColor + """}#2}]\\ \\textit{{#3}}\\ {\\color{""" + boldColor + """}{#4}}\\
\\ifthenelse{\\isempty{#5}}
  {#5}  % if no title option given
{- {#5} }}

\\newcommand{\\entrySmall}[3]{\\textbf{\\color{""" + boldColor + """}{#1}}\\markboth{#1}{#1}\\ {\\color{white}{#2}}\\
\\ifthenelse{\\isempty{#3}}
  {#3}  % if no title option given
{- {#3} }}

\\newcommand\\invisiblesection[1]{%
  \\refstepcounter{section}%
  \\addcontentsline{toc}{section}{\\protect\\numberline{\\thesection}#1}
  \sectionmark{#1}}

  %-----------------------------------------------------

"""

TITLE = """
\\begin{document}
\\author{""" + author + """}
\\date{""" + timeNow + """}
\\begin{titlepage}
\\begin{center}
  \\vspace{10mm}
  \\vspace{40mm}
  \\vspace{10mm}
  \\fontsize{10mm}{7mm}\\selectfont \\textup{\\color{white}{""" + language + """}}\\\\
\\end{center}
\\vspace{25mm}
\\centering{
\\textnormal{\\large{\\bf Author:\\\\}}
{\\large ' + author + '\\\\ }
\\vspace{8mm}
\\textnormal{\\large{\\bf Last Modified:\\\\}}
{\\large ' + timeNow + '\\\\}
\\hfill
}
\\end{titlepage}
\\tableofcontents
\\thispagestyle{empty}

\\clearpage
%-----------------------------------------------------

"""

DOCUMENT = """\\invisiblesection{Lexicon}
\\pagestyle{fancy} % Use the custom headers and footers
\\parindent=0em
\\leftskip 0.1in
\\parindent -0.1in"""
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
                                index_letter = "\\section*{"+s_cur_char.upper()
                                + "}%--------- SECTION " + s_cur_char.upper()
                                + "\n"+"\\begin{multicols}{2}"+"\n\n"
                                startOfList = False
                            else:
                                index_letter = "\\end{multicols}"+"\n"+"%\\newpage"+"\n"+"\\section*{"+s_cur_char.upper()
                                + "}%--------- SECTION " + s_cur_char.upper()
                                + "\n"+"\\begin{multicols}{2}"+"\n\n"
                            s_old_char = s_cur_char
                        elif f_old_char != f_cur_char:
                            if your_list[0] == row:
                                index_letter = "\\section*{"+f_cur_char.upper()
                                + "}%--------- SECTION " + f_cur_char.upper()
                                + "\n"+"\\begin{multicols}{2}"+"\n\n"
                            else:
                                index_letter = "\\end{multicols}"+"\n"+"%\\newpage"+"\n"+"\\section*{"+f_cur_char.upper()
                                + "}%--------- SECTION " + f_cur_char.upper()
                                + "\n"+"\\begin{multicols}{2}"+"\n\n"
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
        DOCUMENT += line
DOCUMENT += """\\end{multicols}
\\clearpage"""

with open(outputFilename, 'a', encoding="utf-8") as myFile:
    myFile.write(PREAMBLE)

    myFile.write(TITLE)

    myFile.write(DOCUMENT)

    myFile.write('\\end{document}')

os.system(f"xelatex {outputFilename}")
os.system(f"xelatex {outputFilename}")
print(f"Made {outputFilename}")
