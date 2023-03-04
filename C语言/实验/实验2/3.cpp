#include <stdio.h>
int main()
{
	
	int a,b;
	int i,j;
	scanf("%d %d",&a,&b);
	
	//最大公约数
	for(i=a<b?a:b;i>0;i--)
	{
		if(a%i==0&&b%i==0)
		{
			printf("%d 和 %d 的最大公约数为 %d\n",a,b,i);
			break;
		}
		
	}
	
	
	//最小公倍数
	for(j=a<b?b:a;;j++)
	{
		if(j%a==0&&j%b==0)
		{
			printf("%d 和 %d 的最小公倍数为 %d\n",a,b,j);
			break;
		}
	}
	
}


