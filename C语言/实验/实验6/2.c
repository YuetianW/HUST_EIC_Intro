#include <stdio.h>

struct Fraction
    {
        int up, down;
    };

struct Fraction add(struct Fraction a, struct Fraction b);

struct Fraction mul(struct Fraction a, struct Fraction b);

struct Fraction simp(struct Fraction s);


int main()
{
    struct Fraction A, B;
    printf("请输入第一个分数：(输入格式：分子/分母)\n");
    scanf("%d/%d", &A.up, &A.down);
    printf("请输入第二个分数：\n");
    scanf("%d/%d", &B.up, &B.down);

    struct Fraction sum = add(A, B);
    struct Fraction pro = mul(A, B);
    sum = simp(sum);
    pro = simp(pro);

    printf("---------------\n");
    if (sum.down == 1)
        printf("和为：%d\n", sum.up);
    else
        printf("和为：%d/%d\n", sum.up, sum.down);
    if (pro.down == 1)
        printf("积为：%d\n", pro.up);
    else
        printf("积为：%d/%d\n", pro.up, pro.down);


}


struct Fraction add(struct Fraction a, struct Fraction b)
{
    struct Fraction res;
    res.up = a.up * b.down + b.up * a.down;
    res.down = a.down * b.down;
    return res;
}

struct Fraction mul(struct Fraction f1, struct Fraction f2)
{
    struct Fraction res;
    res.up = f1.up * f2.up;
    res.down = f1.down * f2.down;
    return res; //注意约分
}

struct Fraction simp(struct Fraction s)
{
    int min = (s.up < s.down ? s.up : s.down);
    int maxDiv;
    for (int i = min; i > 1; --i) {
        if (s.up % i == 0 && s.down % i == 0) {
            s.up /= i;
            s.down /= i;
            return s;
        }
    }
    return s;
}