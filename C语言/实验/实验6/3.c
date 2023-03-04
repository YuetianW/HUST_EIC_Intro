#include <stdio.h>
#include <math.h>

typedef struct point
    {
        int x, y;
    } Point;

float distance(Point p1, Point p2);

float manhattan_distance(Point p1, Point p2);

int main()
{
    Point p1, p2;
    printf("请输入第一个点的坐标：(输入格式：x,y)\n");
    scanf("%d,%d", &p1.x, &p1.y);
    printf("请输入第二个点的坐标：\n");
    scanf("%d,%d", &p2.x, &p2.y);

    float dis;
    int m_dis;
    dis = distance(p1, p2);
    m_dis = manhattan_distance(p1, p2);

    printf("------------------\n");
    printf("两点间直线距离： %f\n", dis);
    printf("两点间曼哈顿距离： %d\n", m_dis);

}

float distance(Point p1, Point p2)
{
    float x_cha = p1.x - p2.x, y_cha = p1.y - p2.y;
    float dis = x_cha * x_cha + y_cha * y_cha;
    dis = sqrt(dis);
    return dis;
}

float manhattan_distance(Point p1, Point p2)
{
    float x_cha = p1.x - p2.x, y_cha = p1.y - p2.y;
    float m_dis = sqrt(x_cha * x_cha) + sqrt(y_cha * y_cha);
    return m_dis;
}