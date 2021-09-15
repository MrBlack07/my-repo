import asyncio
from asyncio import sleep, gather
from .. import loader, utils
import time
import random

@loader.tds
class ClanTagsMod(loader.Module):
	"""RTimer"""
	strings = {'name': 'RTimer'}

	async def timercmd(self, message):
		"""Используй .timer <reply comment> <time(in sec)>"""
		args = utils.get_args_raw(message)
		reply = await message.get_reply_message()
		time = int(args.split(' ', 2)[0])
		if not args:
			await message.edit("No Arg")
			return
		if not reply:
			await message.edit("No Reply")
		zxc = reply.text
		try:
			await message.edit(f"✅Timer Enable on {time} sec.✅\n✅With comment {zxc}✅")
			await sleep(time)
			await message.client.send_message(message.to_id,f"📛Timer:The time is over📛\n📛Comment: {zxc}📛\n📛Time: {time}📛")
		except Exception as f:
			await message.edit(f"<b>Error:\n{f}</b>")