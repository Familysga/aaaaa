import asyncio
import os
import time
import requests
import aiohttp
import config
from pyrogram import filters
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from strings.filters import command
from AlexaMusic import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)
from AlexaMusic import app

import re
import sys
from os import getenv

from dotenv import load_dotenv



@app.on_message(
    command(["الاصدار"])
  
)
async def bkouqw(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/ba967503682a55beaedd3.png",
        caption=f"""**اهلا بك عزيزي {message.from_user.mention} Alexa في اصدار سورس  
★᚜ SOURCE Alexa 𖢎

★᚜ نوع : ميوزك

★᚜ اللغه : اللغه العربيه ويدعم الانجليزيه 

★᚜ مجال العمل : بوتات تشغيل الموسيقى في الاتصال
★᚜ نظام التشغيل : كارولين بوت ميوزك
★᚜ الاصدار 1.0
★᚜ تاريخ التأسيس : 2023/11/20

★᚜ مؤسس  السورس : [ 𝐋𝐄𝐀𝐃𝐄𝐑 𝐒𝐀𝐃𝐃𝐀𝐌 𝐇𝐔𝐒𝐒𝐄𝐈𝐍](https://t.me/S_1_02)""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "SOURCE Alexa 𖢎", url=f"https://t.me/A1DIIU"), 
                 ],[
                 InlineKeyboardButton(
                        "", callback_data="hpdtsnju"),
               ],
          ]
        ),
    )
