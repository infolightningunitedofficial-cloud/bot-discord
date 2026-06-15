import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

FILE = r"G:\discord_bot\magazzino.json"

# 📦 CARICA/SALVA
def carica():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}

def salva():
    with open(FILE, "w") as f:
        json.dump(prodotti, f)

prodotti = carica()

# 👋 WELCOME MESSAGE
@bot.event
async def on_member_join(member):
    try:
        await member.send(
            f"Ciao {member.name} 👋 benvenuto nel server!\n"
            "🛒 Qui trovi le migliori offerte disponibili!"
        )
    except:
        pass

# 🤖 BOT ONLINE
@bot.event
async def on_ready():
    print(f"Bot online come {bot.user}")

# ➕ AGGIUNGI PRODOTTO
@bot.command()
async def aggiungi(ctx, nome, prezzo: int, stock: int, *, descrizione_foto):
    try:
        descrizione, foto = descrizione_foto.rsplit(" ", 1)

        prodotti[nome] = {
            "prezzo": prezzo,
            "stock": stock,
            "descrizione": descrizione,
            "foto": foto
        }

        salva()
        await ctx.send(f"✅ Prodotto aggiunto: {nome}")

    except:
        await ctx.send("❌ Usa: !aggiungi nome prezzo stock descrizione LINKFOTO")

# 📦 LISTA PRODOTTI
@bot.command()
async def lista(ctx):
    if len(prodotti) == 0:
        await ctx.send("📦 Nessun prodotto disponibile")
        return

    for nome, p in prodotti.items():
        embed = discord.Embed(
            title=f"🛒 {nome}",
            description=p["descrizione"],
            color=discord.Color.green()
        )

        embed.add_field(name="💰 Prezzo", value=f"{p['prezzo']}€", inline=True)
        embed.add_field(name="📦 Stock", value=p["stock"], inline=True)

        # 🖼️ immagine prodotto
        embed.set_image(url=p["foto"])

        await ctx.send(embed=embed)

# 📢 PUBBLICA OFFERTA
@bot.command()
async def offerta(ctx, nome):
    if nome not in prodotti:
        await ctx.send("❌ Prodotto non trovato")
        return

    p = prodotti[nome]

    embed = discord.Embed(
        title=f"🔥 OFFERTA: {nome}",
        description=f"{p['descrizione']}\n\n👉 **ACQUISTA SUBITO!**",
        color=discord.Color.red()
    )
    embed.add_field(name="💰 Prezzo", value=f"{p['prezzo']}€")
    embed.add_field(name="📦 Stock", value=p["stock"])

    await ctx.send("@everyone", embed=embed)

# ℹ️ INFO CONTATTI
@bot.command()
async def info(ctx):
    await ctx.send(
        "📞 CONTATTI SHOP:\n"
        "Telegram: @notbrooo\n"
        "💬 Scrivimi in DM per acquistare!"
    )

# 🔑 TOKEN
import os
bot.run(os.getenv("TOKEN"))
