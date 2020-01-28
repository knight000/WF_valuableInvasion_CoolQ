from nonebot.default_config import *

SUPERUSERS = {} #这里填写你自己的QQ号
# COMMAND_START = {'/', '!', '／', '！'} #这里是默认选项
COMMAND_START = {'#'} #设置命令以#开头
COMMAND_SEP = {' '} #命令以空格分割
HOST = '0.0.0.0'
PORT = 8080 #这里是端口，这里改了http-api那里也要改