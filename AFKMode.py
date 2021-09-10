from .. import loader, utils
import datetime, time
from telethon import functions, types

@loader.tds
class AFKModeMod(loader.Module):
    """
    AFKMode :
        Разработчик seen.
    Команды :
    """

    strings = {"name": "AFKMode",
               "afk_status": "<b>Информация о ваших настройках AFK</b>\n\n"
                             "<b>AFK режим:</b> {}\n\n<b>PM режим:</b> {}",
               "afk": "<b>Я сейчас AFK (время моего отсутсвия: <i>{}</i> ).</b>",
               "afk_reason": "<b>Я сейчас AFK (время моего отсутсвия: <i>{}</i> ).</b>"
                             "\n\n<b>Причина:</b> <i>{}</i>",
               "afk_go": "<b>Я ушел в AFK.</b>",
               "afk_back": "<b>Я вышел из AFK.</b>",
               "pm_off": "<b>Теперь вы принимаете сообщения от всех пользователей.</b>",
               "pm_on": "<b>Вы перестали принимать сообщения от пользователей.</b>",
               "pm_go_away": "Здравствуй! К сожалению, я не принимаю личные сообщения от незнакомцев."
                             "\n\nСвяжитесь со мной в группе, или ожидайте пока я одобрю вас.",
               "pm_allowed": "<b>Я разрешил {} писать мне.</b>",
               "pm_deny": "<b>Я запретил {} писать мне.</b>",
               "blocked": "<b>{} был(-а) занесен(-а) в Черный Список.</b>",
               "unblocked": "<b>{} удален(-а) из Черного Списка.</b>",
               "addcontact": "<b>{} был(-а) добавлен(-а) в контакты.</b>",
               "delcontact": "<b>{} был(-а) удален(-а) из контактов.</b>",
               "who_to_allow": "<b>Кому разрешить писать в личку ?</b>",
               "who_to_deny": "<b>Кому запретить писать в личку ?</b>",
               "who_to_block": "<b>Укажите, кого блокировать.</b>",
               "who_to_unblock": "<b>Укажите, кого разблокировать.</b>",
               "who_to_contact": "<b>Укажите, кого добавить в контакт.</b>",
               "who_to_delcontact": "<b>Укажите, кого удалить из контактов.</b>"}

    def __init__(self):
        self.me = None

    async def client_ready(self, message, db):
        self.db=db
        self.client = client
        self.me = await client.get_me(True)

    async def afkgocmd(self, message):
        """
        Используй: .afkgo чтобы включить AFK режим.
        Используй: .afkgo [причина] чтобы включить AFK режим и добавить причину.
        """
        if utils.get_args_raw(message):
            self.db.set("AFKMode", "afk", utils.get_args_raw(message))
        else:
            self.db.set("AFKMode", "afk", True)
        self.db.set("AFKMode", "afk_gone", time.time())
        await utils.answer(message, self.strings["afk_go"])

    async def afkbackcmd(self, message):
        """Используй: .afkback чтобы отключить AFK режим."""
        self.db.set("AFKMode", "afk", False)
        self.db.set("AFKMode", "afk_gone", None)
        await utils.answer(message, self.strings["afk_back"])

    async def pmcmd(self, message):
        """Используй: .pm : чтобы включить/отключить авто ответ на личные сообщения."""
        pm = self.db.get("AFKMode", "pm")
        if pm is not True:
            await utils.answer(message, self.strings["pm_off"])
            self.db.set("AFKMode", "pm", True)
        else:
            await utils.answer(message, self.strings["pm_on"])
            self.db.set("AFKMode", "pm", False)

    async def allowcmd(self, message):
        """Используй: .allow чтобы разрешить этому пользователю писать вам в личку."""
        try:
            if message.is_private:
                user = await message.client.get_entity(message.chat_id)
            else:
                return
        except: return await message.edit("<b>Это не лс.</b>")
        self.db.set("AFKMode", "allowed", list(set(self.db.get("AFKMode", "allowed", [])).union({user.id})))
        await utils.answer(message, self.strings["pm_allowed"].format(user.first_name))

    async def denycmd(self, message):
        """Используй: .deny чтобы запретить этому пользователю писать вам в личку."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not args and not reply:
            return await message.edit("<b>Нет аргументов или реплая.</b>")
        try:
            if message.is_private:
                user = await message.client.get_entity(message.chat_id) 
            if args:
                if args.isnumeric(): user = await message.client.get_entity(int(args))
                else: user = await message.client.get_entity(args)
            else: user = await message.client.get_entity(reply.sender_id)
        except: return await message.edit("<b>Взлом жопы.</b>")
        self.db.set("AFKMode", "allowed", list(set(self.db.get("AFKMode", "allowed", [])).difference({user.id})))
        await utils.answer(message, self.strings["pm_deny"].format(user.first_name))

    async def allowedcmd(self, message):
        """Используй: .allowed : чтобы посмотреть список пользователей которым вы разрешили писать в личку."""
        await message.edit("ща покажу")
        args = utils.get_args_raw(message)
        allowed = self.db.get("AFKMode", "allowed", [])
        number = 0
        users = ""
        if args == "clear":
        	self.db.set("AFKMode", "allowed", [])
        	return await message.edit(f"<b>Список был успешно очищен.</b>")
        try:
            for _ in allowed:
                number += 1
                try:
                    user = await message.client.get_entity(int(_))
                except: pass
                if not user.deleted:
                    users += f"{number}. <a href=tg://user?id={user.id}>{user.first_name}</a> | [<code>{user.id}</code>]\n"
                else:
                    users += f"{number} • Удалённый аккаунт ID: [<code>{user.id}</code>]\n"
            await utils.answer(message, "<b>Список пользователей которым я разрешил писать в личку:</b>\n" + users)
        except: return await message.edit("<b>Какой то айди из списка не правильный :/</b>")

    async def blockcmd(self, message):
        """Используй: .block чтобы заблокировать этого пользователя."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if message.is_private:
            user = await message.client.get_entity(message.chat_id)
        else:
            if reply:
                user = await message.client.get_entity(reply.sender_id)
            else:
                user = await message.client.get_entity(int(args) if args.isnumeric() else args)
            if not user:
                await utils.answer(message, self.strings["who_to_block"])
                return
        await message.client(functions.contacts.BlockRequest(user))
        await utils.answer(message, self.strings["blocked"].format(user.first_name))

    async def unblockcmd(self, message):
        """Используй: .unblock чтобы разблокировать этого пользователя."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if message.is_private:
            user = await message.client.get_entity(message.chat_id)
        else:
            if reply:
                user = await message.client.get_entity(reply.sender_id)
            else:
                user = await message.client.get_entity(int(args) if args.isnumeric() else args)
            if not user:
                await utils.answer(message, self.strings["who_to_unblock"])
                return
        await message.client(functions.contacts.UnblockRequest(user))
        await utils.answer(message, self.strings["unblocked"].format(user.first_name))

    async def addcontcmd(self, message):
        """Используй: .addcont чтобы добавить пользователя в свои контакты."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if message.is_private:
            user = await message.client.get_entity(message.chat_id)
        else:
            if reply:
                user = await message.client.get_entity(reply.sender_id)
            else:
                user = await message.client.get_entity(int(args) if args.isnumeric() else args)
            if not user:
                await utils.answer(message, self.strings["who_to_contact"])
                return
        await message.client(functions.contacts.AddContactRequest(id=user.id, first_name=user.first_name, last_name=' ', phone='seen', add_phone_privacy_exception=False))
        await utils.answer(message, self.strings["addcontact"].format(user.first_name))

    async def delcontcmd(self, message):
        """Используй: .delcont чтобы удалить пользователя из своих контактов."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if message.is_private:
            user = await message.client.get_entity(message.chat_id)
        else:
            if reply:
                user = await message.client.get_entity(reply.sender_id)
            else:
                user = await message.client.get_entity(int(args) if args.isnumeric() else args)
            if not user:
                await utils.answer(message, self.strings["who_to_delcontact"])
                return
        await message.client(functions.contacts.DeleteContactsRequest(id=[user.id]))
        await utils.answer(message, self.strings["delcontact"].format(user.first_name))

    async def afkstatuscmd(self, message):
        """Используй: .afkstatus чтобы посмотреть статистику об вашем AFK."""
        afk_status = self.db.get("AFKMode", "afk")
        pm_status = self.db.get("AFKMode", "pm")
        if afk_status is True:
            reason = "Нет"
        else:
            reason = f"{afk_status}"
        if afk_status is not False:
            now = datetime.datetime.now().replace(microsecond=0)
            gone = datetime.datetime.fromtimestamp(self.db.get("AFKMode", "afk_gone")).replace(microsecond=0)
            diff = now - gone
            msg_afk = f"✅ Включен\nВремя: [ <b><i>{diff}</i></b> ]\nПричина: [<i>{reason}</i>]"
        else:
            msg_afk = "❌ Выключен"
        if pm_status is True:
            msg_pm = "✅ Принимаю сообщения"
        else:
            msg_pm = "❌ Не принимаю сообщения"
        afk_message = self.strings["afk_status"].format(msg_afk, msg_pm)
        await utils.answer(message, afk_message)

    async def watcher(self, message):
        try:
            user = await utils.get_user(message)
            pm = self.db.get("AFKMode", "pm")
            if message.sender_id == (await message.client.get_me()).id: return
            if pm is not True:
                if message.is_private:
                    if not self.get_allowed(message.from_id):
                        if user.bot or user.verified:
                            return
                        await utils.answer(message, self.strings["pm_go_away"])
                if message.mentioned or message.is_private:
                    afk_status = self.db.get("AFKMode", "afk")
                    now = datetime.datetime.now().replace(microsecond=0)
                    gone = datetime.datetime.fromtimestamp(self.db.get("AFKMode", "afk_gone")).replace(microsecond=0)
                    diff = now - gone
                    if afk_status is True:
                        afk_message = self.strings["afk"].format(diff)
                    elif afk_status is not False:
                        afk_message = self.strings["afk_reason"].format(diff, afk_status)
                    await utils.answer(message, afk_message)
        except: pass

    def get_allowed(self, id):
        return id in self.db.get("AFKMode", "allowed", [])