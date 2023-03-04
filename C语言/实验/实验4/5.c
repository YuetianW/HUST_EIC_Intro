#include <stdio.h>

int lenstr(char *str);

int main()
{
    char a[100] = "\0";
    gets(a);
    char *pa = a;
    printf("%d", lenstr(pa));

}

int lenstr(char *str)
{
    int t = 0;
    for (int i = 0;; i++) {
        if (*str != '\0') {
            t++;
            str++;
        } else {
            return t;
        }
    }
}