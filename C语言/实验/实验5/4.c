#include <stdio.h>

char *Copy(char *str, char *str_inv);

int main()
{
    char str[128] = {0};
    char str_inv[128] = {0};
    printf("请输入一串字符：");
    scanf("%s", str);
    Copy(str, str_inv);
    printf("%s", str_inv);
}

char *Copy(char *str, char *str_inv)
{
    int i = 0, j = 0;
    while (str[i] != '\0') {
        if (str[i] == 'a' || str[i] == 'e' || str[i] == 'i' || str[i] == 'o' || str[i] == 'u' ||
            str[i] == 'A' || str[i] == 'E' || str[i] == 'I' || str[i] == 'O' || str[i] == "U") {
            str_inv[j] = str[i];
            j++;
        }
        i++;
    }
}