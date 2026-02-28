import discord
from discord.ext import commands
import asyncio
import random
import time
import json
import os
import config

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents, help_command=None)

# =========================
# SISTEM SAVE DATA (JSON)
# =========================

DATA_FILE = "player_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

player_stats = load_data()

# =========================
# DATABASE SOAL
# =========================

questions = [
{"q":"Ibu kota Indonesia adalah…","o":["A. Bandung","B. Surabaya","C. Jakarta","D. Medan"],"a":"C","lvl":"Mudah","p":10},
{"q":"5 + 7 = …","o":["A. 10","B. 11","C. 12","D. 13"],"a":"C","lvl":"Mudah","p":10},
{"q":"Warna bendera Indonesia adalah…","o":["A. Merah Putih","B. Biru Putih","C. Merah Biru","D. Hijau Putih"],"a":"A","lvl":"Mudah","p":10},
{"q":"Planet tempat kita tinggal adalah…","o":["A. Mars","B. Bumi","C. Venus","D. Jupiter"],"a":"B","lvl":"Mudah","p":10},
{"q":"9 × 3 = …","o":["A. 18","B. 21","C. 27","D. 24"],"a":"C","lvl":"Mudah","p":10},
{"q":"Ibukota Jepang adalah…","o":["A. Seoul","B. Tokyo","C. Beijing","D. Osaka"],"a":"B","lvl":"Sedang","p":20},
{"q":"Planet terbesar di tata surya adalah…","o":["A. Saturnus","B. Mars","C. Jupiter","D. Uranus"],"a":"C","lvl":"Sedang","p":20},
{"q":"Nomor atom emas adalah…","o":["A. 47","B. 79","C. 92","D. 82"],"a":"B","lvl":"Sulit","p":40},
{"q":"Teori relativitas dikemukakan oleh…","o":["A. Newton","B. Galileo","C. Einstein","D. Tesla"],"a":"C","lvl":"Sulit","p":40},
]

# =========================
# EVENT SAAT BOT ONLINE
# =========================

@bot.event
async def on_ready():
    print(f"Bot aktif sebagai {bot.user}")
    print("Bot Quiz siap digunakan 🎮")

# =========================
# HELP COMMAND
# =========================

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="📚 DAFTAR COMMAND",
        description="""
`!startquiz` → Mulai quiz
`!stats` → Lihat statistik kamu
`!help` → Lihat command
""",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

# =========================
# START QUIZ
# =========================

@bot.command()
async def startquiz(ctx):

    user_id = str(ctx.author.id)
    lives = 3
    score = 0
    start_time = time.time()

    random.shuffle(questions)

    await ctx.send("🎮 **Quiz Dimulai!** Kamu punya 3 nyawa ❤️❤️❤️")

    for q in questions:

        if lives <= 0:
            break

        # Warna berdasarkan level
        if q["lvl"] == "Mudah":
            color = discord.Color.green()
        elif q["lvl"] == "Sedang":
            color = discord.Color.gold()
        else:
            color = discord.Color.red()

        progress_bar = "❤️" * lives + "🖤" * (3 - lives)

        embed = discord.Embed(
            title=f"🎯 LEVEL {q['lvl'].upper()}",
            description=f"**{q['q']}**",
            color=color
        )

        for opt in q["o"]:
            embed.add_field(name=opt, value="\u200b", inline=False)

        embed.set_footer(text=f"Skor: {score} | Nyawa: {progress_bar}")

        await ctx.send(embed=embed)
        await ctx.send("⌛ Jawab A/B/C/D (15 detik)")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        question_start = time.time()

        try:
            msg = await bot.wait_for("message", timeout=15.0, check=check)
            answer_time = round(time.time() - question_start, 2)

            if msg.content.upper() == q["a"]:
                score += q["p"]
                await ctx.send(f"✅ BENAR! +{q['p']} poin | ⏱ {answer_time} detik")
            else:
                lives -= 1
                await ctx.send(f"❌ SALAH! Jawaban benar: {q['a']} | Nyawa tersisa: {lives}")

        except asyncio.TimeoutError:
            lives -= 1
            await ctx.send(f"⏰ Waktu habis! Nyawa tersisa: {lives}")

    total_time = round(time.time() - start_time, 2)

    if lives <= 0:
        await ctx.send("💀 GAME OVER!")

    await ctx.send(f"🏁 Quiz selesai!\n🏆 Skor: {score}\n⏳ Lama bermain: {total_time} detik")

    # =========================
    # SIMPAN DATA
    # =========================

    if user_id not in player_stats:
        player_stats[user_id] = {
            "highscore": 0,
            "playtime": 0
        }

    if score > player_stats[user_id]["highscore"]:
        player_stats[user_id]["highscore"] = score

    player_stats[user_id]["playtime"] += total_time

    save_data(player_stats)

# =========================
# STATS COMMAND
# =========================

@bot.command()
async def stats(ctx):

    user_id = str(ctx.author.id)

    if user_id not in player_stats:
        await ctx.send("📭 Belum ada data stats.")
        return

    data = player_stats[user_id]

    embed = discord.Embed(
        title="📊 STATISTIK PLAYER",
        color=discord.Color.purple()
    )

    embed.add_field(name="🏆 High Score", value=data["highscore"], inline=False)
    embed.add_field(name="⏳ Total Waktu Bermain", value=f"{round(data['playtime'],2)} detik", inline=False)
    embed.set_footer(text=f"Player: {ctx.author.name}")

    await ctx.send(embed=embed)

# =========================
# RUN BOT
# =========================

bot.run(config.TOKEN)