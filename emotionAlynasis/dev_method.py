from emotionAlynasis import sentiment_alynasis
import pymysql
import _thread
import test
import time
import datetime
import threading
import numpy as np
import json
# import csv
# import gensim
# import jieba
# from gensim.models import word2vec
# from sklearn.manifold import TSNE
# import matplotlib.pyplot as plt
# from matplotlib.font_manager import *
# import commentjudge

'''评论标签提取方法'''
# def tag_rank(result_1, taglist=list()):
#     a = np.zeros(len(taglist))
#     for _rr in result_1:
#         a = a + np.array(str(_rr['tag']).split(), dtype='int16')
#     total = np.sum(a)
#
#     tag_percentlist = list()
#     for _ in range(tag_count):
#         tag_percentlist.append([taglist[_], a[_]])
#     b = dict(tag_percentlist)
#     list_temp = zip(b.values(), b.keys())
#     list_temp = sorted(list_temp, reverse=True)[0:4]
#     rank_dict = dict()
#     percent = 0
#     for _l in list_temp:
#         if _l[0] != 0:
#             rank_dict[_l[1]] = int(_l[0])
#             percent += _l[0]
#         else:
#             pass
#     if total - percent != 0:
#         rank_dict['其他'] = int(total - percent)
#     else:
#         pass
#     return json.dumps(rank_dict, ensure_ascii=False)
#
#
# connection = pymysql.connect(host='xxxxxx',
#                              user='root',
#                              password='root',
#                              db='xxxxxx',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
# try:
#     with connection.cursor() as cursor:
#         sql_2 = "SELECT `tag_name`, `tag_index` FROM `tp_tag_index`"
#         cursor.execute(sql_2)
#         result_2 = cursor.fetchall()
#         tag_count = len(result_2)
#         tag_list = [0 for i in range(tag_count)]
#         for _r in result_2:
#             tag_list[int(_r['tag_index'])] = _r['tag_name']
#         sql = "SELECT `net_name`, `id` FROM tp_com_info"
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         sql2 = "INSERT INTO tp_bad_percent VALUES (%s, %s, %s)"
#         sql3 = "SELECT `tag` FROM tp_comment_info WHERE `pid` = %s AND `comm_score` = 0 "
#         count = 0
#         for _r in result:
#             cursor.execute(sql3, _r['id'])
#             result2 = cursor.fetchall()
#             tag_ranked = tag_rank(result2, taglist=tag_list)
#             tag_ranked = str(tag_ranked)[1:-1]
#             # print(tag_ranked, _r['id'])
#             cursor.execute(sql2, (_r['id'], _r['net_name'], tag_ranked))
#             # cursor.execute(sql2, (_tag, _r['id']))
#             if count % 500 == 0:
#                 print("已处理"+str(count)+"条信息")
#             count += 1
#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()
# finally:
#     connection.close()


'''负面新闻判定'''
# nag_list = list()
# with open('C:\\Users\Administrator\Desktop\p2p平台负面词词典.txt', 'r', encoding='utf-8') as f:
#     while 1:
#         line = f.readline()
#         if line:
#             nag_list.append(line.split('\n')[0])
#         else:
#             break
# print(nag_list)
#
# # with open('C:\\Users\Administrator\Desktop\\tp_news(2).csv', 'r', encoding='utf-8') as f:
# connection = pymysql.connect(host='xxxxxx',
#                              user='root',
#                              password='root',
#                              db='xxxxxx',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
# try:
#     with connection.cursor() as cursor:
#         sql2 = "SELECT `id`, `title` FROM `tp_news`"
#         cursor.execute(sql2)
#         cursor.execute(sql2)
#         result = cursor.fetchall()
#         for r in result:
#             badword_flag = 0
#             for w in nag_list:
#                 if str(r['title']).count(w) > 0:
#                     badword_flag = 1
#                     break
#             if badword_flag == 1:
#                 score = 0
#             else:
#                 score = 1
#
#             sql = "UPDATE `tp_news` SET `postive_score` = %s WHERE `id` = %s"
#             cursor.execute(sql, (score, r['id']))
#         # connection is not autocommit by default. So you must commit to save
#         #                 # your changes.
#         connection.commit()
# finally:
#     connection.close()



