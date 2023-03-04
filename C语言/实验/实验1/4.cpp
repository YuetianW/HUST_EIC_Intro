#include <stdio.h>

void main()
{
	int a=1,b=2,c=3;
	++a;
	b += ++c;
	{
		int b=4,c=5;c=b*c;
		a += b +=c;
		printf("a1=%d,b1=%d\n",a,b,c);
	}
	printf("a2=%d,b2=%d\n",a,b,c);
	getchar();
}