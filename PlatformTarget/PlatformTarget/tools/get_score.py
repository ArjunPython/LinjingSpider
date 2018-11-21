
# from emotionAlynasis import mainparser
import requests
import json


def get_score(comm_info):
    try:
        # 评论正负面打分 comm_score
        comm_score_url = "http://172.16.20.228:5011/NPalynasis"
        comm_score_n_url = "http://172.16.20.228:5011/YNalynasis"
        data = {"sentence": comm_info}
        score_data = json.loads(requests.post(comm_score_url, data=data).content.decode())["result"][1]
        # 评论价值分析 comm_score_n
        value = json.loads(requests.post(comm_score_n_url, data=data).content.decode())["result"][1]
        return score_data, value
    except Exception as e:
        print(e)
        print("fail")


if __name__ == '__main__':
    n = get_score("分散理性投资，不要捡了芝麻丢了大象")
    print(n)