# '''评论情感分析入库'''
# connection = pymysql.connect(host='xxxxxx',
#                              user='xxxxxx',
#                              password='xxxxxx',
#                              db='xxxxxx',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
# try:
#     with connection.cursor() as cursor:
#         sql = "UPDATE `tp_comment_info` SET `comm_score` = %s WHERE `id` = %s"
#         sql_2 = "SELECT `id`, `comm_info` FROM `tp_comment_info`"
#         cursor.execute(sql_2)
#         result_2 = cursor.fetchall()
#         count = 0
#         for _r in result_2:
#             score = sentiment_alynasis.emotion_alynasis_2(_r['comm_info'])
#             # print(_r['comm_info'], score)
#             cursor.execute(sql, (score, _r['id']))
#             if count % 1000 == 0:
#                 print(count, "条已处理")
#             count += 1
#
#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()
# finally:
#     connection.close()


# print(sentiment_alynasis.tag_abstract("收利息管理费6%！！！提现也收费，无语"))


'''评论标签提取方法'''
# def tag_rank(result_1, taglist=list()):
#     a = np.zeros(len(taglist))
#     for _rr in result_1:
#         a = a + np.array(str(_rr['tag']).split(), dtype='int16')
#     total = np.sum(a)
#
#     tag_percentlist = list()
#     for _ in range(tag_count):
#         tag_percentlist.append([taglist[_], a[_]])
#     b = dict(tag_percentlist)
#     list_temp = zip(b.values(), b.keys())
#     list_temp = sorted(list_temp, reverse=True)[0:4]
#     rank_dict = dict()
#     percent = 0
#     for _l in list_temp:
#         if _l[0] != 0:
#             rank_dict[_l[1]] = int(_l[0])
#             percent += _l[0]
#         else:
#             pass
#     if total - percent != 0:
#         rank_dict['其他'] = int(total - percent)
#     else:
#         pass
#     return json.dumps(rank_dict, ensure_ascii=False)
#
#
# connection = pymysql.connect(host='xxxxxx',
#                              user='root',
#                              password='root',
#                              db='xxxxxx',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
# try:
#     with connection.cursor() as cursor:
#         sql_2 = "SELECT `tag_name`, `tag_index` FROM `tp_tag_index`"
#         cursor.execute(sql_2)
#         result_2 = cursor.fetchall()
#         tag_count = len(result_2)
#         tag_list = [0 for i in range(tag_count)]
#         for _r in result_2:
#             tag_list[int(_r['tag_index'])] = _r['tag_name']
#         sql = "SELECT `net_name`, `id` FROM tp_com_info"
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         sql2 = "INSERT INTO tp_bad_percent VALUES (%s, %s, %s)"
#         sql3 = "SELECT `tag` FROM tp_comment_info WHERE `pid` = %s AND `comm_score` = 0 "
#         count = 0
#         for _r in result:
#             cursor.execute(sql3, _r['id'])
#             result2 = cursor.fetchall()
#             tag_ranked = tag_rank(result2, taglist=tag_list)
#             tag_ranked = str(tag_ranked)[1:-1]
#             # print(tag_ranked, _r['id'])
#             cursor.execute(sql2, (_r['id'], _r['net_name'], tag_ranked))
#             # cursor.execute(sql2, (_tag, _r['id']))
#             if count % 500 == 0:
#                 print("已处理"+str(count)+"条信息")
#             count += 1
#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()
# finally:
#     connection.close()


