import json
import ssl
import sys
import time
import urllib.request
import nonebot
# 这个是给机器人用的版本，用nonebot输出


def GetData():
    # 从网站上获取数据，获取到的是字典
    url = "https://api.warframestat.us/pc/invasions"  # 直接获取入侵的数据
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(req)
    data = json.loads(res.read())
    return data


def GetZh(name):
    # 用于翻译
    str(name)
    with open("awesome\\plugins\\WF_Dict.json", "r", encoding="UTF-8") as f:
        # 翻译文件来自https://github.com/Richasy/WFA_Lexicon
        wfDictList = json.load(f)
    for list1 in wfDictList:
        wfDict = dict(list1)
        if wfDict['en'] == name:
            return wfDict['zh']
        else:
            continue


def CheckRepeat(id):
    if id in RepeatID:
        return True
    else:
        RepeatID.add(id)
        return False


def UseInvasionData(invasions):
    # 暂时只写了入侵的功能
    # invasions = data["invasions"] #以后可能要用，就留着了
    Gotlist = ReadList()  # 获取已拥有的列表
    ReturnData = ""
    for a in invasions:
        dict1 = dict(a)
        if CheckRepeat(dict1['id']):
            # 去重
            continue
        if dict1['completion'] <= 0 or dict1['completion'] >= 100:
            # RepeatID.remove(dict1['id'])  # 去掉已过期的入侵，但是好像没必要就注释掉了
            continue
        if dict1['vsInfestation'] == True:
            # 过滤掉I系相关的入侵，因为没有部件
            continue
        attacker = dict(dict1['attackerReward'])
        attackerItem = attacker['countedItems']
        attackerItem = dict(attackerItem[0])
        defender = dict(dict1['defenderReward'])
        defenderItem = defender['countedItems']
        defenderItem = dict(defenderItem[0])
        # 这里是已拥有的就不提示
        if GetZh(attackerItem['type']) in Gotlist and GetZh(defenderItem['type']) in Gotlist:
            continue
        # if dict1['rewardTypes'] in highvalue:
        if attackerItem['count'] == 1 or defenderItem['count'] == 1:
            # 用奖励的数量来判断是不是武器部件
            node = dict1['node']
            completion = str(int(dict1['completion']))
            ReturnData = ReturnData+"节点:"+node+"，奖励是:[" + \
                GetZh(attackerItem['type'])+']和[' + \
                GetZh(defenderItem['type'])+"]当前进度："+completion+"%\n"
            if GetZh(attackerItem['type']) in Gotlist:
                ReturnData = ReturnData + \
                    "其中["+GetZh(attackerItem['type'])+"]已拥有\n"
            if GetZh(defenderItem['type']) in Gotlist:
                ReturnData = ReturnData + \
                    "其中["+GetZh(defenderItem['type'])+"]已拥有\n"
    return ReturnData


def ReadList():
    data = []
    f = open("awesome\\plugins\\data.list", "r")
    data = f.read()
    data = data.splitlines()
    f.close()
    return data


RepeatID = set()  # 这里是记录已提醒的集合
bot = nonebot.get_bot()
@nonebot.scheduler.scheduled_job('interval', minutes=5)
async def _():
    check = UseInvasionData(GetData())
    f = open("QQ.txt", "r")
    QQ = int(f.readline())
    f.close
    if check != "":
        check = "发现高价值入侵：\n"+check
        print(check)
        await bot.send_private_msg(user_id=QQ, message=check)
