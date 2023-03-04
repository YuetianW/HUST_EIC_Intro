#include <stdio.h>

int main()
{
    int A[3][3] = {1,2,3,4,5,6,7,8,9}, B[3][3] = {0};
    int (*pA)[3] = A, (*pB)[3] = B;

    int n = 3;
	int i=0,j=0,k=0;
    for (i = 0; i < n; i++)//从第i行开始
	{
		for (j = 0; j < n; j++)//从第j列开始
		{
			for (k = 0; k < n; k++)//i行元素和j列元素相乘，结果累加
			{
				*(* (pB + i)+j) += *(*(pA + i) + k) * *(*(pA +k) + j);
			}
		}
	}
	for(i=0; i<3; i++){
        for(j=0; j<3; j++) printf("%2d  ",B[i][j]);
        printf("\n");
    }
}
