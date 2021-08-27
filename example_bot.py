import json
import re

from invisionChatbox.bot import Bot
from invisionChatbox.message import Message
from invisionChatbox.utils.validators import RegexValidator

with open('conf.json', 'r') as f:
    conf = json.load(f)

bot = Bot(**conf)


@bot.command(['hello', 'hi'],)
def hello(message: Message, data: dict):
    print(message.content)


@bot.command(is_command=False, validators=[RegexValidator(re.compile(r'welcome.+hello'))])
def welcome(message: Message, data: dict):
    print('welcome')
    bot.send_message('dasdasd')


bot.run()

print('sd')
