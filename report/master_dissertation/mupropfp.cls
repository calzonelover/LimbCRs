% mupropfp.cls
%
% author: Michael A. Allen, Physics Department, Mahidol University
% email:  maa_software@yahoo.co.uk / frmaa"at"mahidol.ac.th
% webpage: einstein.sc.mahidol.ac.th/~scmal/LaTeX/

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{mupropfp}[2006/12/20 v0.2 Mahidol U. thesis proposal front page]
\LoadClass[11pt,a4paper]{letter}
\RequirePackage{ifthen}
\textwidth 147.5mm
\textheight 234.5mm
\oddsidemargin 12mm
\topmargin 0mm

\newcommand{\majoradvisor}[1]{\def\@majoradvisor{#1}}
\newcommand{\coadvisor}[1]{\def\@coadvisor{#1}}
\newcommand{\coadvisorII}[1]{\def\@coadvisorII{#1}}
\newcommand{\candidate}[1]{\def\@candidate{#1}}
\newcommand{\candidatenumber}[1]{\def\@candidatenumber{#1}}
\newcommand{\degree}[1]{\def\@degree{#1}
  \ifthenelse{\equal{\@degree}{PhD}}
	{\def\@degree{Ph.D.} \def\@fulldegree{Doctor of Philosophy}}
	{\def\@degree{M.Sc.} \def\@fulldegree{Master of Science}}
}
\newcommand{\subjectcode}[1]{\def\@subjectcode{#1}}
\coadvisorII{}
\newcommand{\maketitle}{
	\begin{center}
        \Large THESIS PROPOSAL\vskip 2em
	\Large\@title\vskip 4em
        Submitted to \vskip 2em
        \@majoradvisor\vskip 1em
        \@coadvisor
        \ifthenelse{\equal{\@coadvisorII}{}}{}{\vskip 1em\@coadvisorII}
    	\vfill
        By\vskip 1em
        \@candidate\vskip 2em
        \@candidatenumber\vskip 7em
	{\Large
    	This proposal is a part of the requirements for \\
	the degree of \@fulldegree\ (\@subjectcode) \\
	Faculty of Graduate Studies \\
	Mahidol University}
  	\end{center}
\thispagestyle{empty}
}
