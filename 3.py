import sys


def comparer(first_item, second_item):
    if first_item[1] == second_item[1]:
        return cmp(first_item[0], second_item[0])
    else:
        return -cmp(first_item[1], second_item[1])


def print_table(letter_counts):
    if not letter_counts:
        print '\n',
    else:
        result = []
        for letter, count in sorted(letter_counts.items(), cmp=comparer):
            result.append(': '.join([letter, str(count)]))

        print '\n'.join(result)


def letter_counter(text):

    letter_counts = {}

    for letter in text:
        if letter.isalpha():
            letter = letter.lower()
            if letter not in letter_counts:
                letter_counts[letter] = 1
            else:
                letter_counts[letter] += 1

    print_table(letter_counts)


def main():
    text = sys.stdin.read()
    letter_counter(text)

main()
