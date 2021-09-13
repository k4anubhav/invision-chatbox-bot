import json
import re

from invisionChatbox.bot import Bot
from invisionChatbox.context import Context
from invisionChatbox.utils.validators import RegexValidator

with open('conf.json', 'r') as f:
    conf = json.load(f)

bot = Bot(**conf)


# print message when user use command hello or hi # /hello and /hi if activator is `/`
@bot.command(['hello', 'hi'])
def hello(message: Context, data: dict):
    print(message.content)


# Reply Thanks, when someone says welcome
@bot.command(is_command=False, validators=[RegexValidator(re.compile(r'welcome', re.IGNORECASE))])
def welcome(message: Context, data: dict):
    bot.send_message('Thanks')


@bot.command()
def test(message: Context, data: dict):
    print(message.content)
    print(message.clean_content)
    message.reply("test passed")
    message.reply("test passed", dm=True)


bot.run()
