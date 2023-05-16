import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

links = {}

@bot.command()
async def addlink(ctx, client, nome, link):
    if client not in links:
        links[client] = {}
    links[client][nome] = link
    await ctx.send(f"Link Adicionado para {client} = {nome}")

@bot.command()
async def removelink(ctx, client, nome):
    if client in links and nome in links[client]:
        del links[client][nome]
        await ctx.send(f"Link removido para {client} - {nome}")
    else:
        await ctx.send(f"Não foi possível encontrar o link para {client} - {nome}")

@bot.command()
async def links(ctx, client):
    if client in links:
        sorted_links = sorted(links[client].items(), key=lambda x: [0])
        response = '\n'.join([f"{client} - {nome} - {link}" for nome, link in sorted_links])
        await ctx.send(response)
    else:
        await ctx.send(f"Não foi possível encontrar links para {client}")

    bot.run('MTEwNzQ2NDY0NzA4NDM1MTU0OA.GGjFzg.gvgGmmt2aaJH9nZ4h3xXSilTaNkzHLZUvtPwRE')