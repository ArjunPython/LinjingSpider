nlp处理包

环境配置：
python3.5以上
tensorflow 1.7
gensim 3.4.0
numpy 1.14.0
jieba 0.39
pymysql 0.8.0

接口转方法在mainparser包中：
```评论正负面打分，单个处理
@app.route('/alynasis', methods=['GET', 'POST'])
alyna

公司表获取，无参数
@app.route('/comdata', methods=['GET', 'POST'])
get_comdata()
sis(sentence="")
@sentence 待分析文本

新闻正负面打分，单个处理
@app.route('/newsalynasis', methods=['GET', 'POST'])
news_alynasis()
alynasis(sentence="")
@sentence 待分析文本

历史舆论分获取，无参数
@app.route('/graph', methods=['GET', 'POST'])
getgraphdata()

人员评价
@app.route('/personeval', methods=['GET', 'POST'])
personeval()
评论打标签，批处理，无参数
@app.route('/tagpush', methods=['GET', 'POST'])
pushtag()

当天舆论汇总分数入库，批处理，无参数，所有评论爬完之后调一次,返回值为1则成功入库
opscorepush()