# coding: UTF-8

import tweepy
import re
import json
import datetime

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
FILE_NAME = "record.json"
TODAY = datetime.date.today()
KARASU_ID = 846351355744694272
SEARCH_PATTERN = re.compile(r"からす([0-9]+)円")


def read_records():
    with open(FILE_NAME) as f:
        return json.load(f)


def save_record(dic):
    with open(FILE_NAME, "w") as f:
        json.dump(dic, f)


if __name__ == "__main__":
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)

    record = read_records()
    todayRecord = {}
    friendIds = api.friends_ids(KARASU_ID)
    creditors = []
    debtSum = 0
    for friendId in friendIds:
        friend = api.get_user(friendId)
        friendName = friend._json["name"]
        match = SEARCH_PATTERN.search(friendName)
        if match is not None:
            valueStr = match.group(1)
            creditors.append({
                "id" : friendId,
                "debt" : int(valueStr)
            })
            debtSum += int(valueStr)
            print(friendName + "!!!" + valueStr)
        else:
            print(friendName + "!!!0")

    todayRecord["creditors"] = creditors
    todayRecord["debt"] = debtSum
    print(todayRecord)

    yesterday_debt = record[(TODAY + datetime.timedelta(days=-1)).isoformat()]["debt"]
    delta = debtSum - yesterday_debt
    print("now debt:" + str(debtSum))
    print("delta:" + str(delta))
    api.update_status("現時点でのからすの借金は" + str(debtSum) + "円です。前回との差額は" + str(delta) + "円です。")

    record[TODAY.isoformat()] = todayRecord
    save_record(record)
