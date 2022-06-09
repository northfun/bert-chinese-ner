#!/usr/bin/env python
# coding=utf-8
'''
Author: Northfun
Date: 2022-05-28 14:38:57
LastEditors: Northfun
LastEditTime: 2022-06-05 00:10:26
FilePath: 1_data_prepare.py
'''
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import json
from utils import read_by_lines, write_by_lines, len_ch


# type
# AF: App Feature
def data_process(path, model="trigger", is_predict=False):
    """data_process"""

    def label_data(data, start, l, _type):
        """label_data"""
        for i in range(start, start + l):
            suffix = "B-" if i == start else "I-"
            data[i] = "{}{}".format(suffix, _type)
        return data

    sentences = []
    output = ["text_a"] if is_predict else ["text_a\tlabel"]
    with open(path) as f:
        for line in f:
            d_json = json.loads(line.strip())
            print(f'{d_json}')
            _id = d_json["id"]
            text_a = [
                "，" if t == " " or t == "\n" or t == "\t" else t
                for t in list(d_json["text"].lower())
            ]
            if is_predict:
                sentences.append({"text": d_json["text"], "id": _id})
                output.append('\002'.join(text_a))
            else:
                if model == "trigger":
                    labels = ["O"] * len(text_a)
                    for event in d_json.get("event_list", []):
                        event_type = event["event_type"]
                        start = event["trigger_start_index"]
                        trigger = event["trigger"]
                        labels = label_data(labels, start,
                                            len_ch(trigger), event_type)
                    output.append("{}\t{}".format('\002'.join(text_a),
                                                  '\002'.join(labels)))
                elif model == "role":
                    for event in d_json.get("event_list", []):
                        labels = ["O"] * len(text_a)
                        for arg in event["arguments"]:
                            role_type = arg["role"]
                            argument = arg["argument"]
                            start = arg["argument_start_index"]
                            labels = label_data(labels, start,
                                                len_ch(argument), role_type)
                            output.append("{}\t{}".format('\002'.join(text_a),
                                                          '\002'.join(labels)))
                elif model == "ner":
                    labels = ["O"] * len(text_a)
                    for ner in d_json.get("ner_list", []):
                        ner_type = ner["ner_type"]
                        start = ner["start_index"]
                        argument = ner["argument"]
                        labels = label_data(labels, start,
                                            len_ch(argument), ner_type)
                    output.append("{}\t{}".format('\002'.join(text_a),
                                                  '\002'.join(labels)))

    return output


if __name__ == "__main__":
    # data process
    data_dir = "../app_data/"
    data_file = "dev.jsonl"
    train_tri = data_process(f"{data_dir}{data_file}", "ner")
    write_by_lines("../app_data/dev.tsv", train_tri)
    print("=================end data preprocess==============")
