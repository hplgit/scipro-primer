#!/bin/sh
# Make slides for primer book.
#
# bash make.sh funcif
#
# Source files for the slides are in doc/src/lectures.
# Need some files (newcommands.p.tex for instance) from doc/src/chapters.

set -x

function system {
  "$@"
  if [ $? -ne 0 ]; then
    echo "make.sh: unsuccessful command $@"
    echo "abort!"
    exit 1
  fi
}

if [ $# -eq 0 ]; then
echo 'bash make.sh looplist|oo|ode2'
exit 1
fi

name=$1
rm -f *.tar.gz

opt="--encoding=utf-8"


# Copy newcommands for the HTML files
preprocess -DFORMAT=html ../chapters/newcommands.p.tex > newcommands.tex

# reval.js HTML5 slides
html=${name}-reveal
system doconce format html $name --pygments_html_style=native --keep_pygments_html_bg --html_links_in_new_window --html_output=$html $opt
system doconce slides_html $html reveal --html_slide_theme=darkgray
doconce replace 'pre style="' 'pre style="font-size: 110%; ' $html.html
#exit

html=${name}-reveal-beige
system doconce format html $name --pygments_html_style=perldoc --keep_pygments_html_bg --html_links_in_new_window --html_output=$html $opt
system doconce slides_html $html reveal --html_slide_theme=beige

html=${name}-reveal-white
system doconce format html $name --pygments_html_style=default --keep_pygments_html_bg --html_links_in_new_window --html_output=$html $opt
system doconce slides_html $html reveal --html_slide_theme=simple

# deck.js HTML5 slides
html=${name}-deck
system doconce format html $name --pygments_html_style=perldoc --keep_pygments_html_bg --html_links_in_new_window --html_output=$html $opt
system doconce slides_html $html deck --html_slide_theme=sandstone.default

# Plain HTML slides
html=${name}-solarized
system doconce format html $name --pygments_html_style=perldoc --html_style=solarized3 --html_links_in_new_window --html_output=$html $opt
system doconce split_html $html --method=space8

# One big HTML file with space between the slides (good for browsing)
html=${name}-1
system doconce format html $name --html_style=bloodish --html_links_in_new_window --pygments_html_style=default --html_output=$html $opt
# Add space between splits
system doconce split_html $html.html --method=space8

# LaTeX Beamer slides

rm -f *.aux   # old .aux files can do harm
# Copy newcommands and ptex2tex style file
preprocess -DFORMAT=pdflatex ../chapters/newcommands.p.tex > newcommands.tex
cp ../chapters/.ptex2tex.cfg .

beamertheme=red_shadow

system doconce format pdflatex $name --latex_title_layout=beamer --latex_table_format=footnotesize --latex_admon_title_no_period $opt
system doconce ptex2tex $name envir=minted
#exit
system doconce slides_beamer $name --beamer_slide_theme=$beamertheme
system pdflatex -shell-escape ${name}
system pdflatex -shell-escape ${name}
cp $name.pdf ${name}-beamer.pdf
cp $name.tex ${name}-beamer.tex

# Handouts based on Beamer
system doconce format pdflatex $name --latex_title_layout=beamer --latex_table_format=footnotesize --latex_admon_title_no_period $opt
system doconce ptex2tex $name envir=minted
system doconce slides_beamer $name --beamer_slide_theme=red_shadow --handout
system pdflatex -shell-escape $name
pdflatex -shell-escape $name
pdflatex -shell-escape $name
pdfnup --nup 2x3 --frame true --delta "1cm 1cm" --scale 0.9 --outfile ${name}-beamer-handouts2x3.pdf ${name}.pdf
rm -f ${name}.pdf

# Ordinary plain LaTeX documents (kind of study guide)
rm -f *.aux  # important after beamer!
system doconce format pdflatex $name --minted_latex_style=trac --latex_admon=paragraph --latex_table_format=footnotesize $opt
system doconce ptex2tex $name envir=minted
doconce replace 'section{' 'section*{' $name.tex
pdflatex -shell-escape $name
mv -f $name.pdf ${name}-minted.pdf
cp $name.tex ${name}-plain-minted.tex

system doconce format pdflatex $name --latex_admon=paragraph --latex_table_format=footnotesize $opt
doconce replace 'section{' 'section*{' ${name}.p.tex
system doconce ptex2tex $name envir=ans:nt
pdflatex $name
mv -f $name.pdf ${name}-anslistings.pdf
cp $name.tex ${name}-plain-anslistings.tex

# IPython/Jupyter notebook
# (Make direct github links to all figures - work with a copy tmp.do.txt,
# cannot just use --figure_prefix because the URL is more complicated...)
cp $name.do.txt tmp.do.txt
doconce subst 'FIGURE: +\[fig-(.+?)/(.+?),' 'FIGURE: [https://raw.githubusercontent.com/hplgit/scipro-primer/master/slides/\g<1>/html/fig-\g<1>/\g<2>.png,' tmp.do.txt
system doconce format ipynb tmp $opt
mv -f tmp.ipynb $name.ipynb
mv -f ipynb-tmp-src.tar.gz ipynb-${name}-src.tar.gz


# Publish in separate github repo
# (scipro-primer must be a directory parallel to primer4)
dest=../../../../scipro-primer/slides
if [ ! -d $dest ]; then
# stop if scipro-primer is not present!
echo 'no copying to $dest because it does not exist!'
exit 0
fi

if [ ! -d $dest/$name ]; then
mkdir $dest/$name
mkdir $dest/$name/pdf
mkdir $dest/$name/html
mkdir $dest/$name/ipynb
fi
cp ${name}*.pdf $dest/$name/pdf
cp -r ${name}*.html ._${name}*.html reveal.js deck.js $dest/$name/html

# Figures: cannot just copy link, need to physically copy the files
if [ -d fig-${name} ]; then
if [ -L $dest/$name/html/fig-$name ]; then
rm -f $dest/$name/html/fig-$name
fi
if [ ! -d $dest/$name/html/fig-$name ]; then
mkdir $dest/$name/html/fig-$name
fi
cp -r fig-${name}/* $dest/$name/html/fig-$name
fi

cp ${name}.ipynb $dest/$name/ipynb
ipynb_tarfile=ipynb-${name}-src.tar.gz
if [ ! -f ${ipynb_tarfile} ]; then
cat > README.txt <<EOF
This IPython notebook ${name}.ipynb does not require any additional
programs.
EOF
tar czf ${ipynb_tarfile} README.txt
fi
cp ${ipynb_tarfile} $dest/$name/ipynb


doconce format html index --html_style=bootstrap --html_links_in_new_window --html_bootstrap_jumbotron=off
cp index.html $dest

cd $dest
git add .
