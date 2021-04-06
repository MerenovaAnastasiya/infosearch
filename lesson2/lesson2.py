import os
import re
from pymystem3 import Mystem
import util.file_helper as fh


def main():
    in_directory = "/Users/a.merenova/Desktop/projects/python/infosearch/files"
    out_directory = "/Users/a.merenova/Desktop/projects/python/infosearch/lems"
    file_names = os.listdir(in_directory)
    os.mkdir(out_directory)
    for i in range(len(file_names)):
        out_file_name = 'file' + str(i) + '.txt'
        analyze_text(fh.get_file_name(file_names[i], in_directory), fh.get_file_name(out_file_name, out_directory))


def analyze_text(file_in_name, file_out_name):
    file_out = open(file_out_name, 'w')
    with open(file_in_name, 'r') as file_in:
        for line in file_in:
            lemmas = lemmatize(line)
            file_out.write(' '.join(lemmas))
    file_out.close()


def lemmatize(text):
    text = text.lower()
    # text = ' '.join(re.findall('[а-яА-Я]+', text))
    if len(text) > 0:
        my_stem = Mystem()
        lemmas = my_stem.lemmatize(text)
        lemmas = list(filter(lambda x: re.match('^[а-яА-Я]+$', x) is not None, lemmas))
        return lemmas
    else:
        return list()


if __name__ == '__main__':
    main()