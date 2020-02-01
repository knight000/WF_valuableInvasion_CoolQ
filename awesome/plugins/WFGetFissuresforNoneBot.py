import json
import ssl
import urllib.request
from nonebot import on_command, CommandSession


async def GetDate():
    url = "https://api.warframestat.us/pc/fissures"  # 直接获取裂隙的数据
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


@on_command('Fissures', aliases=('fissures', '裂隙', '裂缝', '虚空裂隙'), only_to_me=False)
async def Fissures(session: CommandSession):
    data = json.loads(await GetDate())
    message = "当前裂隙为："
    for fissure in data:
        if fissure['expired'] == True:
            # 过滤掉过期裂隙
            continue
        message += "\n["+await GetZh(fissure['tier'])+"]"+await GetZh(fissure['missionType']) + \
            "\n"+await GetNodeZh(fissure['node'])+"剩余时间:"+fissure['eta']
    await session.send(message)
    session.finish()
