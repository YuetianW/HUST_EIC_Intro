#include<stdio.h>

void main()
{
    int n, m;
    scanf("%d", &n);
    m = 2 * n - 1;
    int a[m][m];
    int i, j, k;

    for (i = 0; i < m; i++) {
        for (j = i; j < m - i; j++) {
            for (k = i; k < m - i; k++) {
                a[j][k] = i + 1;

            }
        }
    }
    for (i = 0; i < m; i++) {
        for (j = 0; j < m; j++) {
            printf("%d ", a[i][j]);
        }
        printf("\n");
    }

}