'''评论标签提取方法'''
# def all_tag_rank(result_1, taglist=list()):
#     a = np.zeros(len(taglist))
#     for _rr in result_1:
#         try:
#             a = a + np.array(str(_rr['tag']).split(), dtype='int16')
#         except ValueError:
#             pass
#     total = np.sum(a)
#
#     tag_percentlist = list()
#     for _ in range(tag_count):
#         tag_percentlist.append([taglist[_], a[_]])
#     b = dict(tag_percentlist)
#     list_temp = zip(b.values(), b.keys())
#     list_temp = sorted(list_temp, reverse=True)[0:4]
#     rank_dict = dict()
#     percent = 0
#     for _l in list_temp:
#         if _l[0] != 0:
#             rank_dict[_l[1]] = int(_l[0])
#             percent += _l[0]
#         else:
#             pass
#     if total - percent != 0:
#         rank_dict['其他'] = int(total - percent)
#     else:
#         pass
#     return json.dumps(rank_dict, ensure_ascii=False)
#
#
# def gettag_str(tag_index = 0):
#     # sql:SELECT `tag`,REPLACE(tag,' ','') AS b FROM tp_comment_info WHERE `pid` = 2 AND `comm_score` = 0 AND REPLACE(tag,' ','') REGEXP '[0-1]{5}1[0-1]{20}'
#     tag_str = '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'
#     str_index = 2 * tag_index
#
# connection = pymysql.connect(host='xxxxxx',
#                              user='root',
#                              password='root',
#                              db='xxxxxx',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
# try:
#     with connection.cursor() as cursor:
#         sql_2 = "SELECT `tag_name`, `tag_index` FROM `tp_tag_index`"
#         cursor.execute(sql_2)
#         result_2 = cursor.fetchall()
#         tag_count = len(result_2)
#         tag_list = [0 for i in range(tag_count)]
#         for _r in result_2:
#             tag_list[int(_r['tag_index'])] = _r['tag_name']
#         sql = "SELECT `net_name`, `id` FROM tp_com_info"
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         sql2 = "INSERT INTO tp_bad_percent(`pid`, `percent`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `percent` = %s"
#         sql3 = "SELECT `tag` FROM tp_comment_info WHERE `pid` = %s AND `comm_score` = 0 ORDER BY `comm_time`"
#         count = 0
#         for _r in result:
#             cursor.execute(sql3, _r['id'])
#             result2 = cursor.fetchall()
#             tag_ranked = all_tag_rank(result2, taglist=tag_list)
#             tag_ranked = str(tag_ranked)[1:-1]
#             # print(tag_ranked, _r['id'])
#             cursor.execute(sql2, (_r['id'], tag_ranked, tag_ranked))
#             # cursor.execute(sql2, (_tag, _r['id']))
#             if count % 500 == 0:
#                 print("已处理"+str(count)+"条信息")
#             count += 1
#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()
# finally:
#     connection.close()


# '''负面新闻个数入库'''
# connection = pymysql.connect(host='xxxxxx',
#                              user='xxxxxx',
#                              password='xxxxxx',
#                              db='xxxxxx',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
# try:
#     with connection.cursor() as cursor:
#         sql = "SELECT `net_name`, `id` FROM tp_com_info"
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         sql2 = "INSERT INTO `tp_news_count` VALUES (%s, %s, %s)"
#         sql3 = "SELECT `platform`, COUNT(`id`) AS b FROM `tp_news` WHERE `content` LIKE %s AND " \
#                "`postive_score` = 0 GROUP BY `platform` ORDER BY b DESC LIMIT 0,15"
#         sql4 = "SELECT COUNT(`id`) AS b FROM `tp_news` WHERE `content` LIKE %s AND `postive_score` = 0"
#         for _r in result:
#             result_dict = {}
#             cursor.execute(sql3, "%"+_r['net_name']+"%")
#             result2 = cursor.fetchall()
#             for r in result2:
#                 result_dict[r['platform']] = r['b']
#             cursor.execute(sql4, "%" + _r['net_name'] + "%")
#             result3 = cursor.fetchall()
#             pn_rank = str(json.dumps(result_dict, ensure_ascii=False))[1:-1]
#             cursor.execute(sql2, (_r['id'], pn_rank, result3[0]['b']))
#             # print(result2)
#             # print(tag_ranked, _r['id'])
#             # cursor.execute(sql2, (_r['id'], _r['net_name'], tag_ranked))
#             # cursor.execute(sql2, (_tag, _r['id']))
#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()
# finally:
#     connection.close()

