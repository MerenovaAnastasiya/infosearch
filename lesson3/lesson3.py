import os
import re
import util.file_helper as fh

lem_directory = '/Users/a.merenova/Desktop/projects/python/infosearch/lems'
out_directory = '/Users/a.merenova/Desktop/projects/python/infosearch/lesson3'


def write_stat_to_file(stat):
    out_file_name = fh.get_file_name('stat.txt', out_directory)
    file = open(str(out_file_name), 'w')
    for key in stat:
        file.write(key + ' ' + str(stat.get(key)) + "\n")


def collect_stat():
    file_names = os.listdir(lem_directory)
    stat = dict()
    for file_name in file_names:
        collect_statistic(stat, fh.get_file_name(file_name, lem_directory))
    return stat


def collect_statistic(stat, file_name):
    with open(file_name, 'r') as file:
        for line in file:
            words = line.split(' ')
            for word in words:
                word_stat = stat.get(word)
                if word_stat is None:
                    stat.update({word: [os.path.basename(file_name)]})
                else:
                    if os.path.basename(file_name) not in word_stat:
                        word_stat.append(os.path.basename(file_name))
                        stat.update({word: word_stat})


def main():
    stat = collect_stat()
    write_stat_to_file(stat)
    analyze_query(stat)


def analyze_query(stat):
    all_files = set(os.listdir(lem_directory))
    while True:
        print('Введите запрос:')
        query = input()
        words = re.findall('!*[а-яА-Я]+', query)
        operations = re.findall('&|\\|', query)
        word_groups = list()
        word_group_count = -1
        for i in range(len(words)):
            if i == 0:
                word_groups.append([words[i]])
                word_group_count += 1
            elif operations[i - 1] == '&':
                word_groups[word_group_count].append(words[i])
            else:
                word_groups.append([words[i]])
        result = set()
        for group in word_groups:
            group_result = set()
            for i in range(len(group)):
                word = group[i]
                word_result = set()
                clean_word = word[1:] if str(word).startswith('!') else word
                word_files = set() if stat.get(clean_word) is None else set(stat.get(clean_word))
                if not str(word).startswith('!'):
                    word_result = word_result.union(word_files)
                else:
                    word_result = all_files - word_files
                group_result = word_result if i == 0 else group_result.intersection(word_result)
            result = result.union(group_result)
        if len(result) == 0:
            print('Результатов не найдено')
        else:
            print(result)


if __name__ == '__main__':
    main()



# работа | проект & хабр
# работа | жизнь
# проект & срок
# дофига
# дофига & литература
# причина & специалист | дофига
# ящик & почтовый | дофига
# ящик & нетривиальный & область | дофига