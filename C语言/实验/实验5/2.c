#include <stdio.h>

void call_count();

int main()
{
    int i;
    scanf("%d", &i);
    while (i > 0) {
        call_count();
        i--;
    }

}

void call_count()
{
    static int i = 0;
    i++;
    if (i >= 10) {
        printf("调用次数已清零\n");
        return;
    }
    printf("这是第%d次调用本函数\n", i);
}