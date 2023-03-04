#include <stdio.h>

typedef struct student
    {
        int id;
        char *name;
        int score;
    } Student;

int update_score(Student *p, int id, int score);

int display(Student *p);

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
    int ID, newScore, res;
    Student *P = list;
    display(P);
    printf("请输入要更新的学生学号和更新后的成绩：\n");
    scanf("%d%d", &ID, &newScore);
    res = update_score(P, ID, newScore);
    printf("%d\n", res);
    printf("------------------\n最新表单：\n");
    display(P);
}

int update_score(Student *p, int id, int score)
{
    for (Student *p1 = p; p1 <= p + 5; ++p1) {
        if (p1->id == id) {
            p1->score = score;
            return 1;
        }
    }
    return -1;
}

int display(Student *p)
{
    for (Student *p1 = p; p1 <= p + 5; ++p1) {
        printf("%d\t%s\t%d\n", p1->id, p1->name, p1->score);
    }
}