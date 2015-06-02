import unittest
import random
import argparse


class TestFunctions(unittest.TestCase):
    '''Test some functions'''
    def test_tokenize(self):
        answer = ['Hello'.decode('utf-8'), ','.decode('utf-8'), 'World'.decode('utf-8')]
        self.assertEqual(tokenize('Hello, World'.decode('utf-8')), answer)

    def test_tokens_counter(self):
        line = 'Hello, World'.decode('utf-8')
        answer = {(): {u'Hello': 1, u'World': 1, u',': 1}, (u'Hello',): {u',': 1},
                  (u',',): {u'World': 1}, (u'Hello', u','): {u'World': 1}}
        tokens = tokenize(line)
        self.assertEqual(following_tokens_counts(tokens, 2), answer)


def tokenize(text, ignore_spaces=True, ignore_punctuation=False):
    tokens = []
    token = []

    ignoring_symbols = {'\n', '\r', '\t'}
    if ignore_spaces:
        ignoring_symbols.add(' ')

    curr_token_is_number = text[0].isnumeric()
    for symbol in text:
        if symbol.isalpha():
            if curr_token_is_number and token:
                tokens.append(''.join(token))
                token = []
            token.append(symbol)
            curr_token_is_number = False
        elif symbol.isnumeric():
            if not curr_token_is_number and token:
                tokens.append(''.join(token))
                token = []
            token.append(symbol)
            curr_token_is_number = True
        else:
            if token:
                tokens.append(''.join(token))
            token = []
            if symbol not in ignoring_symbols and not ignore_punctuation:
                tokens.append(symbol)
    if token:
        tokens.append(''.join(token))
    return tokens


def print_tokens(args):
    '''Print all tokens of given text'''
    tokens = tokenize(args.text, ignore_spaces=False)
    print '\n'.join(tokens).encode('utf-8')


def following_tokens_counts(tokens, max_depth, counts={}):
    '''Count tokens frequencies after all sequencies no longer than max_depth'''

    tokens_number = len(tokens)

    if tuple() not in counts:
        counts[tuple()] = {}
    if tokens[0] not in counts[tuple()]:
        counts[tuple()][tokens[0]] = 1
    else:
        counts[tuple()][tokens[0]] += 1

    for i in xrange(tokens_number-1):
        token = tokens[i+1]
        sequence = tuple(tokens[:i+1])
        sequence_length = len(sequence)

        if max_depth > sequence_length:
            j = 0
        else:
            j = sequence_length - max_depth

        while j <= sequence_length:
            subsequence = sequence[j:]
            if subsequence not in counts:
                counts[subsequence] = {token: 1}
            else:
                if token not in counts[subsequence]:
                    counts[subsequence][token] = 1
                else:
                    counts[subsequence][token] += 1
            j += 1

    return counts


def print_probabilities(args):
    '''Print probabilities'''
    lines = args.text.split('\n')

    tokens_counts = {}
    for line in lines:
        if line:
            tokens = tokenize(line, ignore_spaces=True, ignore_punctuation=True)
            tokens_counts = following_tokens_counts(tokens, args.depth, tokens_counts)

    table = []
    for sequence, counts in sorted(tokens_counts.items()):
        if sequence:
            table.append(' '.join(sequence))
        else:
            table.append('')

        norm = sum([v for v in counts.values()])
        for token, count in sorted(counts.items()):
            if token.isalpha():
                line = ("  {0}: {1:.2f}".format(token.encode('utf-8'), float(count)/norm))
                line = line.decode('utf-8')
            table.append(line)

    print '\n'.join(table).encode('utf-8')


def get_randomly(counts):
    '''Generate token from list with weighted probability.'''

    totals = []
    words = []
    running_total = 0

    for word, count in counts.items():
        words.append(word)
        running_total += count
        totals.append(running_total)

    rnd = random.random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return words[i]


def generate_tokens(tokens, counts, generated_text_size, max_depth):
    '''Generate new tokens sequence from given tokens and counts'''

    generated_tokens = []
    potential_tokens = []

    new_token = get_randomly(counts[()])
    while not new_token.isalpha() and not new_token.isnumeric():
        new_token = get_randomly(counts[()])
    generated_tokens.append(new_token)

    depth = 0
    size = 1
    while size <= generated_text_size:
        if depth < max_depth:
            depth += 1
        sequence = tuple(generated_tokens[-depth:])
        # Case when chain breaks
        while sequence not in counts:
            # We are generating new token not depending on previous tokens
            new_token = get_randomly(counts[()])
            while not new_token.isalpha() and not new_token.isnumeric():
                new_token = get_randomly(counts[()])
            generated_tokens.append(new_token)
            potential_tokens = []
            sequence = tuple([new_token])
            depth = 1
        new_token = get_randomly(counts[sequence])
        generated_tokens.append(new_token)
        size += 1

    return generated_tokens


def generate_text(tokens):
    '''Generate valid text from given tokens'''
    tokens_number = len(tokens)
    text = []
    punctuation = {'.', '!', '?'}

    # makes first letter capital
    first_token = tokens[0][0].upper() + tokens[0][1:]
    text.append(first_token)

    punctuation_made = False
    for i in xrange(1, tokens_number):
        token = tokens[i]

        if token.isalpha() or token.isnumeric():
            text.append(' ')
            if punctuation_made:
                token = token[0].upper() + token[1:]
            punctuation_made = False
            text.append(token)
        else:
            if token in punctuation:
                punctuation_made = True
            text.append(token)

    if tokens[-1] not in punctuation:
        text.append('.')

    return ''.join(text).encode('utf-8')


def print_generated_text(args):
    '''Generate and print text'''
    tokens = tokenize(args.text)
    counts = following_tokens_counts(tokens, args.depth)
    generated_tokens = generate_tokens(tokens, counts, args.size, args.depth)
    print generate_text(generated_tokens)


def parse_file(filename):
    '''Parse file given filename'''
    with open(filename) as f:
        read_in = f.read()
    text = read_in.decode('utf-8')
    lines = text.split('\n')
    tokens = lines[0].split() + ['\n'.join(lines[1:])]

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_tokenize = subparsers.add_parser('tokenize')
    parser_tokenize.add_argument('text', type=unicode)
    parser_tokenize.set_defaults(func=print_tokens)

    parser_probabilities = subparsers.add_parser('probabilities')
    parser_probabilities.add_argument('--depth', type=int)
    parser_probabilities.add_argument('text', type=unicode)
    parser_probabilities.set_defaults(func=print_probabilities)

    parser_generate = subparsers.add_parser('generate')
    parser_generate.add_argument('--depth', type=int)
    parser_generate.add_argument('--size', type=int)
    parser_generate.add_argument('text', type=unicode)
    parser_generate.set_defaults(func=print_generated_text)

    parser_test = subparsers.add_parser('test')
    parser_test.add_argument('empty')
    parser_test.set_defaults(func=lambda x: unittest.main())

    args = parser.parse_args(tokens)
    args.func(args)


if __name__ == '__main__':
    parse_file("input.txt")
