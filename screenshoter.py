from .. import loader, utils  # pylint: disable=relative-beyond-top-level 
import logging 
from requests import post 
import io 
import asyncio
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon import events
 
logger = logging.getLogger(__name__) 
 
@loader.tds 
class filescreenMod(loader.Module): 
    """Скриншотер""" 
    strings = { 
    "name": "Скриншотер" 
    } 

    async def client_ready(self, client, db): 
        self.client = client 
    
    @loader.sudo 
    async def filescmd(self, message): 
        await message.edit("<b>Получаю данные...</b>") 
        reply = await message.get_reply_message() 
        if not reply: 
            await message.edit("<b>Реплаем на файл!</b>") 
            return 
        media = reply.media 
        if not media: 
            file = io.BytesIO(bytes(reply.raw_text, "utf-8")) 
            file.name = "txt.txt" 
        else: 
            file = io.BytesIO(await self.client.download_file(media)) 
            file.name = reply.file.name if reply.file.name else  reply.file.id+reply.file.ext 
        try: 
            x0at = post('https://x0.at', files={'file': file}) 
        except ConnectionError as e: 
            await message.edit(ste(e)) 
            return 
        url = x0at.text 
        print(url)
        chat = '@URL2IMGBot'
        await message.edit(' <code>p r o c e s s i n g</code>')
        await message.edit(' <code>p r o c e s s i n g . . .</code>')
        async with message.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(events.NewMessage(incoming=True, from_users=310975959))
                await message.client.send_message(chat, str(url))
                response = await response
                await asyncio.sleep(7)
                result = await message.client.get_messages(chat, limit=1)
            except YouBlockedUserError:
                await message.reply('<code>Убери из ЧС этого бота:</code> @Klouns2Bot')
                return
        await message.delete()
        for x in result:
            if x.media:
                await message.client.send_file(message.to_id, x.media)
                
    @loader.sudo 
    async def linkscmd(self, message): 
        await message.edit("<b>Получаю данные...</b>") 
        reply = await message.get_reply_message() 
        if not reply: 
            await message.edit("<b>Реплаем на файл!</b>") 
            return          
        chat = '@URL2IMGBot'
        await message.edit(' <code>p r o c e s s i n g</code>')
        await message.edit(' <code>p r o c e s s i n g . . .</code>')
        async with message.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(events.NewMessage(incoming=True, from_users=310975959))
                await message.client.send_message(chat, reply)
                response = await response
                await asyncio.sleep(7)
                result = await message.client.get_messages(chat, limit=1)
            except YouBlockedUserError:
                await message.reply('<code>Убери из ЧС этого бота:</code> @Klouns2Bot')
                return
        await message.delete()
        for x in result:
            if x.media:
                await message.client.send_file(message.to_id, x.media)
       