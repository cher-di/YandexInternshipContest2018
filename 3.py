from string import ascii_lowercase


class Node:
    def __init__(self, value: str):
        self._value = value
        self._occurred = False
        self._children = []

    def add_child(self, value: str):
        self._children.append(Node(value))

    def make_occurred(self):
        self._occurred = True

    def is_occurred(self):
        return self._occurred

    def get_child(self, value: str):
        for child in self._children:
            if value == child._value:
                return child
        return None

    def is_leaf(self):
        return False if self._children else True

    def have_more_than_one_child(self):
        return len(self._children) > 1

    @property
    def value(self):
        return self._value


if __name__ == '__main__':
    n = int(input())
    words = input().split()

    roots = {letter: Node(letter) for letter in ascii_lowercase}
    pressings_total = 0

    for word in words:
        node = roots[word[0]]
        junction_or_occurred = 0
        for num_from_zero, letter in enumerate(word[1:]):
            num = num_from_zero + 1
            child = node.get_child(letter)
            if child is None:
                for left_letter in word[num:]:
                    node.add_child(left_letter)
                    node = node.get_child(left_letter)
                junction_or_occurred = len(word) - 1
                break
            else:
                if node.have_more_than_one_child():
                    junction_or_occurred = num
                node = child
                if num == len(word) - 1:
                    if node.is_leaf():
                        break
                    else:
                        if not node.is_occurred():
                            node.make_occurred()
                        junction_or_occurred = len(word) - 1

        pressings_total += junction_or_occurred + 1
    print(pressings_total)
