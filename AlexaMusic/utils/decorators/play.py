import asyncio

from pyrogram.enums import CHATMemberStatus
from pyrogram.errors import (
    CHATAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from AlexaMusic import YouTube, app
from AlexaMusic.misc import SUDOERS
from AlexaMusic.utils.database import (
    get_assistant,
    get_cmode,
    get_lang,
    get_playmode,
    get_playtype,
    is_active_CHAT,
    is_maintenance,
)
from AlexaMusic.utils.inline import botplaylist_markup
from config import PLAYLIST_IMG_URL, SUPPORT_CHAT, adminlist
from strings import get_string

links = {}


def PlayWrapper(command):
    async def wrapper(client, message):
        language = await get_lang(message.CHAT.id)
        _ = get_string(language)
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    text=f"{app.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ, ᴠɪsɪᴛ <a href={SUPPORT_CHAT}>sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ</a> ғᴏʀ ᴋɴᴏᴡɪɴɢ ᴛʜᴇ ʀᴇᴀsᴏɴ.",
                    disable_web_page_preview=True,
                )

        try:
            await message.delete()
        except:
            pass

        audio_telegram = (
            (message.reply_to_message.audio or message.reply_to_message.voice)
            if message.reply_to_message
            else None
        )
        video_telegram = (
            (message.reply_to_message.video or message.reply_to_message.document)
            if message.reply_to_message
            else None
        )
        url = await YouTube.url(message)
        if audio_telegram is None and video_telegram is None and url is None:
            if len(message.command) < 2:
                if "stream" in message.command:
                    return await message.reply_text(_["str_1"])
                buttons = botplaylist_markup(_)
                return await message.reply_photo(
                    photo=PLAYLIST_IMG_URL,
                    caption=_["play_18"],
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        if message.command[0][0] == "c":
            CHAT_id = await get_cmode(message.CHAT.id)
            if CHAT_id is None:
                return await message.reply_text(_["setting_7"])
            try:
                CHAT = await app.get_CHAT(CHAT_id)
            except:
                return await message.reply_text(_["cplay_4"])
            channel = CHAT.title
        else:
            CHAT_id = message.CHAT.id
            channel = None
        playmode = await get_playmode(message.CHAT.id)
        playty = await get_playtype(message.CHAT.id)
        if playty != "Everyone":
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.CHAT.id)
                if not admins:
                    return await message.reply_text(_["admin_13"])
                else:
                    if message.from_user.id not in admins:
                        return await message.reply_text(_["play_4"])
        if message.command[0][0] == "v":
            video = True
        else:
            if "-v" in message.text:
                video = True
            else:
                video = True if message.command[0][1] == "v" else None
        if message.command[0][-1] == "e":
            if not await is_active_CHAT(CHAT_id):
                return await message.reply_text(_["play_16"])
            fplay = True
        else:
            fplay = None

        if not await is_active_CHAT(CHAT_id):
            userbot = await get_assistant(CHAT_id)
            try:
                try:
                    get = await app.get_CHAT_member(CHAT_id, userbot.id)
                except CHATAdminRequired:
                    return await message.reply_text(_["call_1"])
                if (
                    get.status == CHATMemberStatus.BANNED
                    or get.status == CHATMemberStatus.RESTRICTED
                ):
                    return await message.reply_text(
                        _["call_2"].format(
                            app.mention, userbot.id, userbot.name, userbot.username
                        )
                    )
            except UserNotParticipant:
                if CHAT_id in links:
                    invitelink = links[CHAT_id]
                else:
                    if message.CHAT.username:
                        invitelink = message.CHAT.username
                        try:
                            await userbot.resolve_peer(invitelink)
                        except:
                            pass
                    else:
                        try:
                            invitelink = await app.export_CHAT_invite_link(CHAT_id)
                        except CHATAdminRequired:
                            return await message.reply_text(_["call_1"])
                        except Exception as e:
                            return await message.reply_text(
                                _["call_3"].format(app.mention, type(e).__name__)
                            )

                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinCHAT/"
                    )
                myu = await message.reply_text(_["call_4"].format(app.mention))
                try:
                    await asyncio.sleep(1)
                    await userbot.join_CHAT(invitelink)
                except InviteRequestSent:
                    try:
                        await app.approve_CHAT_join_request(CHAT_id, userbot.id)
                    except Exception as e:
                        return await message.reply_text(
                            _["call_3"].format(app.mention, type(e).__name__)
                        )
                    await asyncio.sleep(3)
                    await myu.edit(_["call_5"].format(app.mention))
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    return await message.reply_text(
                        _["call_3"].format(app.mention, type(e).__name__)
                    )

                links[CHAT_id] = invitelink

                try:
                    await userbot.resolve_peer(CHAT_id)
                except:
                    pass

        return await command(
            client,
            message,
            _,
            CHAT_id,
            video,
            channel,
            playmode,
            url,
            fplay,
        )

    return wrapper
