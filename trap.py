# requires: pydub
from pydub import AudioSegment
from .. import loader, utils
from telethon import types
import io
import requests

biography = requests.get("https://siasky.net/fAKw0t5Wnrly_aVkGyYvAuIXokINZzFEU2u_QhECqqZ2ow").content

biogra = requests.get("https://siasky.net/PAA5aVEM3UL20i-rNnJUO2XxZKzzWzCWnnw-2P2zWepyAg").content

biogram = requests.get("https://siasky.net/fAPHfVfYNsbDwLUbmpyNuIwA04YPQC1GJdYPG6aDhuo6-Q").content


class TrapMod(loader.Module):
    """trap"""
    strings = {'name': 'trap_to_voice'}
    
    
    async def trapcmd(self, message):
        """.Trap <reply to voice>
        """
        reply = await message.get_reply_message()
        if not reply or not reply.file or not reply.file.mime_type.startswith("audio"):
            return await message.edit("<b>Reply to audio.</b>")
        await message.edit("<b>сичас будет качать))</b>")
        voice = io.BytesIO()
        await reply.download_media(voice)
        voice.seek(0)
        voice = AudioSegment.from_file(voice)
        biogr = io.BytesIO(biography)
        vol = utils.get_args_raw(message)
        if vol and  vol.isdigit():
            vol = 100-int(vol)
        else:
            vol = 20
        biogr.seek(0)
        biogr = AudioSegment.from_file(biogr)[0:len(voice)]-vol
        out = biogr.overlay(voice, position=0)
        output = io.BytesIO()
        output.name="biography.ogg"
        out.export(output, format="ogg", bitrate="64k", codec="libopus")
        output.seek(0)
        await message.client.send_file(message.to_id, output, reply_to=reply.id, voice_note=True, duration=len(out)/1000)
        await message.delete()
        
    async def trcmd(self, message):
        """.Tr <reply to voice>
        """
        reply = await message.get_reply_message()
        if not reply or not reply.file or not reply.file.mime_type.startswith("audio"):
            return await message.edit("<b>Reply to audio.</b>")
        await message.edit("<b>сичас будет качать))...</b>")
        voice = io.BytesIO()
        await reply.download_media(voice)
        voice.seek(0)
        voice = AudioSegment.from_file(voice)
        biogr = io.BytesIO(biogra)
        vol = utils.get_args_raw(message)
        if vol and  vol.isdigit():
            vol = 100-int(vol)
        else:
            vol = 20
        biogr.seek(0)
        biogr = AudioSegment.from_file(biogr)[0:len(voice)]-vol
        out = biogr.overlay(voice, position=0)
        output = io.BytesIO()
        output.name="biography.ogg"
        out.export(output, format="ogg", bitrate="64k", codec="libopus")
        output.seek(0)
        await message.client.send_file(message.to_id, output, reply_to=reply.id, voice_note=True, duration=len(out)/1000)
        await message.delete()
        
    async def ptcmd(self, message):
        """.pt <reply to voice>
        """
        reply = await message.get_reply_message()
        if not reply or not reply.file or not reply.file.mime_type.startswith("audio"):
            return await message.edit("<b>Reply to audio.</b>")
        await message.edit("<b>сичас будет качать))</b>")
        voice = io.BytesIO()
        await reply.download_media(voice)
        voice.seek(0)
        voice = AudioSegment.from_file(voice)
        biogr = io.BytesIO(biogram)
        vol = utils.get_args_raw(message)
        if vol and  vol.isdigit():
            vol = 100-int(vol)
        else:
            vol = 20
        biogr.seek(0)
        biogr = AudioSegment.from_file(biogr)[0:len(voice)]-vol
        out = biogr.overlay(voice, position=0)
        output = io.BytesIO()
        output.name="biography.ogg"
        out.export(output, format="ogg", bitrate="64k", codec="libopus")
        output.seek(0)
        await message.client.send_file(message.to_id, output, reply_to=reply.id, voice_note=True, duration=len(out)/1000)
        await message.delete()