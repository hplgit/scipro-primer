#!/bin/sh
opt="--skip_inline_comments"

doconce spellcheck -d .dict4spell.txt *.do.txt
if [ $? -ne 0 ]; then
  echo "Misspellings!"  # use mydict.txt~.all~ as new dictionary.txt?
  exit 1
fi

name=main_bioinf

doconce format html $name PRIMER_BOOK=False EBOOK=False $opt

# ------
# The technique here was to make pygments files and link to them
# in _static-* (links mako function, but the new technique is to
# link to nicely typeset files at gihub.com

static=_static-bioinf
rm -rf $static
mkdir $static

# Generate nicely formatted code as pygments versions of Python files
cd src-bioinf
pyg="pygmentize -f html -O full,style=emacs"
for file in *.py; do
  $pyg -o ../$static/$file.html -l python $file
done
cp *.py ../$static
cd ..
# ------

doconce format sphinx $name PRIMER_BOOK=False EBOOK=False $opt
rm -rf sphinx-rootdir
doconce sphinx_dir author="H. P. Langtangen and G. K. Sandve" title="Illustrating Python via Examples from Bioinformatics" version=0.9 theme=cbc $name
python automake_sphinx.py
# Note: duplicate links warnings occur, but that is okay (we use the
# same repeated link text for local files)

doconce format pdflatex $name PRIMER_BOOK=False EBOOK=False $opt --device=paper
ptex2tex -DMINTED $name
pdflatex -shell-escape $name
makeindex $name
pdflatex -shell-escape $name
pdflatex -shell-escape $name

# Move
dest=../pub
rm -rf $dest/html
cp -r sphinx-rootdir/_build/html $dest
cp $name.pdf $dest/bioinf-py.pdf
cp $name.html $dest/bioinf-py.html
cp fig-bioinf/*.jpg $dest/fig-bioinf/



