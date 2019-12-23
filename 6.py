PROGRAMMER = 1
MANAGER = 2

if __name__ == '__main__':
    n = int(input())
    a = [int(i) for i in input().split()]
    b = [int(i) for i in input().split()]
    m = int(input())
    certificates = []
    for i in range(m):
        certificates.append(tuple(int(i) for i in input().split()))

    programmers, managers = set(), set()
    profit = sorted(tuple((i, PROGRAMMER, a[i]) for i in range(n)) +
                    tuple((i, MANAGER, b[i]) for i in range(n)), key=lambda x: x[2], reverse=True)
    for person, skill_type, value in profit:
        if person not in (programmers | managers):
            if skill_type == PROGRAMMER and len(programmers) < n // 2 or \
                    skill_type == MANAGER and len(managers) == n // 2:
                programmers.add(person)
            else:
                managers.add(person)

    total_sum = sum(a[person] for person in programmers) + sum(b[person] for person in managers)

    for num, certificate_type, d in certificates:
        person = num - 1

        if certificate_type == PROGRAMMER:
            a[person] += d
            if person in programmers:
                total_sum += d

            else:
                max_total_sum = 0
                selected_programmer = -1
                for programmer in programmers:
                    if total_sum - b[person] - a[programmer] + a[person] + b[programmer] > total_sum:
                        max_total_sum = total_sum - b[person] - a[programmer] + a[person] + b[programmer]
                        selected_programmer = programmer

                if selected_programmer != -1:
                    programmers.remove(selected_programmer)
                    managers.remove(person)
                    programmers.add(person)
                    managers.add(selected_programmer)
                    total_sum = max_total_sum

        elif certificate_type == MANAGER:
            b[person] += d
            if person in managers:
                total_sum += d

            else:
                max_total_sum = 0
                selected_manager = -1
                for manager in managers:
                    if total_sum - a[person] - b[manager] + b[person] + a[manager] > total_sum:
                        max_total_sum = total_sum - a[person] - b[manager] + b[person] + a[manager]
                        selected_manager = manager

                if selected_manager != -1:
                    programmers.remove(person)
                    managers.remove(selected_manager)
                    programmers.add(selected_manager)
                    managers.add(person)
                    total_sum = max_total_sum

        else:
            print("Bad certificate type")

        print(total_sum)
