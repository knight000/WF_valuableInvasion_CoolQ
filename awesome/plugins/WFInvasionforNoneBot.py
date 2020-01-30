import json
import ssl
import urllib.request
import nonebot
# 这个是给机器人用的版本，用nonebot输出


RepeatID = set()  # 这里是记录已提醒的集合
bot = nonebot.get_bot()
@nonebot.scheduler.scheduled_job('interval', minutes=5)
async def _():
    f = open("awesome\\plugins\\data.list", "r")
    Gotlist = f.read()  # 获取已拥有的列表
    f.close()
    Gotlist = Gotlist.splitlines()
    ReturnData = ""
    url = "https://api.warframestat.us/pc/invasions"  # 直接获取入侵的数据
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(req)
    invasions = json.loads(res.read())
    for dict1 in invasions:
        #dict1 = dict(a)
        if dict1['id'] in RepeatID:
            # 去重
            continue
        else:
            RepeatID.add(dict1['id'])
        if dict1['completion'] <= 0 or dict1['completion'] >= 100:
            # RepeatID.remove(dict1['id'])  # 去掉已过期的入侵，但是好像没必要就注释掉了
            continue
        if dict1['vsInfestation'] == True:
            # 过滤掉I系相关的入侵，因为没有部件
            continue
        attacker = dict(dict1['attackerReward'])
        attackerItemDict = attacker['countedItems']
        attackerItemDict = dict(attackerItemDict[0])
        defender = dict(dict1['defenderReward'])
        defenderItemDict = defender['countedItems']
        defenderItemDict = dict(defenderItemDict[0])
        # 这里是汉化
        attackerItem = attackerItemDict['type']
        defenderItem = defenderItemDict['type']
        with open("awesome\\plugins\\WF_Dict.json", "r", encoding="UTF-8") as f:
            # 翻译文件来自https://github.com/Richasy/WFA_Lexicon
            wfDictList = json.load(f)
        for list1 in wfDictList:
            wfDict = dict(list1)
            if wfDict['en'] == attackerItem:
                attackerItem = wfDict['zh']
                break
            else:
                continue
        for list2 in wfDictList:
            wfDict = dict(list2)
            if wfDict['en'] == defenderItem:
                defenderItem = wfDict['zh']
                break
            else:
                continue
        # 这里是已拥有的就不提示
        if attackerItem in Gotlist and defenderItem in Gotlist:
            continue
        # if dict1['rewardTypes'] in highvalue:
        if attackerItemDict['count'] == 1 or defenderItemDict['count'] == 1:
            # 用奖励的数量来判断是不是武器部件
            node = dict1['node']
            completion = str(int(dict1['completion']))
            ReturnData += "\n节点:"+node+"，奖励是:[" + \
                attackerItem+']和[' + \
                defenderItem+"]当前进度："+completion+"%"
            if attackerItem in Gotlist:
                ReturnData += "\n其中["+attackerItem+"]已拥有"
            if defenderItem in Gotlist:
                ReturnData += "\n其中["+defenderItem+"]已拥有"
    f = open("QQ.txt", "r")
    QQ = int(f.readline())
    f.close
    if ReturnData != "":
        ReturnData = "发现高价值入侵:"+ReturnData
        await bot.send_private_msg(user_id=QQ, message=ReturnData)
