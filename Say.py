import asyncio
from .. import loader, utils
import time
import random
import requests

@loader.tds
class ClanTagsMod(loader.Module):
	"""Say"""
	strings = {'name': 'Say'}

	async def saycmd(self, message):
		"""Используй .say <command>"""
		code = utils.get_args_raw(message)
		if not code:
			await message.edit(f"<b>No arg</b>")
			return
		try:
			await message.edit(f"{code}")
		except:
			await message.edit("<b>Error</b>")