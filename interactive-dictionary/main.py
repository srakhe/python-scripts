from json import load
from difflib import get_close_matches
import re

def load_dict(path):
    with open(path) as file:
        data = load(file)
    return data

def double_check(data,word):
    similar_words = get_close_matches(word=word,possibilities=data.keys(),n=5,cutoff=0.8)
    if similar_words:
        list_words = ''
        i = 1
        for words in similar_words:
            list_words+=(' '+str(i)+'.'+str(words)+',')
            i+=1
        print('Did you mean any of these: %s instead?' % list_words)
        print('If yes, then enter the number of the word, if no, then click enter to exit!')
        correct_word_pos = input()
        if correct_word_pos:
            print('Okay, looking for %s instead :)' % similar_words[int(correct_word_pos)-1])
            return get_meaning(data, similar_words[int(correct_word_pos)-1])

def get_meaning(data,word):
    word = str.lower(word)
    if word in data:
        return data[word]
    else:
        print('The word doesnt exist!')
        return double_check(data,word)

if __name__ == '__main__':
    data = load_dict('dictionary.json')
    meaning = get_meaning(data,input('Enter the word to search please: '))
    if meaning:
        lines = re.split('\d.',meaning)
        for line in lines:
            if not line == ' ':
                print(line)