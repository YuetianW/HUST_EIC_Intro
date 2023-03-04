#include <stdio.h>
#include <string.h>

int is_substring(char *str1, char *str2);

int main()
{
    char str1[50],str2[50];
    int flag;
    gets(str1);
    gets(str2);

    flag = is_substring(str1,str2);

    if(flag)
    {
        printf("yes");
    }
    else
    {
        printf("no");
    }
    return 0;
}

int is_substring(char *str1, char *str2)
{
    int flag=0;//设置一个变量来判断是否为子串
    char *p=str1,*q=str2;//指针初始化，赋以首地址
    for(p=str1;*p;p++)//将str1的首地址赋给p;第二个表达式判断字符是否为‘0’；
    {
        for(q=str2;*p==*q&&*q;p++,q++);//注意这里有分号！！这个for语句没有内嵌代码
 
        if(!*q)//如果str2遍历完，此时*q的值一定是默认值‘0’，那么！*q为真
        {
            flag=1;
            break;//得到想要的答案之后就跳出循环
        }
    }
    return flag;
}
