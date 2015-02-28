import sys


def fibonacci(n):
    a, b = 0, 1
    for i in xrange(0, n):
        a, b = b, a + b
    return a


def main():
    n = int(sys.stdin.read())
    print fibonacci(n)

main()
