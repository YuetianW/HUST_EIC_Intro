#include <stdio.h>
int main()
{
	int b=1;
	int i;
	int sum=0;
	
	for(i=1;i<=10;i++)
	{   
		b *= i;
		sum += b;
	}
	
	printf("sum=%d",sum);
}