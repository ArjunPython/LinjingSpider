from emotionAlynasis import sentiment_alynasis, test

alynasisor = sentiment_alynasis.SentimentAlynasis()
def alynasis(sentence=''):
    '''评论正负面判定
    @sentence: str, 代分析的文本内容
    @return: int, 正负面评分，1正面，0负面'''
    print("开始分析...")
    # if request.method == 'POST':
    # score = sentiment_alynasis.emotion_alynasis_2(sentence)
    level = alynasisor.emotion_alynasis_2(sentence)
    # tag_list = sentiment_alynasis.tag_transform(sentence)
    return level


def news_alynasis(sentence=''):
    '''新闻正负面判定
    @sentence: str, 代分析的文本内容
    @return: int, 正负面评分，1正面，0负面'''
    # if request.method == 'POST':
    level = alynasisor.news_alynasis(sentence)
    return level
    # else:
    #     error = '请使用post方法传参'
        # return jsonify({'result': error})


def getgraphdata(cpid, name):
    scorelist, datelist = test.getscorelist_mysql(company_id=cpid, company_name=name)
    return scorelist, datelist


def personeval(sentence):
    '''人员简历评价接口返回值 0:开发，1:金融, 2:管理'''
    if str(sentence).__contains__('开发'):
        rst = 0
    elif str(sentence).__contains__('金融'):
        rst = 1
    else:
        rst = 2
    return rst


def get_comdata():
    comlist, idlist = test.getcomdata()
    return comlist
    # else:
    #     error = '请使用post方法传参'
        # return jsonify({'result': error})


def pushtag():
    '''当日评论标签入库
    @returen: 1，成功'''
    alynasisor.tagbatchpush()
    result = alynasisor.tag_abstract()
    return result

def opscorepush():
    '''当日舆论评分入库，无参数
    @return: 1，成功； 0，失败'''
    result = alynasisor.opscoreperday()
    if result:
        return 1
    else:
        return 0
