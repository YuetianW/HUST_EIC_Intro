#include <stdio.h>
#define N 4
int main()
{
	int i,j;
	int a[N],t;
	
	for(i=0;i<N;i++)
	{
		scanf("%d",&a[i]);
	}
	
	for(i=0;i<N-1;i++)
	{
		for(j=i+1;j<N;j++)
		{
			if(a[i]>a[j])
			{
				t=a[i];
				a[i]=a[j];
				a[j]=t;
			}
		}
	}
	
	for(i=0;i<N;i++)
	{
		printf("%d\t",a[i]);
	}
}