#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def deal_jsonl_file(file, output_file):
    last_in_line = True
    jsl_list = []
    with open(file, 'r') as reader:
        sentence = []
        for line in reader:
            # print(repr(line))

            review = json.loads(line)
            jsl = to_masked_jsonl(review)
            if len(jsl) == 0:
                continue
            jsl_list.append(jsl)
            sentence = []

    with open(output_file, 'w') as writer:
        for jsl in jsl_list:
            writer.write(jsl+'\n')


def _sort_by(ner_item):
    return ner_item['start_index']


def to_masked_jsonl(review, to_word='我是app功能短语'):
    text = review['text']
    text_masked = '' 
    last_end = 0

    if review.get('ner_list', '') == '' or len(review['ner_list']) == 0:
        return ""

    ner_list = review['ner_list']
    ner_list.sort(key = _sort_by)

    for i in range(len(ner_list)):
        start_index = ner_list[i]['start_index'] 
        argument = ner_list[i]['argument'] 

        text_masked += text[last_end:start_index]
        text_masked += to_word
        last_end = start_index + len(argument)

    text_masked += text[last_end:] 

    review['text_masked'] = text_masked
    return json.dumps(review, ensure_ascii=False)


if __name__ == '__main__':
    deal_jsonl_file(
        './train.jsonl',
        './train_masked.jsonl'
    )
