#include <stdio.h>

int main()
{
    int A[5]={2,6,3,7,9};
    int B[5];
    int a;
    scanf("%d",&a);

    int i,n=0,j=0;
    for(i=0;i<5;i++)
    {
        if(A[i]!=a)
        {
            B[j]=A[i];
            j++;
            n+=1;
        }

    }
    int C[n];
    for(i=0;i<n;i++)
    {
        C[i]=B[i];
    }

    for(i=0;i<n;i++)
    {
        printf("%d ",C[i]);
    }

}