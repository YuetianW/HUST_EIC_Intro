#include <stdio.h>
#include <string.h>

void inverse_number(char *str, char *str_inv);

int main()
{
    char str[10], str_inv[10];
    scanf("%s", str);
    if (str[0] == '-') {
        printf("-");
        inverse_number(str + 1, str_inv);
    } else
        inverse_number(str, str_inv);
    return 0;
}

void inverse_number(char *str, char *str_inv)
{
    for (int i = strlen(str) - 1; i >= 0; --i) {
        printf("%c", str[i]);
    }
}
