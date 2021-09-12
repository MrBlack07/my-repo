import asyncio
from .. import loader, utils
import time
import random
import requests
import COVID19Py

@loader.tds
class ClanTagsMod(loader.Module):
	"""CovidStat"""
	strings = {'name': 'CovidStat'}

	async def covidcmd(self, message):
		"""Используй .covid <код страны>"""
		code = utils.get_args_raw(message)
		covid19 = COVID19Py.COVID19()
		if not code:
			location = covid19.getLatest()
			await message.edit(f"<u>🛏Данные по всему миру:</u>\n<b>😷Заболевших: </b>{location['confirmed']:,}\n<b>💀Сметрей: </b>{location['deaths']:,}")
			return
		await message.edit("Loading...")
		try:
			covid19 = COVID19Py.COVID19()
			location = covid19.getLocationByCountryCode(code)
			date = location[0]['last_updated'].split("T")
			time = date[1].split(".")
			final_message = f"<u>🛏Данные по стране {code}:</u>\n📊Население: {location[0]['country_population']:,}\n" \
							f"⌛️Последнее обновление: {date[0]} {time[0]}\n🦠Последние данные:\n<b>" \
							f"😷Заболевших: </b>{location[0]['latest']['confirmed']:,}\n<b>💀Сметрей: </b>" \
							f"{location[0]['latest']['deaths']:,}"
			await message.edit(final_message)
		except:
			await message.edit("<b>Invalid country code.Perhaps this code is not in the database</b>")
