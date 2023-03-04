#include <stdio.h>

int a = 2;

int f(int n)
{
    static int a = 3;
    int t = 0;
    if (n % 2) {
        static int a = 4;
        t += a++;
    } else {
        static int a = 5;
        t += a++;
    }
    return t + a++;
}

void main()
{
    int s = a, i;
    for (i = 0; i < 3; i++)
    {
        s += f(i);
        printf("%d\t",s);
    }
    printf("%d\n", s);
}