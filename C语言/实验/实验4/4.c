#include <stdio.h>

int main()
{
    char a[100] = "\0";
    char *pa=a;
    scanf("%s",pa);

    int i, j, p = 0;
    for (i = 0; i < 100; i++) {
        if (a[i] != '\0') {
            p++;
        }
    }

    int k = 0;
    for (i = 0, j = p - 1; i <= j; i++, j--) {
        if (a[i] != a[j]) {
            k = 1;
        } else
            continue;
    }

    if (k == 0)
        printf("yes");
    else
        printf("no");

}
