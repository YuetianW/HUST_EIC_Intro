#include <stdio.h>
 
int main()
{
	int i,j;
	for(i=0;i<10;i++)
	{
		printf("\n");
		for(j=0;j<9-i;j++)
		{
			printf(" ");
		}
		for(j=0;j<2*i+1;j++)
		{
			printf("#");
		}
	}
	getchar();
	return 0;
}