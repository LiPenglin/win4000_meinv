import jieba
import jieba.posseg as pseg

from nlp.db import MongoClient
from nlp.config import *

class Tokenizer(object):
    def __init__(self):
        self._db = MongoClient()
        # 去停词
        self._stopwords = []
        with open(STOP_WORDS, mode='r', encoding='utf-8') as f:
            for w in f:
                self._stopwords.append(w.strip())
    def get_topN_tags(self):
        print('topN ...')
        word_list = []
        for meinv in self._db.get_meinv(key='meinv_name', filter={}):
            # 词性判断
            msgs =   [m for m in pseg.cut(meinv) if m.word not in self._stopwords and m.flag is 'n']
            word_list.extend([key for key, value in msgs]) # 添加所有word
        word_set = set(word_list)
        word_freq_dict = dict()
        for word in word_set:
            if len(word) > 1:
                freq = word_list.count(word)
                word_freq_dict[word] = freq
        tags_list = [k for k, v in sorted(word_freq_dict.items(), key=lambda x : x[1], reverse=True)] # dict根据value降序排序
        return tags_list[0:100] # top100

    def participle(self):
        tags_list = self.get_topN_tags()
        print(tags_list)
        for meinv in self._db.get_meinv(key='meinv_name', filter={}):
            # 全模式
            tags = [m for m in jieba.cut(meinv, cut_all=True) if m in tags_list]
            # 去重复
            if tags:
                tags = set(tags)
            else:
                tags = ['其他']
            pic_list = self._db.get(table=MONGO_TABLE, query={'meinv_name' : meinv})
            # data
            data = {
                'meinv_name' : meinv.strip(),
                'meinv_tags' : list(tags),
                'meinv_pic_list' : list(pic_list)
            }
            self._db.put(table=MONGO_YIERLING, data=data)
            print(meinv, 'ok...')
        print('yierling ok...')


if __name__ == '__main__':
    tn = Tokenizer()
    tn.participle()