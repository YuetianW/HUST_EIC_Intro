#include <stdio.h>

int main()
{
    int a[10];
    int i;
    for (i = 0; i < 10; i++) {
        scanf("%d", &a[i]);
    }

    int num = 0;
    int *pa = &a[0];
    for (i = 0; i < 10; i++) {
        if (a[i] > *pa) {
            pa = &a[i];
            num = i;
        }
    }

    printf("Max:%d\n下标：%d", *pa, num+1);
}
