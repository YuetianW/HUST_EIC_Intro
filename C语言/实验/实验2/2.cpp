#include <stdio.h>
int main()
{
	int i=1,d=1;
	
	while(d<100-13){
		d = 13*i;
		i++;
		printf("%d ",d);
	}
	return 0;
}