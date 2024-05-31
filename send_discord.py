from discord import Webhook
import aiohttp
import asyncio
import sys

message = sys.argv[1]
uname = sys.argv[2]

async def foo(msg,uname):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url('https://discord.com/api/webhooks/1240620878597984337/iYfPWx7X-s4u-dFBNVvftOlwXYU0Jrugtu839wtYwuCc2hjpDGAHUMe161tXzoCnjMLP', session=session)
        await webhook.send(msg, username=uname,silent=True)

loop=asyncio.get_event_loop()
loop.run_until_complete(foo(msg=message,uname=uname))