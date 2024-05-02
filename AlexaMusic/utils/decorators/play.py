# Copyright (C) 2024 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

""""
TheTeamAlexa is a project of Telegram bots with variety of purposes.
Copyright (c) 2024 -present Team=Alexa <https://github.com/TheTeamAlexa>

This program is free software: you can redistribute it and can modify
as you want or you can collabe if you have new ideas.
"""
import asyncio

from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import PLAYLIST_IMG_URL, PRIVATE_BOT_MODE, adminlist
from AlexaMusic.misc import db
from strings import get_string
from AlexaMusic import YouTube, app
from AlexaMusic.misc import SUDOERS
from AlexaMusic.utils.database import (
    get_cmode,
    get_lang,
    get_playmode,
    get_assistant,
    get_playtype,
    is_active_chat,
    is_commanddelete_on,
    is_served_private_chat,
)
from AlexaMusic.utils.database.memorydatabase import is_maintenance
from AlexaMusic.utils.inline.playlist import botplaylist_markup

links = {}


def PlayWrapper(command):
    async def wrapper(client, message):
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    "Bot is under maintenance. Please wait for some time..."
                )
        if PRIVATE_BOT_MODE == str(True):
            if not await is_served_private_GROUP(message.GROUP.id):
                await message.reply_text(
                    "**Private Music Bot**\n\nOnly for authorized GROUPs from the owner. Ask my owner to allow your GROUP first."
                )
                return await app.leave_GROUP(message.GROUP.id)
       if await is_commanddelete_on(message.chat.id):
            try:
                await message.delete()
            except:
                pass
        language = await get_lang(message.GROUP.id)
        _ = get_string(language)
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
                    caption=_["playlist_1"],
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        if message.command[0][0] == "c":
            GROUP_id = await get_cmode(message.GROUP.id)
            if GROUP_id is None:
                return await message.reply_text(_["setting_12"])
            try:
                GROUP = await app.get_GROUP(GROUP_id)
            except:
                return await message.reply_text(_["cplay_4"])
            channel = GROUP.title
        else:
            GROUP_id = message.GROUP.id
            channel = None
        playmode = await get_playmode(message.GROUP.id)
        playty = await get_playtype(message.GROUP.id)
        if playty != "Everyone":
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.GROUP.id)
                if not admins:
                    return await message.reply_text(_["admin_18"])
                if message.from_user.id not in admins:
                    return await message.reply_text(_["play_4"])
        if message.command[0][0] == "v":
            video = True
        else:
            if message.text and "-v" in message.text:
                video = True
            else:
                video = True if message.command[0][1] == "v" else None
        if message.command[0][-1] == "e":
            if not await is_active_GROUP(GROUP_id):
                return await message.reply_text(_["play_18"])
            fplay = True
        else:
            fplay = None

        if not await is_active_GROUP(GROUP_id):
            userbot = await get_assistant(GROUP_id)
            try:
                try:
                    get = await app.get_GROUP_member(GROUP_id, userbot.id)
                except GROUPAdminRequired:
                    return await message.reply_text(_["call_12"])
                if get.status in [
                    GROUPMemberStatus.BANNED,
                    GROUPMemberStatus.RESTRICTED,
                ]:
                    return await message.reply_text(
                        _["call_13"].format(
                            app.mention, userbot.id, userbot.name, userbot.username
                        )
                    )
            except UserNotParticipant:
                if GROUP_id in links:
                    invitelink = links[GROUP_id]
                else:
                    if message.GROUP.username:
                        invitelink = message.GROUP.username
                        try:
                            await userbot.resolve_peer(invitelink)
                        except:
                            pass
                    else:
                        try:
                            invitelink = await app.export_GROUP_invite_link(GROUP_id)
                        except GROUPAdminRequired:
                            return await message.reply_text(_["call_12"])
                        except Exception as e:
                            return await message.reply_text(
                                _["call_14"].format(app.mention, type(e).__name__)
                            )

                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinGROUP/"
                    )
                myu = await message.reply_text(_["call_15"].format(app.mention))
                try:
                    await asyncio.sleep(1)
                    await userbot.join_GROUP(invitelink)
                except InviteRequestSent:
                    try:
                        await app.approve_GROUP_join_request(GROUP_id, userbot.id)
                    except Exception as e:
                        return await message.reply_text(
                            _["call_14"].format(app.mention, type(e).__name__)
                        )
                    await asyncio.sleep(3)
                    await myu.edit(_["call_16"].format(app.mention))
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    return await message.reply_text(
                        _["call_14"].format(app.mention, type(e).__name__)
                    )

                links[GROUP_id] = invitelink

                try:
                    await userbot.resolve_peer(GROUP_id)
                except:
                    pass

        return await command(
            client,
            message,
            _,
            GROUP_id,
            video,
            channel,
            playmode,
            url,
            fplay,
        )

    return wrapper
