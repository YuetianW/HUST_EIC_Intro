#include <stdio.h>
int main()
{
	float a,b,s;
	char op;
	
	scanf("%f%c%f",&a,&op,&b);
	
	switch(op)
	{
		case '+':   printf("%f+%f=%f",a,b,a+b);
		            break;
		case '-':   printf("%f-%f=%f",a,b,a-b);
		            break;
		case '*':   printf("%f*%f=%f",a,b,a*b);
		            break;
	    case '/':   if(b==0)
	                {
	                	printf("除法错误");
	                	break;
					}else
		            {
					    printf("%f/%f=%f",a,b,a/b);
	                    break;
	                }
	                
	    default:    printf("无法进行这种运算\n");
	}
}