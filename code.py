import discord
import feedparser
import requests
import asyncio
import os

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))   # your channel ID (integer)
NEWS_API_KEY = os.getenv('NEWSAPI_KEY')

RSS_FEEDS = [
    'https://threatpost.com/feed/',
    'https://www.bleepingcomputer.com/feed/',
    'https://krebsonsecurity.com/feed/',
    'https://www.darkreading.com/rss.xml',
    'https://www.securityweek.com/feed'
]

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def send_news():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        print("❌ Channel not found or bot lacks permission")
        return

    # 🔹 1. Send top RSS headlines
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:1]:  # send top 1 per feed
            title = entry.title
            link = entry.link
            msg = f"📰 **{title}**\n{link}"
            await channel.send(msg)
            await asyncio.sleep(2)

    # 🔹 2. Send headlines from NewsAPI
    print("📡 Fetching NewsAPI results...")
    url = f"https://newsapi.org/v2/everything?q=cybersecurity&language=en&pageSize=3&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get("status") == "ok":
        for article in data["articles"]:
            title = article["title"]
            link = article["url"]
            source = article["source"]["name"]
            msg = f"🌐 **{title}** ({source})\n{link}"
            await channel.send(msg)
            await asyncio.sleep(2)
    else:
        await channel.send("⚠️ Error fetching news from NewsAPI.")

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    await send_news()
    await client.close()

client.run(TOKEN)
