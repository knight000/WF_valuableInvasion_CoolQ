import json
import ssl
import urllib.request
from nonebot import on_command, CommandSession


async def GetDate():
    url = "https://api.warframestat.us/pc/invasions"  # 直接获取入侵的数据
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(req)
    return res.read()


async def GetZh(en):
    with open("awesome\\plugins\\WF_Dict.json", "r", encoding="UTF-8") as f:
        # 翻译文件来自https://github.com/Richasy/WFA_Lexicon
        wfDictList = json.load(f)
    for wfDict in wfDictList:
        if en == wfDict['en']:
            return wfDict['zh']
    return en


async def GetNodeZh(node):
    Planet = node[node.find('(')+1:node.find(')')]
    node = node[:node.find('(')]
    Planet = await GetZh(Planet)
    node += '('+Planet+')'
    return node


@on_command('Invasion', aliases=('invasion', '入侵'), only_to_me=False)
async def Invasion(session: CommandSession):
    data = json.loads(await GetDate())
    message = "当前入侵为："
    with open("awesome\\plugins\\WF_Invasion.json", "r", encoding="UTF-8") as f:
        # 翻译文件来自https://github.com/Richasy/WFA_Lexicon
        wfDictList = json.load(f)
    for invasion in data:
        defender = dict(invasion['defenderReward'])
        defenderItem = defender['countedItems']
        defenderItem = dict(defenderItem[0])
        completion = str(int(invasion['completion']))
        node = await GetNodeZh(invasion['node'])
        for list1 in wfDictList:
            wfDict = dict(list1)
            if wfDict['en'] == defenderItem['type']:
                ZhdefenderItem = wfDict['zh']
                break
            else:
                continue
        if invasion['completion'] <= 0 or invasion['completion'] >= 100:
            continue
        if invasion['vsInfestation'] == True:
            message += "\n"+node + \
                "奖励是:["+ZhdefenderItem+"]\n当前进度:"+completion+"%"
        else:
            attacker = dict(invasion['attackerReward'])
            attackerItem = attacker['countedItems']
            attackerItem = dict(attackerItem[0])
            for list1 in wfDictList:
                wfDict = dict(list1)
                if wfDict['en'] == attackerItem['type']:
                    ZhattackerItem = wfDict['zh']
                    break
                else:
                    continue
            message += "\n"+node+"奖励是:[" + \
                ZhdefenderItem+"]或[" + \
                ZhattackerItem+"]\n当前进度:"+completion+"%"
    await session.send(message)
    session.finish()
