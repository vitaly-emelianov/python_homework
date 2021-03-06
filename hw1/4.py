import sys


def read_input():

    content = sys.stdin

    max_length = 0
    lines = []

    got_max_length = False
    for line in content:
        if(not got_max_length):
            max_length = int(line)
            got_max_length = True
        else:
            lines.append(line)

    text = '\n'.join(lines)

    return (max_length, text)


def fit_width(max_length, text):

    lines = text.split('\n')
    editted_text = []

    for line in lines:
        if line == '':
            editted_text.append('')

        else:
            words = line.split(' ')

            new_line = []
            new_line_length = 0

            for word in words:
                word_length = len(word)

                if word_length >= max_length:
                    editted_text.append(' '.join(new_line))
                    editted_text.append(word)
                    new_line = []
                    new_line_length = 0

                elif new_line_length + word_length <= max_length:
                    new_line.append(word)
                    new_line_length += (word_length + 1)

                else:
                    editted_text.append(' '.join(new_line))
                    new_line = [word]
                    new_line_length = word_length + 1

            if new_line:
                editted_text.append(' '.join(new_line))

    return '\n'.join(editted_text)


def main():

    (max_length, text) = read_input()
    sys.stdout.write(fit_width(max_length, text))

main()
