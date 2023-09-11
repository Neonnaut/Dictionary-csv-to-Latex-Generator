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

\\usepackage{hanging} % Gets entries indenting well

% Hack for getting hanging to BEHAVE
\\makeatletter
\\def\\hangparas#1#2{%
  \\setlength{\\parindent}{\\z@}%
  \\everypar{%
    \\if@nobreak
      \\@nobreakfalse
      \\clubpenalty \\@M
    \\else
      \\clubpenalty \\@clubpenalty
    \\fi
    \\everypar{\hangpara{#1}{#2}}%
    \\hangpara{#1}{#2}%
  }%
}

\\usepackage{xcolor} % coloured text
\\usepackage{hyperref} % hypertext in contents

"""
# eeee
DARKTHEME = """
\\pagecolor[rgb]{0.137,0.152,0.18} %black
\\color[rgb]{0.84,0.88,0.94} %grey

\\definecolor{bold_color}{rgb}{0.831,0.823,0.823}

\\usepackage{sectsty}
\\chapterfont{\\color{white}}  % sets colour of chapters
\\sectionfont{\\color{white}}

\\hypersetup{
  colorlinks,citecolor=white,filecolor=white,linkcolor=white,urlcolor=white
}

"""

LIGHTTHEME = """
\\color[rgb]{0.18,0.18,0.18} %grey
\\definecolor{bold_color}{rgb}{0,0,0}
\\hypersetup{
  colorlinks,citecolor=black,filecolor=black,linkcolor=black,urlcolor=black
}

"""

COMMANDS = """
\\newcommand{\\entry}[5]{\\textbf{\\color{bold_color}{#1}}\\markboth{#1}{#1}\\ [{\\color{bold_color}#2}]\\ \\textit{{#3}}\\ {\\color{bold_color}{#4}}\\
\\ifthenelse{\\isempty{#5}}
  {#5}  % if no title option given
{- {#5} }}

\\newcommand{\\entrySmall}[3]{\\textbf{\\color{bold_color}{#1}}\\markboth{#1}{#1}\\ {\\color{white}{#2}}\\
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
\\author{\\myAuthor}
\\date{\\myDate}
\\begin{titlepage}
\\begin{center}
  \\vspace{10mm}
  \\vspace{40mm}
  \\vspace{10mm}
  \\fontsize{10mm}{7mm}\\selectfont \\textup{\\color{white}{\\myLanguage}}\\\\
\\end{center}
\\vspace{25mm}
\\centering{
\\textnormal{\\large{\\bf Author:\\\\}}
{\\large \\myAuthor\\\\ }
\\vspace{8mm}
\\textnormal{\\large{\\bf Last Modified:\\\\}}
{\\large \\myDate\\\\}
\\hfill
}
\\end{titlepage}
\\tableofcontents
\\thispagestyle{empty}

\\clearpage
%-----------------------------------------------------

"""

LEXICON_PREAMBLE = """\\invisiblesection{Lexicon}
\\pagestyle{fancy} % Use the custom headers and footers
\\parindent=0em
\\leftskip 0.1in
\\parindent -0.1in

"""