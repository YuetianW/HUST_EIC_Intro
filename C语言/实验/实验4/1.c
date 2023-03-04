#include <stdio.h>

int main()
{
    char a = 'A';
    int x = 125;
    float p = 10.25;

    char *pa=&a;
    int *px=&x;
    float *pp=&p;

    printf("a:%c\n",a);
    printf("address of a:%p\n",pa);
    printf("x:%d\n",x);
    printf("address of x:%p\n",px);
    printf("p:%f\n",p);
    printf("address of p:%p\n",pp);



}
