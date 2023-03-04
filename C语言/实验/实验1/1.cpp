#include <stdio.h>

int main()
{
	char a;
	a=getchar();
	int i=0;

	if(65<=a&&a<=90)
	{
		printf("%c",a);
		i++;
	}

	else if(97<=a&&a<=122)
	{
		printf("%c",a-32);
		i++;
	}

	else if(48<=a&&a<=57)
	{
		i++;
		int r=a-48;
		int b=0,k=0,i;

		int code[10];

		while (r!=0)
		{
			b=r%2;
			k++;
			code[k]=b;
			r=r/2;
		}

		for(i=k;i>=1;i--)
		{
			printf("%d",code[i]);
		}
		
	}

	if(i==0)
	{
		printf("%d",a);
	}


	getchar();getchar();
	return 0;
}