#include <stdio.h>

void bubble_sort(int array[10]);

int main()
{
    int array[10]={1,2,3,4,5,6,7,8,9,0};

    /*for (int i = 0; i < 10; i++) {
        scanf("%d", &array[i]);
    } //将十个数输入到一维数组*/
    int *p=array;

    bubble_sort(p);

    for (int i = 0; i < 10; i++) {
        printf(" %d ", array[i]);
    }
}

void bubble_sort(int array[10])
{

    for (int i = 1; i < 10; ++i) {
        for (int j = 0; j < 10 - i; ++j) {
            if (array[j]>array[j+1])
            {
                int temp = array[j];
                array[j] = array[j + 1];
                array[j + 1] = temp;
            }
            
        }
    }
}
