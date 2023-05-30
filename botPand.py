import os
import discord
import pandas as pd
from discord.ext import commands
import asyncio
import sys
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True # se necessário
intents.presences = True # se necessário

# Carrega o arquivo CSV com os links (se não existir, cria um novo)
try:
    df_links = pd.read_csv('links.csv', index_col=0)
except FileNotFoundError:
    df_links = pd.DataFrame(columns=['Canal', 'Site', 'Link'])

# Configuração do bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando não encontrado. Digite um comando válido! \n!commands para listar os comandos.")

@bot.command(name='commands')
async def custom_help(ctx, *args):
    if not args:
        embed = discord.Embed(title="Comandos do Bot", description="Aqui estão os comandos disponíveis:")
        # Adicione campos ao embed para cada comando personalizado do seu bot
        embed.add_field(name="!addlink", value="Adiciona um novo link")
        embed.add_field(name="!allinks", value="Exibe todos os links cadastrados")
        embed.add_field(name="!client", value="Busca pelo cliente")
        embed.add_field(name="!title", value="Busca pelo titulo")
        await ctx.send(embed=embed)
    else:
        pass

# Comando para adicionar um novo link
@bot.command()
async def addlink(ctx, canal:str, site:str, link:str):
    global df_links
    new_row = {'Canal': canal, 'Site': site, 'Link': link}
    df_links.loc[len(df_links)] = new_row
    df_links.to_csv('links.csv', encoding='utf-8')
    await ctx.send(f'Link adicionado: {canal} - {site}: {link}')

# Comando para exibir todos os links cadastrados
@bot.command()
async def allinks(ctx):
    global df_links

    # Verifica se existem links cadastrados
    if len(df_links) == 0:
        await ctx.send('Não há links cadastrados!')
        return

    # Monta a mensagem com a lista de links
    msg = 'Links cadastrados:\n\n'
    for index, row in df_links.iterrows():
        msg += f'{index}: **[{row["Canal"]}]** {row["Site"]} - {row["Link"]}\n'

    await ctx.send(msg)

@bot.command()
async def client(ctx, canal:str):
    global df_links

    #filtered_links = df_links.loc[df_links['Canal'] == canal]
    filtered_links = df_links[df_links['Canal'].str.contains(canal)]

    if len(filtered_links) == 0:
        await ctx.send(f'Não há link cadastrados para o Cliente {canal}')
        return

    msg = f'Links do Cliente {canal}:\n\n'
    for index, row in filtered_links.iterrows():
        msg += f'{index}: **[{row["Canal"]}]** {row["Site"]} - {row["Link"]} \n'

    await ctx.send(msg)

@bot.command()
async def title(ctx, nome:str):
    global df_links

    filtered_links = df_links[df_links['Site'].str.contains(nome)]

    if len(filtered_links) == 0:
        await ctx.send(f'Não há link cadastrados para o Cliente {nome}')
        return

    msg = f'Resultados para {nome}:\n\n'
    for index, row in filtered_links.iterrows():
        msg += f'{index}: **[{row["Canal"]}]** {row["Site"]} - {row["Link"]} \n'

    await ctx.send(msg)

@bot.command()
async def valida(ctx, name:str):
    file_path = 'C:/Users/Gustavo/Projetos/dataValidator/main.py'
    cmd = ['python', file_path, f'{name}.env']

    process = await asyncio.create_subprocess_exec(*cmd)

    await process.communicate()

# Executa o bot
load_dotenv()
bot.run(os.getenv('ID_BOT'))
