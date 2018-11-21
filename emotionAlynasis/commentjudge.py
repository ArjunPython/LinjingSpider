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
import os

OBPATH = os.path.abspath('..')
numDimensions = 100
maxSeqLength = 100
batchSize = 32
lstmUnits = 64
numClasses = 2
iterations = 250000
model = word2vec.Word2Vec.load(OBPATH + "/emotionAlynasis/w2v613")
wordVectors = np.array([model[word] for word in (model.wv.vocab)])
wordsList = np.array([word for word in (model.wv.vocab)])

# wordsList = np.load('wordsList.npy')
print('Loaded the word list!')
wordsList = wordsList.tolist()  # Originally loaded as numpy array
wordsList = [word for word in wordsList]  # Encode words as UTF-8
tf.reset_default_graph()

labels = tf.placeholder(tf.float32, [batchSize, numClasses])
input_data = tf.placeholder(tf.int32, [batchSize, maxSeqLength])

data = tf.Variable(tf.zeros([batchSize, maxSeqLength, numDimensions]), dtype=tf.float32)
data = tf.nn.embedding_lookup(wordVectors, input_data)

lstmCell = tf.contrib.rnn.BasicLSTMCell(lstmUnits)
lstmCell = tf.contrib.rnn.DropoutWrapper(cell=lstmCell, output_keep_prob=1)
value, _ = tf.nn.dynamic_rnn(lstmCell, data, dtype=tf.float32)

weight = tf.Variable(tf.truncated_normal([lstmUnits, numClasses]))
bias = tf.Variable(tf.constant(0.1, shape=[numClasses]))
value = tf.transpose(value, [1, 0, 2])
last = tf.gather(value, int(value.get_shape()[0]) - 1)
prediction = (tf.matmul(last, weight) + bias)

correctPred = tf.equal(tf.argmax(prediction, 1), tf.argmax(labels, 1))
accuracy = tf.reduce_mean(tf.cast(correctPred, tf.float32))
sess = tf.InteractiveSession()
saver = tf.train.Saver()
path = OBPATH +'/emotionAlynasis/models_opinioneval'
# path = 'C://Users/Administrator/models'
print('从 ' + path + ' 加载神经网络模型')
saver.restore(sess, tf.train.latest_checkpoint(path))
print("模型加载完毕")


def comment_judge(text):
    inputText = str(' '.join(jieba.cut(text)))
    inputMatrix = getSentenceMatrix(inputText)
    predictedSentiment = sess.run(prediction, {input_data: inputMatrix})[0]
    # predictedSentiment[0] represents output score for positive sentiment
    # predictedSentiment[1] represents output score for negative sentiment
    if (predictedSentiment[0]>predictedSentiment[1]):
        return 1
    else:
        return 0



def getSentenceMatrix(sentence):
    sentenceMatrix = np.zeros([batchSize, maxSeqLength], dtype='int32')
    split = sentence.split()
    for indexCounter, word in enumerate(split):
        try:
            sentenceMatrix[0, indexCounter] = wordsList.index(word)
        except ValueError:
            try:
                sentenceMatrix[0, indexCounter] = 10000  # Vector for unkown words
            except IndexError:
                pass
        except IndexError:
            pass
    return sentenceMatrix
