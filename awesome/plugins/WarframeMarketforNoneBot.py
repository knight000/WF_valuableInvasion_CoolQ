import json
from reqLibs import requests
from nonebot import on_command, CommandSession


@on_command('warframe_market', aliases=('wm', '市场'), only_to_me=False)
async def warframe_market(session: CommandSession):
    wmurl = 'warframe.market/items/'
    with open("awesome\\plugins\\WF_Sale.json", "r", encoding="UTF-8") as f:
        SaleList = json.load(f)
    session.state['item'] = session.current_arg_text.strip()
    item = session.get('item', prompt='请输入你要查询的物品')
    url = ''
    message = ''
    for Sale in SaleList:
        if Sale['zh'] == item or Sale['en'] == item:
            url = 'https://' + wmurl + Sale['search']
            message = Sale['zh']+'的wm链接为:\n' + \
                wmurl+Sale['search']+'\n以下是出价最低的前五位买家：'
            ItemName = Sale['en']
            break
        else:
            continue
    if message == '':
        session.finish('未找到相关信息')
    else:
        try:
            req = await requests.get(url)
            data = await req.text
        except:
            session.finish('信息获取失败')
        orders = data[data.find('application-state')+19:]
        orders = orders[:orders.find('</script>')]
        orders = json.loads(orders)
        orders = dict(orders["payload"])["orders"]
        SellList = []
        for list1 in orders:
            SellDict = {}
            wmDict = dict(list1)
            if wmDict["visible"] == False:
                continue
            if wmDict["order_type"] != "sell":
                continue
            user = wmDict["user"]
            if user["status"] != "ingame":
                continue
            SellDict['name'] = user["ingame_name"]
            SellDict['platinum'] = wmDict["platinum"]
            SellList.append(SellDict)
        SellList = sorted(SellList, key=lambda x: x["platinum"])
        SellDict = {}
        i = 0
        for list2 in SellList:
            i += 1
            if i > 5:
                break
            else:
                SellDict = dict(list2)
                message += "\n出售者["+SellDict["name"]+"]"+str(SellDict["platinum"])+"白金"+"\n/w " + SellDict["name"] + \
                    " Hi! I want to buy: "+ItemName+" for " + \
                    str(SellDict["platinum"])+" platinum. (warframe.market)"
        session.finish(message)
