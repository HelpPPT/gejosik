from konlpy.tag import Kkma
from tagtokorean import data

def has_batchim(word):    #아스키(ASCII) 코드 공식에 따라 입력된 단어의 마지막 글자 받침 유무를 판단해서 뒤에 붙는 조사를 리턴하는 함수
      last = word[-1]     #입력된 word의 마지막 글자를 선택해서
      criteria = (ord(last) - 44032) % 28     #아스키(ASCII) 코드 공식에 따라 계산 (계산법은 다음 포스팅을 참고하였습니다 : http://gpgstudy.com/forum/viewtopic.php?p=45059#p45059)
      if criteria == 0:       #나머지가 0이면 받침이 없는 것
          return False
      else:                   #나머지가 0이 아니면 받침 있는 것
          return True

class Gejosik:
    tagger = ''

    def __init__(self, *args):
        if len(args) == 0:
            self.tagger = Kkma()
        elif len(args) == 1:
            self.tagger = args[0]
        else:
            raise ValueError('인자는 0개 또는 konlpy tagger 1개 입니다.')
    
    def vocab(self, vocab: str):
        vocab = vocab.removesuffix('.')
        t_vocabs = self.tagger.pos(vocab)
        # print(t_vocabs)
        
        idx = 0
        for i in range(0, len(t_vocabs)):
            (t_vocab, t_vocab_type) = t_vocabs[i]
            if not (t_vocab_type.startswith('V') or t_vocab_type.startswith('N') or t_vocab_type.startswith('XR')):
                break
            idx = i
        
        hannanum_vocab = ''

        (t_vocab, t_vocab_type) = t_vocabs[idx]
        if t_vocab_type.startswith('V') :
          if has_batchim(t_vocab):
            # 종성이 ㅂ 인가 확인
            last_character = t_vocab[-1]
            jong_sung_idx = (ord(last_character) - 0xAC00) % 28
            jong_sung = jong_sung_idx + 0x11A8 - 1
            if(jong_sung == 4536):
                # 17 제거
                hannanum_vocab = t_vocab[0: -1] + chr(ord(last_character) - 17) + '움'
            else:
                hannanum_vocab = t_vocab + '음'
          else:
            last_letter = t_vocab[-1]
            batchim_last_letter = chr(ord(last_letter) + 16) # 16 더해줄 경우 ㅁ 받침 추가
            hannanum_vocab = t_vocab[0: -1] + batchim_last_letter
        elif t_vocab_type.startswith('N') or t_vocab_type.startswith('XR'):
            hannanum_vocab = t_vocab
        
        # print(t_vocabs)
        n_t_vocabs = []
        for item in t_vocabs:
            word, tag = item
            korean_tag = data[tag]
            n_t_vocabs.append((word, tag, korean_tag))

        ans = ""
        for i in range(0, idx):
            ans += t_vocabs[i][0]
        ans += hannanum_vocab

        return ans

    def sentence(self, sentence):
        idx = sentence.rfind(' ')
        if idx == -1:
            return self.vocab(sentence)
        temp_sentence = sentence[0:idx + 1]
        last_word = sentence[idx + 1: ]
        gejosik_word = self.vocab(last_word)
        return temp_sentence + gejosik_word