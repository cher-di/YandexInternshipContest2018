if __name__ == '__main__':
    n = int(input())
    p = []
    for i in range(n):
        a, b = tuple(int(el) for el in input().split())
        p.append(a * b)
    p_sum = sum(p)
    for p_el in p:
        print(round(p_el / p_sum, 12))
