import json
import ssl
import urllib.request
from nonebot import on_command, CommandSession


async def GetDate():
    url = "https://api.warframestat.us/pc/arbitration"  # 直接获取仲裁的数据
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


@on_command('Arbitration', aliases=('arbitration', '仲裁'), only_to_me=False)
async def Arbitration(session: CommandSession):
    data = json.loads(await GetDate())
    message = "当前仲裁为:\n"+data['tile']+"("+await GetZh(data['planet'])+")\n"+data['enemy']+await GetZh(data['type'])
    await session.send(message)
    session.finish()