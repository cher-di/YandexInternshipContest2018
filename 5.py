if __name__ == '__main__':
    k, m, d = (int(i) for i in input().split())
    days_left = 0
    books_per_day = 1
    while m >= 0:
        m = m - books_per_day if d in (6, 7) else m + k - books_per_day
        if m >= 0:
            days_left += 1
        d = d % 7 + 1
        books_per_day += 1
    print(days_left)
