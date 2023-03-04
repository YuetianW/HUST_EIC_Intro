#include <stdio.h>

int main()
{
    int a[5]={1,2,9,6,5};
    int i,b;
    for (i=0;i<3;i++)
    {
        b=a[i];
        a[i]=a[4-i];
        a[4-i]=b;
    }
    for(i=0;i<5;i++)
    {
        printf("%d ",a[i]);
    }
}
