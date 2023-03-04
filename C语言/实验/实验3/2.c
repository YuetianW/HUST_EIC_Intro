#include <stdio.h>

int fun3(int x)
{
    static int a = 3;
    a += x;
    return (a);
}

void main()
{
    int k = 2, m = 1, n;
    n = fun3(k);
    n = fun3(m);
    printf("%d \n", n);
}