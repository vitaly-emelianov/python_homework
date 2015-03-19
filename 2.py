import sys


def norm(p, x):

    norm = 0
    for item in x:
        norm += abs(item) ** p
    norm = norm ** (1.0 / p)

    return norm


def main():

    content = raw_input()
    p = float(content)

    content = raw_input()
    content = content.split()

    vector = []
    for item in content:
        vector.append(float(item))

    print norm(p, vector)

main()
