import json
import re

from invisionChatbox.bot import Bot
from invisionChatbox.context import Context
from invisionChatbox.utils.validators import RegexValidator

with open('conf.json', 'r') as f:
    conf = json.load(f)

bot = Bot(**conf)


@bot.command(['hello', 'hi'],)
def hello(message: Context, data: dict):
    print(message.content)


@bot.command(is_command=False, validators=[RegexValidator(re.compile(r'welcome.+hello'))])
def welcome(message: Context, data: dict):
    print('welcome')
    bot.send_message('dasdasd')


@bot.command()
def test(message: Context, data: dict):
    print(message.content)
    print(message.clean_content)
    message.reply("test passed")
    message.reply("test passed", dm=True)


# bot.send_direct_message(member_id=36, message="test message")
bot.run()

print('sd')
