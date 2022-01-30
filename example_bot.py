import json
import re

from invisionChatbox.basicclient import BasicClient
from invisionChatbox.context import Context
from invisionChatbox.utils.validators import RegexValidator
from invisionChatbox.utils.decorators import run_in_thread

bot = BasicClient(**json.load(open('conf.json')))


# print message when user use command hello or hi # /hello and /hi if activator is `/`
@bot.command(['hello', 'hi'])
def hello(ctx: Context, data: dict):
    print(ctx.content)


# Reply Thanks, when someone says welcome
@bot.command(is_command=False, validators=[RegexValidator(re.compile(r'welcome', re.IGNORECASE))])
def welcome(ctx: Context, data: dict):
    ctx.reply('Thanks')


# run when someone uses test command, /test if activator is `/`
# using run in threads command sometimes can run twice
@bot.command()
@run_in_thread
def test(ctx: Context, data: dict):
    print(ctx.content)
    print(ctx.clean_content)
    ctx.reply("test passed")
    ctx.reply("test passed", dm=True)


bot.run()
