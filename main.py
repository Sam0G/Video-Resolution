import os
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeVideo

# استبدل هذه القيم ببياناتك الحقيقية
API_ID = 38831490              # رقم api_id
API_HASH = "d8f0dfa3edfa244df7f5623fef10826b"    # كود api_hash
BOT_TOKEN = "8953003387:AAEUDPy1HTWbc35-lvgfeYxHzQ8qbEOE4aI" # توكن BotFather

bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

def classify_resolution(width: int, height: int) -> str:
    res = min(width, height)
    if res >= 2160:
        label = "2160p (4K UHD)"
    elif res >= 1440:
        label = "1440p (2K QHD)"
    elif res >= 1080:
        label = "1080p (Full HD)"
    elif res >= 720:
        label = "720p (HD)"
    elif res >= 540:
        label = "540p"
    elif res >= 480:
        label = "480p (SD)"
    elif res >= 360:
        label = "360p"
    else:
        label = f"{res}p"
    return f"{label} ({width}x{height})"

@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.reply("أهلاً بك! أرسل أو حوّل لي أي ملف فيديو (حتى لو كان 5GB)، وسأخبرك بأبعاده ودقته الحقيقية المشفرة داخله.")

@bot.on(events.NewMessage)
async def check_resolution(event):
    if event.text and event.text.startswith('/'):
        return

    msg = event.message
    width, height = None, None

    if msg.video:
        for attr in msg.video.attributes:
            if isinstance(attr, DocumentAttributeVideo):
                width, height = attr.w, attr.h
                break
    elif msg.document:
        for attr in msg.document.attributes:
            if isinstance(attr, DocumentAttributeVideo):
                width, height = attr.w, attr.h
                break

    if width and height:
        result = classify_resolution(width, height)
        await event.reply(f"🎬 **دقة الفيديو الفعلية:**\n{result}")
    elif msg.media:
        await event.reply("⚠️ لم يسجل تليجرام أبعاد الفيديو لهذا الملف (قد لا تكون الترويسة مدعومة أو الملف تالف).")

print("البوت يعمل الآن على السيرفر...")
bot.run_until_disconnected()
