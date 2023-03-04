#include <stdio.h>
#define P(a) printf("%d\n",a)
int main()
{
	unsigned int x,y;
	scanf("%d%d",&x,&y);
	P(x|y);
	P(x^y);
	P(x&y);
	P(~x+~y);
	P(x<<3);
	P(y>>4);
	getchar();getchar();
	return 0;
}