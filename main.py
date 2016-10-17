# coding=utf8

import os
import re
import json
from argparse import ArgumentParser

PATH = '/home/mag/src/1C_exange_zabbix/testfiles/'
FILEPATERN = re.compile(r'^(\w+)_(\w+)_(\w+)_.+\.zip')


def creareargumentparser():
    parser = ArgumentParser(description='Crate JSON file for Zabbix LLD')
    parser.add_argument('--path', '-p', type=str, help='path to exchange files')
    parser.add_argument(
        '--out',
        '-o',
        type=bool,
        nargs='+',
        help='True for output to screen'
    )
    return parser

def max_modify_file_type(item):
    """
    key function for data modifes
    """
    return item[1]

def unique_pairs(seq):
    """
    Get list of tuple pairs and return unique pairs
    """
    unic = {}
    for a, b in seq:
        if unic.get(a) is None and b not in unic.keys():
            unic[a] = b
    return [ i for i in unic.items()]


def generate_json_for_zabbix(path):
    """
    Make JSON object for zabbix files
    :param path: folder with 1C exchange
    :return: JSON object:
                list of params:
                    '#DELTATIME': difference beetwin file's modify date
                    '#LEFTNAME': left file name
                    '#RIGHTNAME': right file name
                    '#LEFTSIZE': left file size
                    '#RIGHTSIZE': right file size
                    '#LEFTMODIFYDATE': left file modify date,
                    '#RIGHTMODIFYDATE': right file modify date
    """
    files = [
        [
            re.match(FILEPATERN, file).groups(),
            os.path.getmtime(os.path.join(PATH, file)),
            os.path.getsize(os.path.join(PATH, file)),
            os.path.join(PATH, file),
            file,
        ]
        for file in os.listdir(PATH)
        if os.path.isfile(os.path.join(PATH, file))
    ]
    # print(files)
    types = list(set([file[0] for file in files]))
    # print(types)
    pairs = list(
        set([(i, (i[1], i[0], i[2])) for i in types])
    )
    results = []
    for left, right in unique_pairs(pairs):
        # print(start, finish)
        file_pair = (
            max([f for f in files if f[0] == left], key=max_modify_file_type),
            max([f for f in files if f[0] == right], key=max_modify_file_type)
        )
        result = {
            '#DELTATIME': abs(file_pair[0][1] - file_pair[1][1]),
            '#LEFTNAME': file_pair[0][4],
            '#RIGHTNAME': file_pair[1][4],
            '#LEFTSIZE': file_pair[0][2],
            '#RIGHTSIZE': file_pair[1][2],
            '#LEFTMODIFYDATE': file_pair[0][1],
            '#RIGHTMODIFYDATE': file_pair[1][1]
        }
        results.append(result)
    json_for_zabbix = json.dumps({'data': results})
    return json_for_zabbix


if __name__ == '__main__':
    namespace = creareargumentparser()
    args = namespace.parse_args()
    if args.out:
         print(generate_json_for_zabbix(args.path))
    else
        generate_json_for_zabbix(path)
