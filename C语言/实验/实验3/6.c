#include <stdio.h>

int main()
{
    int a = 0, b = 0, c = 0, d = 0, e = 0;
    int i;
    do {
        scanf("%d", &i);
        switch (i) {
            case 1:
                a++;
                break;
            case 2:
                b++;
                break;
            case 3:
                c++;
                break;
            case 4:
                d++;
                break;
            case 5:
                e++;
                break;
        }

    } while (i != -1);

    printf("%d %d %d %d %d",a,b,c,d,e);

}
