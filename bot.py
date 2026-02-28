import discord
from discord.ext import commands
import config
import asyncio
import random
import time

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents, help_command=None)

# =========================
# DATA PENYIMPANAN STATS
# =========================

player_stats = {}

# =========================
# DATABASE SOAL
# =========================

questions = [
# MUDAH (15)
{"q":"Ibu kota Indonesia adalah…","o":["A. Bandung","B. Surabaya","C. Jakarta","D. Medan"],"a":"C","lvl":"Mudah","p":10},
{"q":"5 + 7 = …","o":["A. 10","B. 11","C. 12","D. 13"],"a":"C","lvl":"Mudah","p":10},
{"q":"Warna bendera Indonesia adalah…","o":["A. Merah Putih","B. Biru Putih","C. Merah Biru","D. Hijau Putih"],"a":"A","lvl":"Mudah","p":10},
{"q":"Planet tempat kita tinggal adalah…","o":["A. Mars","B. Bumi","C. Venus","D. Jupiter"],"a":"B","lvl":"Mudah","p":10},
{"q":"Hewan yang bertelur adalah…","o":["A. Kucing","B. Ayam","C. Sapi","D. Kambing"],"a":"B","lvl":"Mudah","p":10},
{"q":"Air membeku pada suhu…","o":["A. 0°C","B. 10°C","C. 50°C","D. 100°C"],"a":"A","lvl":"Mudah","p":10},
{"q":"Alat untuk melihat benda kecil adalah…","o":["A. Teleskop","B. Mikroskop","C. Lup","D. Kamera"],"a":"B","lvl":"Mudah","p":10},
{"q":"Bahasa resmi Indonesia adalah…","o":["A. Jawa","B. Sunda","C. Melayu","D. Indonesia"],"a":"D","lvl":"Mudah","p":10},
{"q":"9 × 3 = …","o":["A. 18","B. 21","C. 27","D. 24"],"a":"C","lvl":"Mudah","p":10},
{"q":"Matahari terbit di…","o":["A. Barat","B. Utara","C. Timur","D. Selatan"],"a":"C","lvl":"Mudah","p":10},
{"q":"Ikan bernapas dengan…","o":["A. Paru-paru","B. Insang","C. Kulit","D. Hidung"],"a":"B","lvl":"Mudah","p":10},
{"q":"Hari setelah Senin adalah…","o":["A. Rabu","B. Minggu","C. Selasa","D. Kamis"],"a":"C","lvl":"Mudah","p":10},
{"q":"100 ÷ 10 = …","o":["A. 5","B. 10","C. 20","D. 50"],"a":"B","lvl":"Mudah","p":10},
{"q":"Hewan tercepat di darat adalah…","o":["A. Singa","B. Kuda","C. Cheetah","D. Harimau"],"a":"C","lvl":"Mudah","p":10},
{"q":"Warna daun pada umumnya adalah…","o":["A. Merah","B. Hijau","C. Biru","D. Kuning"],"a":"B","lvl":"Mudah","p":10},

# SEDANG (10)
{"q":"Ibukota Jepang adalah…","o":["A. Seoul","B. Tokyo","C. Beijing","D. Osaka"],"a":"B","lvl":"Sedang","p":20},
{"q":"Unsur dengan simbol Fe adalah…","o":["A. Fluor","B. Fosfor","C. Besi","D. Francium"],"a":"C","lvl":"Sedang","p":20},
{"q":"Sungai terpanjang di dunia adalah…","o":["A. Amazon","B. Nil","C. Mississippi","D. Yangtze"],"a":"B","lvl":"Sedang","p":20},
{"q":"Planet terbesar di tata surya adalah…","o":["A. Saturnus","B. Mars","C. Jupiter","D. Uranus"],"a":"C","lvl":"Sedang","p":20},
{"q":"Penemu telepon adalah…","o":["A. Thomas Edison","B. Nikola Tesla","C. Alexander Graham Bell","D. Isaac Newton"],"a":"C","lvl":"Sedang","p":20},
{"q":"Negara dengan populasi terbesar di dunia adalah…","o":["A. India","B. Amerika Serikat","C. China","D. Indonesia"],"a":"A","lvl":"Sedang","p":20},
{"q":"Nilai π mendekati…","o":["A. 2,14","B. 3,14","C. 4,13","D. 3,41"],"a":"B","lvl":"Sedang","p":20},
{"q":"Gunung tertinggi di dunia adalah…","o":["A. Kilimanjaro","B. Everest","C. Fuji","D. Elbrus"],"a":"B","lvl":"Sedang","p":20},
{"q":"Bahasa resmi Brasil adalah…","o":["A. Spanyol","B. Portugis","C. Inggris","D. Prancis"],"a":"B","lvl":"Sedang","p":20},
{"q":"Organ pemompa darah adalah…","o":["A. Paru-paru","B. Otak","C. Jantung","D. Hati"],"a":"C","lvl":"Sedang","p":20},

# SULIT (5)
{"q":"Nomor atom emas adalah…","o":["A. 47","B. 79","C. 92","D. 82"],"a":"B","lvl":"Sulit","p":40},
{"q":"Teori relativitas dikemukakan oleh…","o":["A. Newton","B. Galileo","C. Einstein","D. Tesla"],"a":"C","lvl":"Sulit","p":40},
{"q":"Novel '1984' ditulis oleh…","o":["A. Orwell","B. Huxley","C. Hemingway","D. Tolstoy"],"a":"A","lvl":"Sulit","p":40},
{"q":"Gas paling banyak di atmosfer Bumi adalah…","o":["A. Oksigen","B. Nitrogen","C. Karbon dioksida","D. Hidrogen"],"a":"B","lvl":"Sulit","p":40},
{"q":"Senyawa H₂O₂ disebut…","o":["A. Air","B. Hidrogen","C. Hidrogen peroksida","D. Oksigen cair"],"a":"C","lvl":"Sulit","p":40},
]

