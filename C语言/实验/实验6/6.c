#include <stdio.h>

typedef struct student
    {
        int id;
        char name[20];
        struct laptop
            {
                char model[20];
                char color[20];
                int price;
            } Laptop;
    } Student;

int display(Student *p);

int main()
{
    Student list[3];
    Student *p;
    for (p = list; p <= list + 2; ++p) {
        static int i = 1;
        printf("请输入第%d位学生的学号：\n", i);
        scanf("%d", &p->id);
        printf("请输入第%d位学生的姓名：\n", i);
        scanf("%s", p->name);
        printf("请输入第%d位学生的笔记本电脑型号：\n", i);
        scanf("%s", p->Laptop.model);
        printf("请输入第%d位学生的笔记本电脑颜色：\n", i);
        scanf("%s", p->Laptop.color);
        printf("请输入第%d位学生的笔记本电脑价格：\n", i);
        scanf("%d", &p->Laptop.price);
        i++;
    }
    p = list;
    display(p);
}

int display(Student *p)
{
    for (Student *p1 = p; p1 <= p + 2; ++p1) {
        printf("%d\t%s\t%s\t%s\t￥%d\n",
               p1->id, p1->name, p1->Laptop.model, p1->Laptop.color, p1->Laptop.price);
    }
}