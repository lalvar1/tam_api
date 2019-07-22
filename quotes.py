import os

def funny_quotes():
    reports = {}
    report_list = []
    #dir = os.chdir('./tam_api')
    file_obj = open('quotes.txt', 'r')
    text = file_obj.read()
    text = text.split('\n')
    for line in text:
        line = line.strip(',')
        if '{' in line or '}' in line:
            continue
        lines = line.split(':')
        if len(lines) > 1:
            d = {lines[0]: lines[1].strip('"')}
            if 'author' in line:
                aux_dict = d
            elif 'quote' in line:
                aux_dict.update(d)
                report_list.append(aux_dict)
    #text = text.strip().strip().strip('\t')
        report_list = sorted(report_list, key=lambda k: k['author'])
    return report_list

print(funny_quotes())