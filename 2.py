import sys


def norm(p, x):

    norm = 0
    for item in x:
        norm += abs(item) ** p
    norm = norm ** (1.0 / p)

    return norm


def main():

    content = sys.stdin.read()
    temp = []

    for i in xrange(len(content)):
        if content[i] != '\n':
            temp.append(content[i])
        else:
            break

    p = float(''.join(temp))
    temp = content[i+1:].split()
    vector = []
    for item in temp:
        vector.append(float(item))

    print norm(p, vector)

main()
