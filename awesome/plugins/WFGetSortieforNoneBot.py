import json
import ssl
import urllib.request
from nonebot import on_command, CommandSession


async def GetDate():
    url = "https://api.warframestat.us/pc/sortie"  # 直接获取突击的数据
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
    return wfDict['en']


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


@on_command('Sortie', aliases=('sortie', '突击'), only_to_me=False)
async def Sortie(session: CommandSession):
    data = json.loads(await GetDate())
    message = "当前突击为:"
    for sortie in data['variants']:
        message += "\n["+await GetZh(sortie['missionType'])+"]"+await GetNodeZh(sortie['node'])+"\n"+await GetModifierZh(sortie['modifier'])
    message += "\n派系:"+data['faction']+"\n受害者:" + \
        data['boss']+"\n剩余时间:"+data['eta']
    await session.send(message)
    session.finish()
