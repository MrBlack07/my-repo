import asyncio
from .. import loader, utils
from telethon import events
import time
import random
import requests

@loader.tds
class ClanTagsMod(loader.Module):
	"""SpamChecker"""
	strings = {'name': 'SpamChecker'}

	async def spamcheckcmd(self, message):
		chat = '@SpamBot'
		await message.edit("Gettting info...")
		async with message.client.conversation(chat) as check:
			try:
				response = check.wait_event(events.NewMessage(incoming=True, from_users=178220800))
				bot_send_message = await message.client.send_message(chat, "/start")
				bot_response = response = await response
				if "Good news" or "Ваш аккаунт свободен" in response.text:
					await message.edit("Your account is unlocked")
				else:
					await message.edit("Your account is spam-blocked")
			except Exception as f:
				await message.edit('<b>Error</b> \n'+ f)
				return
			await bot_send_message.delete()
			await bot_response.delete()