'''词向量训练'''
# wf = open('C:\\Users\Administrator\Desktop\负面新闻语料_cut.txt', 'w', encoding='utf-8')
# with open('C:\\Users\Administrator\Desktop\负面新闻语料.txt',encoding='utf-8') as f:
#     while 1:
#         line = f.readline()
#         if line:
#             wf.write(str(' '.join(jieba.cut(line))+ '\n'))
#         else:
#             break
# wf.close()
# sentences = word2vec.LineSentence("C:\\Users\Administrator\Desktop\总评论_cut.txt")
# model = word2vec.Word2Vec(sentences, size=100, hs=1, negative=0)
#
#
# def plot_with_labels(low_dim_embs, labels, filename='tsne.png'):
#     assert low_dim_embs.shape[0] >= len(labels), "More labels than embedings"
#     plt.figure(figsize=(25, 25))
#     for i, label in enumerate(labels):
#         x, y = low_dim_embs[i,:]
#         plt.scatter(x, y)
#         plt.annotate(label,
#                     xy=(x, y),
#                     xytext=(5,2),
#                     textcoords='offset points',
#                     ha='right',
#                     va='bottom')
#     plt.show
#     plt.savefig(filename)
#
#
# # myfont = FontProperties(fname='/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc')
# plt.rcParams.update({
#     'font.family':'sans-serif',
#     'font.sans-serif':['simfang'],
#     })
# plt.rcParams['font.sans-serif'] = ['FangSong']
# plt.rcParams['font.serif'] = ['FangSong']
# plt.rcParams['font.size'] = 20
# tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000)
# plot_only = 1000
# low_dim_embs = tsne.fit_transform(model.wv.vectors[:plot_only,:])
# labels = [model.wv.index2word[i] for i in range(plot_only)]
# plot_with_labels(low_dim_embs, labels)
# plt.show()

# newfile = open('C:\\Users\Administrator\Desktop\\tp_news_copy.txt', 'w', encoding='utf-8')
# with open('C:\\Users\Administrator\Desktop\\tp_news.txt', 'r', encoding='utf-8') as f:
#     while 1:
#         line = f.readline()
#         if line:
#             score = sentiment_alynasis.emotion_alynasis_2(line.split('@')[0])
#             if score == 0:
#                 newfile.writelines(line+'/n')
#         else:
#             break
# newfile.close()

'''评论价值入库'''
# connection = pymysql.connect(host='xxxxxx',
#                              user='xxxxxx',
#                              password='xxxxxx',
#                              db='xxxxxx',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
# try:
#     with connection.cursor() as cursor:
#         sql = "SELECT `comm_info`, `id` FROM tp_comment_info WHERE `comm_score_n` IS NULL"
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         sql2 = "UPDATE `tp_comment_info` SET `comm_score_n` = %s WHERE `id` = %s"
#         count = 0
#         for _r in result:
#             cursor.execute(sql2, (commentjudge.comment_judge(_r['comm_info']), _r['id']))
#             count += 1
#             if count % 1000 == 0:
#                 print(len(result)-count, '剩余')
#             # print(result2)
#             # print(tag_ranked, _r['id'])
#             # cursor.execute(sql2, (_r['id'], _r['net_name'], tag_ranked))
#             # cursor.execute(sql2, (_tag, _r['id']))
#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()
# finally:
#     print('处理完毕')
#     connection.close()





