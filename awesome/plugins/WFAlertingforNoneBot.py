import json
import requests
from nonebot import on_command, CommandSession


async def GetDate(DataType):
    url = "https://api.warframestat.us/pc/"+DataType
    data = requests.get(url, verify=False)
    return data.text


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


async def GetModifierZh(en):
    with open("awesome\\plugins\\WF_Modifier.json", "r", encoding="UTF-8") as f:
        # 翻译文件来自https://github.com/Richasy/WFA_Lexicon
        wfDictList = json.load(f)
    for wfDict in wfDictList:
        if en == wfDict['en']:
            return wfDict['zh']
    return en


@on_command('voidTrader', aliases=('voidtrader', '虚空商人', 'baro'), only_to_me=False)
async def voidTrader(session: CommandSession):
    data = json.loads(await GetDate('voidTrader'))
    if data['active'] == False:
        message = "Baro Ki'Teer在路上\n到达剩余时间:"+data['startString']
    else:
        message = "Baro Ki'Teer已到达"+await GetNodeZh(data['location'])
        inventoryList = data['inventory']
        for inventory in inventoryList:
            message += "\n"+await GetZh(inventory['item'])+"\n价格:"
            if inventory['ducats'] != 0:
                message += "["+str(inventory['ducats'])+"]杜卡德金币"
            if inventory['credits'] != 0:
                message += "["+str(inventory['credits'])+"]现金"
    await session.send(message)
    session.finish()


@on_command('Sortie', aliases=('sortie', '突击'), only_to_me=False)
async def Sortie(session: CommandSession):
    data = json.loads(await GetDate('sortie'))
    message = "当前突击为:"
    for sortie in data['variants']:
        message += "\n["+await GetZh(sortie['missionType'])+"]"+await GetNodeZh(sortie['node'])+"\n"+await GetModifierZh(sortie['modifier'])
    message += "\n派系:"+data['faction']+"\n受害者:" + \
        data['boss']+"\n剩余时间:"+data['eta']
    await session.send(message)
    session.finish()


@on_command('Invasion', aliases=('invasion', '入侵'), only_to_me=False)
async def Invasion(session: CommandSession):
    data = json.loads(await GetDate('invasions'))
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


@on_command('Fissures', aliases=('fissures', '裂隙', '裂缝', '虚空裂隙'), only_to_me=False)
async def Fissures(session: CommandSession):
    data = json.loads(await GetDate('fissures'))
    message = "当前裂隙为："
    for fissure in data:
        if fissure['expired'] == True:
            # 过滤掉过期裂隙
            continue
        message += "\n["+await GetZh(fissure['tier'])+"]"+await GetZh(fissure['missionType']) + \
            "\n"+await GetNodeZh(fissure['node'])+"剩余时间:"+fissure['eta']
    await session.send(message)
    session.finish()


@on_command('Arbitration', aliases=('arbitration', '仲裁'), only_to_me=False)
async def Arbitration(session: CommandSession):
    data = json.loads(await GetDate('arbitration'))
    message = "当前仲裁为:\n"+data['tile']+"("+await GetZh(data['planet'])+")\n"+data['enemy']+await GetZh(data['type'])
    await session.send(message)
    session.finish()


@on_command('RivenData', aliases=('riven', '倾向'), only_to_me=False)
async def RivenData(session: CommandSession):
    with open("awesome\\plugins\\WF_Riven.json", "r", encoding="UTF-8") as f:
        RivenList = json.load(f)
    session.state['item'] = session.current_arg_text.strip()
    item = session.get('item', prompt='请输入你要查询的物品')
    item = await GetZh(item)
    success = False
    for RivenDict in RivenList:
        RivenDict = dict(RivenDict)
        if RivenDict["name"] == item:
            success = True
            message = "已查询到["+item+"]的紫卡倾向:\n" + \
                str(RivenDict["level"])+"星倾向"+str(RivenDict["ratio"])
            break
        else:
            continue
    if success:
        await session.send(message)
    else:
        await session.send('未查询到相关信息')
    session.finish()
