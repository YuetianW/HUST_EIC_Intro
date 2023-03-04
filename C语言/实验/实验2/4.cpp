#include <stdio.h>
int main()
{
	double i=1.00,j=1.00;
	double sum=0.00,b;
	
	for(int a=0;a<15;a++)
	{
		b=i;
		i=i+j;
		j=b;
		sum=sum+(i/j);
		
	}
	printf("sum=%f",sum);
}