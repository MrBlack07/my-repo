from .. import loader
from telethon import events
from time import time
from .. import utils
import speech_recognition as sr
from pydub import AudioSegment
import asyncio

@loader.tds
class VoiceToTextMod(loader.Module):
    strings = {"name": "Voice To Text"}

    async def recognize(self, event):
        msg = await event.reply('<code>🗣 Проверяю наличие голосового сообщения...</code>')
        try:
            filename = "/tmp/" + str(time()).replace('.', '')
            await event.download_media(file=filename + '.ogg')
            song = AudioSegment.from_ogg(filename + '.ogg')
            song.export(filename + '.wav', format="wav")
            await msg.edit('<code>🗣 Распознаю голосовое сообщение...</code>')
            r = sr.Recognizer()
            with sr.AudioFile(filename + '.wav') as source:
                audio_data = r.record(source)
                text = r.recognize_google(audio_data, language='ru-RU')
                await msg.edit('<b>👆 Текст этого войса:</b>\n<pre>' + text + '</pre>')
        except:
            await msg.delete()

    @loader.owner
    async def voicycmd(self, message):
        reply = await message.get_reply_message()
        if not reply.media or not reply.media.document.attributes[0].voice:
            await message.edit('🗣 <b>Войс не найден</b>')
            await asyncio.sleep(2)
            await message.delete()

        await self.recognize(reply)

    @loader.owner
    async def watcher(self, event):
        if not event.media or not event.media.document.attributes[0].voice:
            return

        await self.recognize(event)
