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
        vocab = vocab.removesuffix('.') # . 제거
        parsed_morphemes = self.tagger.pos(vocab)

        parsed_morphemes_tagged = []
        for item in parsed_morphemes:
            word, tag = item
            korean_tag = data[tag]
            parsed_morphemes_tagged.append((word, tag, korean_tag))
        
        # 의미없는 형태소 추출
        meaningless_morpheme_idx = -1
        for i in range(0, len(parsed_morphemes)):
            (morpheme_word, morpheme_type) = parsed_morphemes[i]
            if morpheme_type.startswith('V') or morpheme_type.startswith('N') or morpheme_type.startswith('XR'):
                break
            else:
                meaningless_morpheme_idx = i

        # 의미있는 형태소 추출
        meaningful_morpheme_idx = -1
        for i in range(meaningless_morpheme_idx + 1, len(parsed_morphemes)):
            (morpheme_word, morpheme_type) = parsed_morphemes[i]
            if not (morpheme_type.startswith('V') or morpheme_type.startswith('N') or morpheme_type.startswith('XR')):
                break
            else:
                meaningful_morpheme_idx = i
        
        gejosik_morpheme = ''

        if meaningful_morpheme_idx == -1:
            vocab_result = {
            'selected_vocab': "",
            'gejosik_vocab': "",
            'morphemes': "",
            'meaningless_morphemes': "",
            'meaningful_morphemes': "",
            }
            return vocab_result

        (morpheme_word, morpheme_type) = parsed_morphemes[meaningful_morpheme_idx]
        if morpheme_type.startswith('V'):
            if has_batchim(morpheme_word):
                # 종성이 ㅂ 인가 확인
                last_character = morpheme_word[-1]
                jong_sung_idx = (ord(last_character) - 0xAC00) % 28
                jong_sung = jong_sung_idx + 0x11A8 - 1
                if(jong_sung == 4536):
                    # 17 제거
                    gejosik_morpheme = morpheme_word[0: -1] + chr(ord(last_character) - 17) + '움'
                else:
                    gejosik_morpheme = morpheme_word + '음'
            else:
                last_letter = morpheme_word[-1]
                batchim_last_letter = chr(ord(last_letter) + 16) # 16 더해줄 경우 ㅁ 받침 추가
                gejosik_morpheme = morpheme_word[0: -1] + batchim_last_letter
        elif morpheme_word == '하다':
            gejosik_morpheme = '함'
        elif morpheme_type.startswith('N') or morpheme_type.startswith('XR'):
            gejosik_morpheme = morpheme_word

        gejosik_vocab = ""
        for i in range(0, meaningful_morpheme_idx):
            gejosik_vocab += parsed_morphemes[i][0]
        gejosik_vocab += gejosik_morpheme

        meaningful_morphemes = parsed_morphemes_tagged[meaningless_morpheme_idx + 1 : meaningful_morpheme_idx + 1]
        to_change = False
        if len(meaningful_morphemes) >= 1:
            if meaningful_morphemes[0][1].startswith("V") == True:
                to_change = True

        vocab_result = {
            'selected_vocab': vocab,
            'gejosik_vocab': gejosik_vocab,
            'morphemes': parsed_morphemes_tagged,
            'meaningless_morphemes': parsed_morphemes_tagged[0: meaningless_morpheme_idx + 1],
            'meaningful_morphemes': meaningful_morphemes,
            'to_change': to_change,
        }

        return vocab_result

    def sentence(self, sentence):
        space_leftside_of_last_word_idx = sentence.rfind(' ')

        sentence_result = {'original_sentence': sentence}
        # 한 단어로만 이루어진 문장이 들어온 경우
        if space_leftside_of_last_word_idx == -1:
            vocab_result = self.vocab(sentence)

            sentence_result.update(vocab_result)
            sentence_result['gejosik_sentence'] = vocab_result['gejosik_vocab']
        # 여러 단어로 이루어진 문장이 들어온 경우
        else:
            sentence_wo_last_vocab = sentence[0:space_leftside_of_last_word_idx + 1]
            # 마지막 단어만 추출해서 처리
            last_vocab = sentence[space_leftside_of_last_word_idx + 1:]
            vocab_result = self.vocab(last_vocab)

            sentence_result.update(vocab_result)
            sentence_result['gejosik_sentence'] = sentence_wo_last_vocab + vocab_result['gejosik_vocab']

        return sentence_result