# def get_baiduresult(threadname, start=0):
#     connection = pymysql.connect(host='xxxxxx',
#                                  user='root',
#                                  password='root',
#                                  db='xxxxxx',
#                                  charset='utf8mb4',
#                                  cursorclass=pymysql.cursors.DictCursor)
#     try:
#         with connection.cursor() as cursor:
#             sql = "SELECT `title`, `id` FROM tp_news LIMIT %s, 10000  "
#             cursor.execute(sql, start)
#             result = cursor.fetchall()
#             sql2 = "UPDATE `tp_news` SET `postive_score` = %s WHERE `id` = %s"
#             count = 0
#             for _r in result:
#                 score = sentiment_alynasis.emotion_alynasis(_r['title'])
#                 # print(_r['title'], int(score))
#                 cursor.execute(sql2, (score, _r['id']))
#                 count += 1
#                 if count % 1000 == 0:
#                     print(threadname, ': ', count, '条已处理')
#                 # print(result2)
#                 # print(tag_ranked, _r['id'])
#                 # cursor.execute(sql2, (_r['id'], _r['net_name'], tag_ranked))
#                 # cursor.execute(sql2, (_tag, _r['id']))
#         # connection is not autocommit by default. So you must commit to save
#         # your changes.
#         connection.commit()
#     finally:
#         print('处理完毕')
#         connection.close()
#
#
# try:
#     start = 55000
#     for i in range(20):
#         _thread.start_new_thread(get_baiduresult, ('线程'+str(i), start))
#         print('线程启动正常....')
#         start += 5000
# except:
#     print('Error: 线程启动错误')
#
# while 1:
#    pass


# 舆论历史分数批量入库
# connection = pymysql.connect(host='xxxxxx',
#                              user='root',
#                              password='root',
#                              db='xxxxxx',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
#
#
#
# c_list, i_list = test.getcomdata()
# # i_list.append(0)
# try:
#     with connection.cursor() as cursor:
#         for i in i_list:
#             score_list, data_list = test.getscorelist(i, 'un')
#             for j in range(0, len(score_list)):
#                 sql = 'INSERT INTO `tp_opinion_score`(`pid`, `score_dev`, `createtime`) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE `score_dev` = %s'
#                 cursor.execute(sql, (i, score_list[j], data_list[j], score_list[j]))
#             print(i, '已完成')
#         connection.commit()
# finally:
#     print('处理完毕')
#     connection.close()

# 当天舆论评分入库
# connection = pymysql.connect(host='xxxxxx',
#                              user='root',
#                              password='root',
#                              db='xxxxxx',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
# comlist, idlist = test.getcomdata()
# idlist.append(0)
# thedatelist = [1530720000]
# try:
#     with connection.cursor() as cursor:
#         for thedate in thedatelist:
#             for i in idlist:
#                 score = test.getscorelist_perday(company_id=i, thedate=thedate)
#                 sql = 'INSERT INTO `tp_opinion_score`(`pid`, `score`, `createtime`) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE `score`=%s'
#                 cursor.execute(sql, (i, score, thedate, score))
#     connection.commit()
# finally:
#     print('处理完毕')
#     connection.close()

# 标签入库
# def tagbatchpush(date = str(datetime.date.today())):
#     id_max = 0
#     id_min = 0
#     threadlist = []
#     connection = pymysql.connect(host='xxxxxx',
#                                  user='root',
#                                  password='root',
#                                  db='xxxxxx',
#                                  charset='utf8mb4',
#                                  cursorclass=pymysql.cursors.DictCursor)
#     try:
#         with connection.cursor() as cursor:
#             # date = str(datetime.date.today())
#             datasql = 'SELECT MAX(`id`) AS maxid, MIN(`id`) as minid FROM `tp_comment_info` WHERE `update_date` = %s'
#             cursor.execute(datasql, date)
#             result = cursor.fetchall()
#             id_max = result[0]['maxid']
#             id_min = result[0]['minid']
#         connection.commit()
#     finally:
#         connection.close()
#
#     start = id_min
#     count = id_max - id_min
#     thread_num = 15
#     margin = int(count / thread_num) + 1
#     print('start, count, margin:', start, count, margin)
#     for i in range(thread_num):
#         threadlist.append(sentiment_alynasis.TagPushThread(i, 'thread-'+str(i), start, margin))
#         start += margin
#     for _t in threadlist:
#         _t.start()
#     for _t in threadlist:
#         _t.join()
#     return 1
#     # while 1:
#     #    pass
#
#
# sentiment_alynasis.tagbatchpush()

# print(test.getscorelist_perday(company_id=21, thedate=1530633600))

al = sentiment_alynasis.SentimentAlynasis()
al.tag_abstract()