#include <stdio.h>
#include <stdlib.h>

double dice6(int N, int ndice, int nsix)
{
  int M = 0;
  int six, r, i, j;
  double p;

  for (i = 0; i < N; i++) {
    six = 0;
    for (j = 0; j < ndice; j++) {
      r = 1 + rand()/(RAND_MAX*6.0); /* roll die no. j */
      if (r == 6)
	six += 1;
    }
    if (six >= nsix)
      M += 1;
  }
  p = ((double) M)/N;
  return p;
}

int main(int nargs, const char* argv[])
{
  int N = atoi(argv[1]);
  int ndice = 6;
  int nsix = 3;
  double p = dice6(N, ndice, nsix);
  printf("C code: N=%d, p=%.6f\n", N, p);
  return 0;
}




