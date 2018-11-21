import urllib3
import requests
import json
import pymysql
import uuid
import ssl
import numpy as np
from gensim.models import word2vec
import tensorflow as tf
import jieba
import re
import threading
import time
import datetime
import os
import test
from emotionAlynasis import test



class SentimentAlynasis(object):
    def __init__(self):
        self.connection = pymysql.connect(host='xxxxxx',
                                 user='xxxxxx',
                                 password='xxxxxx',
                                 db='xxxxxx',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()
        self.sess = tf.InteractiveSession()
        self.OBPATH = os.path.abspath('..')
        print(self.OBPATH)
        numDimensions = 100
        self.maxSeqLength = 100
        self.batchSize = 32
        lstmUnits = 64
        numClasses = 2
        iterations = 250000
        model = word2vec.Word2Vec.load(self.OBPATH + "/emotionAlynasis/w2v613")
        wordVectors = np.array([model[word] for word in (model.wv.vocab)])
        self.wordsList = np.array([word for word in (model.wv.vocab)])

        # wordsList = np.load('wordsList.npy')
        print('Loaded the word list!')
        self.wordsList = self.wordsList.tolist()  # Originally loaded as numpy array
        self.wordsList = [word for word in self.wordsList]  # Encode words as UTF-8
        # tf.reset_default_graph()
        self.graph = tf.get_default_graph()
        with self.graph.as_default():
            labels = tf.placeholder(tf.float32, [self.batchSize, numClasses])
            self.input_data = tf.placeholder(tf.int32, [self.batchSize, self.maxSeqLength])

            data = tf.Variable(tf.zeros([self.batchSize, self.maxSeqLength, numDimensions]), dtype=tf.float32)
            data = tf.nn.embedding_lookup(wordVectors, self.input_data)

            lstmCell = tf.contrib.rnn.BasicLSTMCell(lstmUnits)
            lstmCell = tf.contrib.rnn.DropoutWrapper(cell=lstmCell, output_keep_prob=1)
            value, _ = tf.nn.dynamic_rnn(lstmCell, data, dtype=tf.float32)

            weight = tf.Variable(tf.truncated_normal([lstmUnits, numClasses]))
            bias = tf.Variable(tf.constant(0.1, shape=[numClasses]))
            value = tf.transpose(value, [1, 0, 2])
            last = tf.gather(value, int(value.get_shape()[0]) - 1)
            self.prediction = (tf.matmul(last, weight) + bias)

            correctPred = tf.equal(tf.argmax(self.prediction, 1), tf.argmax(labels, 1))
            accuracy = tf.reduce_mean(tf.cast(correctPred, tf.float32))
            saver = tf.train.Saver()
            path = self.OBPATH + '/emotionAlynasis/model_comment_613'
            # path = 'C://Users/Administrator/models'
            saver.restore(self.sess, tf.train.latest_checkpoint(path))
            # inputText = str(' '.join(jieba.cut("傻逼东西")))
            # inputMatrix = self.getSentenceMatrix(inputText)
            # predictedSentiment = self.sess.run(self.prediction, {self.input_data: inputMatrix})[0]
            # print(predictedSentiment)
        print("从 " + path + " 加载神经网络模型模型加载完毕")


        self.nag_list = list()
        with open(self.OBPATH + '/emotionAlynasis/p2p平台负面词词典.txt', 'r', encoding='utf-8') as f:
            while 1:
                line = f.readline()
                if line:
                    self.nag_list.append(line.split('/n')[0])
                else:
                    break


    def emotion_alynasis(self, text):
        host = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=24.79a4660b45fdcea8f246909f83f5ea' \
            'a4.2592000.1532572400.282335-11186693'
        body = json.dumps({'text': text})
        r = requests.post(url=host,
                        data=body,
                        headers={'Content-Type': 'application/json'})
        result = eval(str(r.content, encoding='gbk'))
        try:
            return 1 if result['items'][0]['positive_prob'] > 0.6 else 0
        except KeyError:
            print(text)
            return 0


    def emotion_alynasis_2(self, text):
        # tf.reset_default_graph()
        with self.graph.as_default():
            inputText = str(' '.join(jieba.cut(text)))
            inputMatrix = self.getSentenceMatrix(inputText)
            predictedSentiment = self.sess.run(self.prediction, {self.input_data: inputMatrix})[0]
        if (predictedSentiment[0] > predictedSentiment[1]):
            return 1
        else:
            return 0

    def batch_insert(self):
        sql = "SELECT `comment` FROM `platform_review` LIMIT 17940, 50000"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print("数据读取成功,开始插入数据")
        # Create a new record
        count = 0
        for d in result:
            target = d['comment']
            tb_id = uuid.uuid1()
            sql = "INSERT INTO `tp_emotionscore` (`uuid`, `comment`, `postive_score`) VALUES (%s, %s, %s)"
            try:
                em_score = self.emotion_alynasis(target)
            except KeyError:
                em_score = self.emotion_alynasis(target)
            self.cursor.execute(sql, (str(tb_id), target, em_score))
            if count % 300 == 0:
                print("已处理"+str(count)+"条信息")
            count = count + 1
        self.connection.commit()


    def news_alynasis(self,text):
        badword_flag = 0
        for w in self.nag_list:
            if str(text).count(w) > 0:
                badword_flag = 1
                break
        if badword_flag == 1:
            score = 0
        else:
            score = 1
        return score


    def getSentenceMatrix(self, sentence):
        sentenceMatrix = np.zeros([self.batchSize, self.maxSeqLength], dtype='int32')
        split = sentence.split()
        for indexCounter, word in enumerate(split):
            try:
                sentenceMatrix[0, indexCounter] = self.wordsList.index(word)
            except ValueError:
                try:
                    sentenceMatrix[0, indexCounter] = 10000  # Vector for unkown words
                except IndexError:
                    pass
            except IndexError:
                pass
        return sentenceMatrix

    
    def tagbatchpush(self):
        id_max = 0
        id_min = 0
        threadlist = []
        date = str(datetime.date.today())
        datasql = 'SELECT MAX(`id`) AS maxid, MIN(`id`) as minid FROM `tp_comment_info` WHERE `update_date` = %s'
        self.cursor.execute(datasql, date)
        data_result = self.cursor.fetchall()
        id_max = data_result[0]['maxid']
        id_min = data_result[0]['minid']
        self.connection.commit()

        start = id_min
        count = id_max - id_min
        thread_num = 15
        margin = int(count / thread_num) + 1
        print('start, count, margin:', start, count, margin)
        for i in range(thread_num):
            threadlist.append(TagPushThread(i, 'thread-'+str(i), start, margin, self))
            start += margin
        for _t in threadlist:
            _t.start()
        for _t in threadlist:
            _t.join()
        return 1

    def all_tag_rank(self, result_1, tag_count, taglist=list()):
            a = np.zeros(len(taglist))
            for _rr in result_1:
                try:
                    a = a + np.array(str(_rr['tag']).split(), dtype='int16')
                except ValueError:
                    pass
            total = np.sum(a)

            tag_percentlist = list()
            for _ in range(tag_count):
                tag_percentlist.append([taglist[_], a[_]])
            b = dict(tag_percentlist)
            list_temp = zip(b.values(), b.keys())
            list_temp = sorted(list_temp, reverse=True)
            list_temp = np.array(list_temp)
            ng_dict = dict() # name-group字典
            ng_sql = "SELECT `tag_name`, `tag_group` FROM `tp_tag_index`"
            self.cursor.execute(ng_sql)
            ng_result = self.cursor.fetchall()
            g_list = []
            rank_dict = dict()
            for ng in ng_result:
                ng_dict[ng['tag_name']] = ng['tag_group']
                # if g_list.count(ng['tag_group']) == 0:
                g_list.append(ng['tag_group'])
            g_list = np.array(g_list)
            list_temp_0 = np.array(list_temp[:, 0], dtype="float32")
            for g in g_list:
                # print(list_temp_0, list_temp_0[np.where(g_list == g)], np.where(g_list == g))
                rank_dict[g] = float(np.sum(list_temp_0[np.where(g_list == g)]))
            return json.dumps(rank_dict, ensure_ascii=False)


    def tag_abstract(self):
        sql_2 = "SELECT `tag_name`, `tag_index` FROM `tp_tag_index`"
        self.cursor.execute(sql_2)
        result_2 = self.cursor.fetchall()
        tag_count = len(result_2)
        tag_list = [0 for i in range(tag_count)]
        for _r in result_2:
            tag_list[int(_r['tag_index'])] = _r['tag_name']
        sql = "SELECT `net_name`, `id` FROM tp_com_info"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        sql2 = "INSERT INTO tp_bad_percent(`pid`, `percent`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `percent` = %s"
        sql3 = "SELECT `tag` FROM tp_comment_info WHERE `pid` = %s AND `comm_score` = 0 ORDER BY `comm_time`"
        count = 0
        for _r in result:
            self.cursor.execute(sql3, _r['id'])
            result2 = self.cursor.fetchall()
            tag_ranked = self.all_tag_rank(result2, tag_count, taglist=tag_list)
            tag_ranked = str(tag_ranked)[1:-1]
            # print(tag_ranked, _r['id'])
            self.cursor.execute(sql2, (_r['id'], tag_ranked, tag_ranked))
            # cursor.execute(sql2, (_tag, _r['id']))
            if count % 500 == 0:
                print("已处理"+str(count)+"条信息")
            count += 1
        return 1

    def opscoreperday(self):
        comlist, idlist = test.getcomdata()
        idlist.append(0)
        thetime = time.time()
        thedate = int(thetime - thetime % (3600 * 24)-3600*8) # 获取当日时间戳，即时时间戳减去和一天秒数的余数减去时区
        for i in idlist:
            score = test.getscorelist_perday(company_id=i, thedate=thedate)
            sql = 'INSERT INTO `tp_opinion_score`(`pid`, `score`, `createtime`) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE `score`=%s'
            self.cursor.execute(sql, (i, score, thedate, score))
        self.connection.commit()
        return 1

class TagPushThread (threading.Thread):
    def __init__(self, threadid, name, startid, margin, alynasisor):
        threading.Thread.__init__(self)
        self.OBPATH = os.path.abspath('..')
        self.threadid = threadid
        self.name = name
        self.startid = startid
        self.margin = margin
        self.connection = pymysql.connect(host='xxxxxx',
                                 user='xxxxxx',
                                 password='s@11##!4',
                                 db='xxxxxx',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()
        self.tag_dict = dict()         # 评论标签数组化
        sql = "SELECT `tag_name`, `tag_index` FROM `tp_tag_index`"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.connection.commit()
        print("数据读取成功")
        for r in result:
            self.tag_dict[r['tag_name']] = r['tag_index']
        self.nagtive_worddict = dict()
        with open(self.OBPATH + "/emotionAlynasis/负面词典.txt", "r", encoding="utf-8") as f:
            while 1:
                line = f.readline()
                if line:
                    self.nagtive_worddict[line.split()[0]] = line.split()[1]
                else:
                    break
        self.alynasisor = alynasisor

    def tag_abstract(self, sentence=""):
        # 切割句子成汉字短语
        tag_list = list()
        sentence_split = re.split(r'([\u4e00-\u9fa5]+)', sentence, flags=re.I)
        sentence_zh = filter(lambda x: re.match(r'([\u4e00-\u9fa5]+)', x, re.M | re.I), sentence_split)
        nagtive_word_key = self.nagtive_worddict.keys()
        for _s in sentence_zh:
            if self.alynasisor.emotion_alynasis_2(_s) == 0:
                for _k in nagtive_word_key:
                    if _s.count(_k) > 0 and tag_list.count(self.nagtive_worddict[_k]) == 0:
                        tag_list.append(self.nagtive_worddict[_k])
        return tag_list

    def tag_transform(self, sentence=""):
        tag_list = [0] * len(self.tag_dict)
        sentence_tag_list = self.tag_abstract(sentence)
        for _s in sentence_tag_list:
            tag_list[int(self.tag_dict[_s])] = 1
        return tag_list


    def run(self):
        starttime = time.time()
        tag_sql = 'SELECT `id`, `comm_info` FROM `tp_comment_info` WHERE `id` > %s AND `id` < %s'
        update_sql = 'UPDATE `tp_comment_info` SET `tag` = %s WHERE `id` = %s'
        endid = self.startid + self.margin
        self.cursor.execute(tag_sql, (self.startid - 1, endid))
        tag_result = self.cursor.fetchall()
        # lock.release()
        count = 0
        for _r in tag_result:
            print('正在执行....')
            tag = self.tag_transform(_r['comm_info'])
            # lock.acquire()
            self.cursor.execute(update_sql, (str(tag)[1:-1].replace(',', ''), _r['id']))
            count += 1
            if count % 100 == 0:
                print('线程', self.threadid, '剩余：', self.margin - count)
        self.connection.commit()
        print('线程', self.threadid, '结束', '耗时', time.time()-starttime)