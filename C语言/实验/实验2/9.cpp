#include <stdio.h>
int main()
{
	int a;
	
	printf("请输入今天是星期几：");
	scanf("%d",&a);
	
	switch(a)
	{
		case 1:
		case 2:
		case 3:
		case 4:
		case 5:   
		           printf("工作日愉快\n");
		           break;
		           
		case 6:
		case 7:
			       printf("周末愉快\n");
			       break;
			       
		default:  
		           printf("请输入位于1到7之间的数");
		           break;
	}
}