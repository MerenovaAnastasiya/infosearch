import os
import util.file_helper as fh
import math
import csv

lem_directory = '/Users/a.merenova/Desktop/projects/python/infosearch/lems'
res_directory = '/Users/a.merenova/Desktop/projects/python/infosearch/lesson4/result'
tf_accuracy = 5
idf_accuracy = 5
tf_idf_accuracy = 5


def main():
    file_names = os.listdir(lem_directory)
    word_idf = calculate_idf(file_names)
    # idf_result_file = fh.get_file_name('idf.csv', res_directory)
    # tf_idf_result_file = fh.get_file_name('tf_idf.csv', res_directory)
    for file_name in file_names:
        file = open(fh.get_file_name(file_name, res_directory), 'w')
        all_words = get_all_words_in_file(file_name)
        words_tf = {}
        for word in all_words:
            word_tf = calculate_tf_by_word(word, all_words)
            words_tf.update({word: word_tf})
        for key in words_tf:
            tf = words_tf.get(key)
            idf = word_idf.get(key)
            tf_idf = calculate_tf_idf(tf, idf)
            file.write(key + ' tf=' + str(tf) + ' idf=' + str(idf) + ' tf-idf=' + str(tf_idf) + '\n')

    # result_map = {}
    # for file_name in file_names:
    #     all_file_words = get_all_words_in_file(file_name)
    #     for word in all_file_words:
    #         word_stat = {}
    #         if result_map.get(word) is not None:
    #             word_stat = result_map.get(word)
    #         word_tf = calculate_tf_by_word(word, all_file_words)
    #         word_stat.update({word: word_tf})
    #         result_map.update({word: word_stat})
    # print(word_stat)


    # file.close()
    # columns = list('') + file_names
    # with open(tf_result_file, '', newline='') as csv_file:
    #     writer = csv.writer(csv_file, delimiter=',')
    #     for column in columns:
    #         writer.writerow(column)
    # file_words_tf = {}
    #
    # write_tf_result()


# def write_tf_result(column_names, ):
#     tf_result_file = fh.get_file_name('tf.csv', res_directory)

def calculate_idf(file_names):
    word_idf = {}
    files_count = len(file_names)
    word_file_occurrences = count_word_occurrences(file_names)
    for key in word_file_occurrences:
        word_idf.update({key: calculate_idf_for_word(word_file_occurrences.get(key), files_count)})
    return word_idf


def count_word_occurrences(file_names):
    word_file_occurrences = {}
    for file_name in file_names:
        all_unique_words = set(get_all_words_in_file(file_name))
        for word in all_unique_words:
            if word_file_occurrences.get(word) is not None:
                word_file_occurrences.update({word: word_file_occurrences.get(word) + 1})
            else:
                word_file_occurrences.update({word: 1})
    return word_file_occurrences


def calculate_tf_idf(tf, idf):
    return round(tf * idf, tf_idf_accuracy)


def calculate_idf_for_word(word_occurrences, all_files_count):
    return round(math.log2(all_files_count / word_occurrences), idf_accuracy)


def calculate_tf_by_word(word, all_words):
    occurrences = calculate_occurrences(word, all_words)
    return round(occurrences / len(all_words), tf_accuracy)


def calculate_tf_by_occurrences(occurrences, all_words_count):
    return round(occurrences / all_words_count, tf_accuracy)


def calculate_occurrences(search_word, all_words):
    count = 0
    for word in all_words:
        if search_word == word:
            count += 1
    return count


def get_all_words_in_file(file_name):
    all_words_in_file = list()
    with open(fh.get_file_name(file_name, lem_directory), 'r') as file:
        for line in file:
            words = line.lower().split()
            all_words_in_file = all_words_in_file + list(words)
    file.close()
    return all_words_in_file


if __name__ == '__main__':
    main()
