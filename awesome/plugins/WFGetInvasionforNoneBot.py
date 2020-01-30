import json
import ssl
import urllib.request
from nonebot import on_command, CommandSession


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


@on_command('Invasion', aliases=('invasion', '入侵'))
async def Invasion(session: CommandSession):
    url = "https://api.warframestat.us/pc/invasions"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(req)
    data = json.loads(res.read())
    message = "当前入侵为："
    for invasion in data:
        defender = dict(invasion['defenderReward'])
        defenderItem = defender['countedItems']
        defenderItem = dict(defenderItem[0])
        completion = str(int(invasion['completion']))
        node = invasion['node']
        if invasion['completion'] <= 0 or invasion['completion'] >= 100:
            continue
        if invasion['vsInfestation'] == True:
            message += "\n节点:"+node + \
                "奖励是:["+GetZh(defenderItem['type'])+"]当前进度:"+completion+"%"
        else:
            attacker = dict(invasion['attackerReward'])
            attackerItem = attacker['countedItems']
            attackerItem = dict(attackerItem[0])
            message += "\n节点:"+node+"奖励是:[" + \
                GetZh(defenderItem['type'])+"]或[" + \
                GetZh(attackerItem['type'])+"]当前进度:"+completion+"%"
    await session.send(message)
    session.finish()