# =========================
# EVENT SAAT BOT ONLINE
# =========================

@bot.event
async def on_ready():
    print(f"Bot aktif sebagai {bot.user}")
    print("Halo! Bot Quiz siap digunakan 🎮")

# =========================
# COMMAND HELP
# =========================

@bot.command()
async def help(ctx):
    await ctx.send("""
📚 **DAFTAR COMMAND**
```
!startquiz → Mulai quiz
!stats → Lihat statistik kamu
!help → Lihat command```
""")

# =========================
# START QUIZ
# =========================

@bot.command()
async def startquiz(ctx):
    user_id = ctx.author.id
    lives = 3
    score = 0
    start_time = time.time()

    random.shuffle(questions)

    await ctx.send(f"🎮 Quiz Dimulai! Nyawa: {lives}")

    for q in questions:
        if lives <= 0:
            break

        embed = discord.Embed(title=f"Level {q['lvl']}", description=q["q"], color=discord.Color.blue())
        for opt in q["o"]:
            embed.add_field(name=opt, value="\u200b", inline=False)

        await ctx.send(embed=embed)
        await ctx.send("Jawab A/B/C/D (15 detik)")

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

    await ctx.send(f"🏁 Quiz selesai!\nSkor: {score}\nLama bermain: {total_time} detik")

    # Simpan stats
    if user_id not in player_stats:
        player_stats[user_id] = {"highscore": 0, "playtime": 0}

    if score > player_stats[user_id]["highscore"]:
        player_stats[user_id]["highscore"] = score

    player_stats[user_id]["playtime"] += total_time

# =========================
# STATS COMMAND
# =========================

@bot.command()
async def stats(ctx):
    user_id = ctx.author.id

    if user_id not in player_stats:
        await ctx.send("Belum ada data stats.")
        return

    data = player_stats[user_id]

    await ctx.send(f"""
📊 **Statistik Kamu**
🏆 High Score: {data['highscore']}
⏳ Total Waktu Bermain: {round(data['playtime'],2)} detik
""")

bot.run(config.TOKEN)