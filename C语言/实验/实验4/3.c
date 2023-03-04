#include <stdio.h>

int main()
{
    int a[10];
    int i;
    for(i=0;i<10;i++)
    {
        scanf("%d",&a[i]);
    }

    int *pa[10];
    for(i=0;i<10;i++)
    {
        pa[i]=&a[i];  //让指针数组分别指向数组中每一个元素
    }

    int *pmin,*pmax;

    int min=a[0];
    for(i=0;i<10;i++)
    {
        if(a[i]<=min)
        {
            min=a[i];
            pmin=&a[i];
        }
    }
    int temp;
    temp=a[0];
    a[0]=*pmin;
    *pmin=temp;  //交换min与第一个数

    int max=a[0];
    for(i=0;i<10;i++)
    {
        if(a[i]>=max)
        {
            max=a[i];
            pmax=&a[i];
        }
    }
    temp=a[9];
    a[9]=*pmax;
    *pmax=temp;

    for(i=0;i<10;i++)
    {
        printf("%d ",a[i]);
    }

}
