import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gejosik import Gejosik

g = Gejosik()

file = open('./test/sentences.txt', 'r')
sentences = file.readlines()
sentences = [line.rstrip('\n') for line in sentences]

for sentence in sentences:
    print('=================START==================')
    print(f'original sentence: {sentence}')
    gejosik_sentence = g.sentence(sentence)['gejosik_sentence']
    print(f'gejosik sentence: {gejosik_sentence}')
    print('==================END===================')
