"""
bibtex格式的文献解析器
详细：https://blog.csdn.net/qq_37607269/article/details/113267279
"""
import bibtexparser
from bibtexparser.bparser import BibTexParser

from .customization import *


def customizations(record):
    """
    加载自定义的内容
    :param record:
    :return:
    """
    record = author(record)
    record = title(record)
    record = unique_id(record)
    record = doi(record)
    record = journal(record)
    return record


def parse_bib_str(bib_str: str):
    """
    传入bibtex格式的字符串,解析为以字典为元素的list
    :param bib_str:
    :return: list  (item is dic)
    """
    bib_str = bib_str.replace('{{', '{').replace('}}', '}').replace('Early Access Date', 'Early-Access-Date').replace(
        'Early Access Year', 'Early-Access-Year')
    parser = BibTexParser()
    parser.customization = customizations
    bib_datebase = bibtexparser.loads(bib_str, parser=parser)
    return bib_datebase.entries


if __name__ == '__main__':
    with open('1.bib', encoding='utf-8') as bib_file:
        bib_str = bib_file.read()
    entries = parse_bib_str(bib_str)
    print(len(entries))
    for i in entries:
        print(i.keys())
        print('#' * 50)
        input('press')
