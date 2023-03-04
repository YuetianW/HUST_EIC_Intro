#include <stdio.h>

int main()
{
    int i,j,k;
    scanf("%d",&i);
    scanf("%d",&j);
    scanf("%d",&k);

    int *pi=&i,*pj=&j,*pk=&k;
    int temp;
    temp=*pi;
    *pi=*pk;
    *pk=temp;
    temp=*pj;
    *pj=*pk;
    *pk=temp;
    printf("%d\t%d\t%d",i,j,k);

}
