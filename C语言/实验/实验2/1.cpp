#include <stdio.h>
int main()
{
	int i;
	int sum=0;
	
	for(i=0;i<100;i++)
	{
		if(i%2!=0)
		{
			sum=sum+i;
		}
	}
	printf("100之内自然数奇数之和为%d\n",sum);
}