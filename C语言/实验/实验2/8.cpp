#include <stdio.h>
int main()
{
	float x,y;
	printf("x=");
	scanf("%f",&x);
	if(x<1)
	{
		y=x;
	}else if(x<10)
	{
		y=x+5;
	}else 
	{
		y=x-5;
	}
	
	printf("y=%f",y);
	
	
	    
	
}