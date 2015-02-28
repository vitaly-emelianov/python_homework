import sys


def letter_counter(text):

    letter_counts = {}

    for letter in text:
        if letter.isalpha():
            letter = letter.lower()
            if letter not in letter_counts:
                letter_counts[letter] = 1
            else:
                letter_counts[letter] += 1

    if not letter_counts:
        print '\n',
    else:
        result = []
        letter_counts_alphabetical = sorted(letter_counts.items(), key=lambda x: x[0])
        for letter, count in sorted(letter_counts_alphabetical, key=lambda x: x[1], reverse=True):
            result.append(': '.join([letter, str(count)]))

        print '\n'.join(result)


def main():
    text = sys.stdin.read()
    letter_counter(text)

main()
