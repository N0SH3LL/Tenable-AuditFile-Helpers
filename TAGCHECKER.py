import sys
import re
from collections import defaultdict

def check_tags(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return
#
    layers = []
    problems = []
    tag_counts = defaultdict(lambda: {'open': 0, 'close': 0})
    custom_item_open = None

    tag_pattern = re.compile(r'<(/?)(if|condition|then|else|custom_item)[^>]*>')

    for line_number, line in enumerate(lines, start=1):
        tags = tag_pattern.findall(line)

        for tag in tags:
            closing, tag_type = tag

            if tag_type == 'custom_item': #
                if closing == '':
                    if custom_item_open is not None:
                        problems.append(f"Nested <custom_item> tag on line {line_number}. Previous <custom_item> opened on line {custom_item_open}.")
                    custom_item_open = line_number
                    tag_counts['custom_item']['open'] += 1
                else:
                    if custom_item_open is None:
                        problems.append(f"Unmatched closing </custom_item> tag on line {line_number}.")
                    else:
                        custom_item_open = None
                    tag_counts['custom_item']['close'] += 1
                continue

            if custom_item_open is not None:
                problems.append(f"Unexpected tag <{tag_type}> on line {line_number} within <custom_item> block opened on line {custom_item_open}.")

            if closing == '':
                tag_counts[tag_type]['open'] += 1
                if tag_type == 'if':
                    layers.append({'if': (line_number, False), 'condition': None, 'then': None, 'else': None})
                elif tag_type in ('condition', 'then', 'else'):
                    if not layers or (layers[-1][tag_type] is not None and not layers[-1][tag_type][1]):
                        problems.append(f"Missing opening <if> tag for <{tag_type}> on line {line_number}.")
                        layers.append({'if': ('Missing', True), 'condition': None, 'then': None, 'else': None})
                    current_layer = layers[-1]
                    if current_layer[tag_type] is None:
                        current_layer[tag_type] = (line_number, False)
                    else:
                        problems.append(f"Tag <{tag_type}> on line {line_number} already opened on line {current_layer[tag_type][0]}.")
            else:
                tag_counts[tag_type]['close'] += 1
                if not layers:
                    problems.append(f"Unmatched closing </{tag_type}> tag on line {line_number}.")
                    continue
                current_layer = layers[-1]
                if current_layer[tag_type] is None:
                    problems.append(f"Unmatched closing </{tag_type}> tag on line {line_number} with no opening tag.")
                else:
                    if current_layer[tag_type][1]:
                        problems.append(f"Tag </{tag_type}> on line {line_number} already closed corresponding tag.")
                    else:
                        current_layer[tag_type] = (current_layer[tag_type][0], True)

                if tag_type == 'if':
                    layer = layers.pop() #
                    if not layer['then']:
                        problems.append(f"Missing <then> tag in <if> block starting on line {layer['if'][0]}.")
                    for key in ['condition', 'then', 'else']:
                        if layer[key] and not layer[key][1]:
                            problems.append(f"Missing closing </{key}> tag for opening <{key}> tag on line {layer[key][0]}.")

    if custom_item_open is not None:
        problems.append(f"Unclosed <custom_item> tag opened on line {custom_item_open}.")

    while layers:
        last_layer = layers.pop()
        if last_layer['if'][0] != 'Missing':
            problems.append(f"Missing closing </if> tag for opening <if> tag on line {last_layer['if'][0]}.")
        for key in ['condition', 'then', 'else']:
            if last_layer[key] and not last_layer[key][1]:
                problems.append(f"Missing closing </{key}> tag for opening <{key}> tag on line {last_layer[key][0]}.")

    for tag_type, counts in tag_counts.items():
        if counts['open'] != counts['close']:
            problems.append(f"Mismatched {tag_type} tags: {counts['open']} opening vs {counts['close']} closing.")

    if problems:
        print("Problems found:")
        for problem in problems: #
            print(problem)
    else:
        print("No problems found. All tags are properly nested and closed.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python TAGCHECKER.py <filename>")
    else:
        check_tags(sys.argv[1])
