import json
import ssl
import urllib.request
from nonebot import on_command, CommandSession


async def GetDate():
    url = "https://api.warframestat.us/pc/voidTrader"  # 直接获取虚空商人的数据
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


@on_command('voidTrader', aliases=('voidtrader', '虚空商人', 'baro'), only_to_me=False)
async def voidTrader(session: CommandSession):
    data = json.loads(await GetDate())
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
