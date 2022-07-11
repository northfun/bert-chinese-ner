#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def deal_bio_file(file, output_file):
    last_in_line = True
    jsl_list = []
    with open(file, 'r') as reader:
        sentence = []
        for line in reader:
            # print(repr(line))

            if line == '\n':
                if last_in_line:
                    last_in_line = False
                    # print(f'===={sentence}')
                    jsl = bio_2_jsonl(sentence)
                    jsl_list.append(jsl)
                    sentence = []
                continue
            
            last_in_line = True
            line = line.rstrip('\n')
            sentence.append(line)

    with open(output_file, 'w') as writer:
        for jsl in jsl_list:
            writer.write(jsl+'\n')


def bio_2_jsonl(bio_line):
    text = []
    ner_list = []
    last_is_word = False
    ner = []
    tag_type = ''

    for i in range(len(bio_line)):
        word, tag = bio_line[i].split('\t')

        text.append(word)
        if tag.find('-') > 0:
            _, tag_type = tag.split('-')

        if tag != 'O':
            if last_is_word and tag == 'B':
                ner_list.append({
                      'ner_type': tag_type,
                      'argument': ''.join(ner),
                      'start_index': i - len(ner)
                  })
                ner = []

            last_is_word = True
            ner.append(word) 
        else:
            if last_is_word:
                ner_list.append({
                    'ner_type': tag_type,
                    'argument': ''.join(ner),
                    'start_index': i - len(ner)
                })
                last_is_word = False
                ner = []
    return json.dumps({
        'text': ''.join(text),
        'ner_list': ner_list,
    }, ensure_ascii=False)


if __name__ == '__main__':
    deal_bio_file(
        '/Users/fanbeishuang/fbs/workspace/py/github/northfun/app_ner/bert-chinese-ner/app_data2/train.txt',
        './train.jsonl'
    )
