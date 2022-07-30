#!/usr/bin/env python
# coding=utf-8

def read_lines(file):
    with open(file) as f:
        sentences = set()
        begin = False
        sentence = []

        count = 0
        for line in f:
            if line == '\n':
                if not begin:
                    sentences.add(' '.join(sentence))
                    begin = True
                    count += 1
                    sent = ' '.join(sentence).replace('\n','')
                    sentence = []
                continue

            begin = False
            sentence.append(line)

        print(f'before:{count},after:{len(sentences)}')

        if len(sentences) == count:
            return None 

        return list(sentences)


def write_sentences_2_file(file, sentences):
    if sentences == None or len(sentences) == 0:
        print(f'no sentences')
        return

    with open(file, 'w') as writer:
        count = 0
        for line in sentences:
            wlines = line.split(' ')

            for wline in wlines:
                writer.write(wline) # \n not trimed

            writer.write('\n')
            count += 1

        print(f'write to file lines:{count}')


def get_filename(file):
    return file.rsplit('/', 1)[1].rsplit('.', 1)[0]


if __name__ == '__main__':
    input_file = '../app_data2/train_aug_3.txt'
    file_name = get_filename(input_file)

    output_file = file_name + '_dedup.txt'
    print(f'output_file:{output_file}')

    lines = read_lines(input_file)
    write_sentences_2_file(output_file, lines)

