#include <stdio.h>

typedef struct student
    {
        int id;
        char *name;
        int score;
    } Student;

int display(Student *p);

void sort_by_student_id(Student s[6]);

int main()
{
    Student list[6] = {
            {4, "York",   100},
            {7, "Jack",   90},
            {8, "Taylor", 80},
            {3, "Daisy",  70},
            {9, "John",   60},
            {2, "Judy",   50}
    };
    Student *p = list;
    printf("原始表单：\n");
    display(p);
    sort_by_student_id(p);
    printf("\n排序后：\n");
    display(p);
}

int display(Student *p)
{
    for (Student *p1 = p; p1 <= p + 5; ++p1) {
        printf("%d\t%s\t%d\n", p1->id, p1->name, p1->score);
    }
}

void sort_by_student_id(Student s[6])
{
    for (Student *p1 = s; p1 <= s + 5; ++p1) {
        for (Student *p2 = p1 + 1; p2 <= s + 5; ++p2) {
            if (p1->id > p2->id) {
                Student temp;
                temp = *p1;
                *p1 = *p2;
                *p2 = temp;
            }
        }
    }
}