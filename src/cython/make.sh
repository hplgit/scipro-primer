#!/bin/sh
sh clean.sh

# Build Cython code
python setup_cy.py build_ext --inplace
# Test if module works
python -c "import _dice6_cy"
if [ $? -eq 0 ]; then
  echo "Cython module successfully built"
else
  echo "Cython module NOT successfully built"
  exit 1
fi
# Compile and view C code
cython -a dice6.pyx
#firefox dice6.html

# Build stand-alone C program
gcc -o dice6.capp -O3 dice6_c.c

# Build f2py-generated interface to dice6 in C
f2py -m _dice6_c1 -h dice6_c.pyf dice6_c_signature.f --overwrite-signature
f2py -c dice6_c.pyf dice6_c.c
python -c 'import _dice6_c1 as r; print dir(r); print r.dice6.__doc__; print r.dice6(1000, 4, 2)'
if [ $? -eq 0 ]; then
  echo "f2py-generated interface to C successfully built"
else
  echo "f2py-generated interface to C NOT successfully built"
  exit 1
fi

# Build Cython-generated interface to foll_dice in C
python setup_c.py build_ext --inplace
# Test if module works
python -c 'import _dice6_c2 as r; print dir(r); print r.dice6_cwrap.__doc__; print r.dice6_cwrap(1000, 4, 2)'
if [ $? -eq 0 ]; then
  echo "Cython-generated interface to C successfully built"
else
  echo "Cython-generated interface to C NOT successfully built"
  exit 1
fi

echo
echo
files="_dice6_c1.so _dice6_c2.so _dice6_cy.so dice6.capp"
for file in $files; do
  if [ ! -f $file ]; then
    echo
    echo "$file was NOT successfully built"
  else
    echo "$file was successfully built"
  fi
done


exit 0
# Profile Python code
python -m cProfile -o .prof dice6.py 300000
#python -c 'import pstats; pstats.Stats(".prof").sort_stats("time").print_stats(30)'
# Or
python -c "
import pstats
s = pstats.Stats('.prof')
s.strip_dirs()
s.sort_stats('time')
s.print_stats(30)
"



