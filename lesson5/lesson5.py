import os

import lesson2.lesson2 as l2
import lesson4.lesson4 as l4

lem_directory = '/Users/a.merenova/Desktop/projects/python/infosearch/lems'


def search_word_vector(words, all_unique_words):
    file_names = os.listdir(lem_directory)
    vector = list()
    word_occurrences = {}
    for word in words:
        if word_occurrences.get(word) is None:
            word_occurrences.update({word: 1})
        else:
            word_occurrences.update({word: word_occurrences.get(word) + 1})
    max_occurrences = 0
    for word in words:
        occurrences = word_occurrences.get(word)
        if occurrences > max_occurrences:
            max_occurrences = occurrences

    words_idf = l4.calculate_idf(file_names)
    for word in all_unique_words:
        idf = 0 if word not in words else words_idf.get(word)
        if idf == 0:
            vector.append(0)
        else:
            vector.append(idf * word_occurrences.get(word) / max_occurrences)
    # for word in words:
    #     idf = 0 if words_idf.get(word) is None else words_idf.get(word)
    #     vector.append(idf * word_occurrences.get(word)/max_occurrences)
    return vector


def calculate_vector_length(vector):
    length = 0
    for coordinate in vector:
        length += coordinate ** 2
    return length


def find_all_unique_words(file_names):
    all_unique_words = set()
    for file in file_names:
        all_unique_words.update(set(l4.get_all_words_in_file(file)))
    return list(all_unique_words)


def get_all_file_names():
    return os.listdir(lem_directory)


def calculate_file_vector(file_name, all_unique_words, words_idf):
    all_file_words = l4.get_all_words_in_file(file_name)
    vector = list()
    for word in all_unique_words:
        if word in all_file_words:
            tf = l4.calculate_tf_by_word(word, all_file_words)
            idf = words_idf.get(word)
            tf_idf = l4.calculate_tf_idf(tf, idf)
            vector.append(tf_idf)
        else:
            vector.append(0)
    return vector


def main():
    print('Введите Ваш запрос')
    query = input()
    all_file_names = get_all_file_names()
    all_unique_words = find_all_unique_words(all_file_names)
    words = l2.lemmatize(query)
    vector = search_word_vector(words, all_unique_words)
    vector_length = calculate_vector_length(vector)
    print('vector = ' + str(vector))
    print('vector length = ' + str(vector_length))
    words_idf = l4.calculate_idf(all_file_names)
    cos_sim = {}
    for file_name in all_file_names:
        file_vector = calculate_file_vector(file_name, all_unique_words, words_idf)
        file_vector_length = calculate_vector_length(file_vector)
        vector_multiplication = 0
        for i in range(len(all_unique_words)):
            query_vector_coordinate = vector[i]
            file_vector_coordinate = file_vector[i]
            vector_multiplication += query_vector_coordinate * file_vector_coordinate
        res = round(vector_multiplication / (file_vector_length * vector_length), 3)
        cos_sim.update({file_name: res})
    cos_sim = dict(sorted(cos_sim.items(), key=lambda item: item[1], reverse=True))
    print(cos_sim)
    # max_distance = max(cos_sim.items(), key=lambda x: x[1])
    # print(max_distance)


if __name__ == '__main__':
    main()
