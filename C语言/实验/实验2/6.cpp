#include <stdio.h>
int main()
{
	int a,b=1;
	int i=0;
	
	for(a=1;;a++)
	{
		b=a*a;
		if(b>=1000)
			break;
		printf("%d\t",b);
		i++;
		
		if(i==8)
		{
			printf("\n");
			i=0;
		}
	    
	}
	
}