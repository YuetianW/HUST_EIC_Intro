#include <stdio.h>

int main()
{
	int i,j;
	printf("%3c",'*');
	for(i=1;i<=9;i++)
	{
		printf("%3d",i);
	}
	printf("\n");
	for(i=1;i<=9;i++)
	{
		printf("%3d",i);
		for(j=1;j<=9;j++)
		{
			if(i<=j)
				printf("%3d",i*j);
			else
				printf("%3c",' ');
		}
		printf("\n");
	}
	getchar();
	return 0;
}