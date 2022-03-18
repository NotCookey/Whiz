import discord
from discord.ext import commands
import tenorpy
import configparser
from rich import print
import urllib3
import urllib
from utils import tenorpy
import time
import os
import io
import asyncio
import json
import discum

config = configparser.ConfigParser()
config.read("CONFIG.ini")
bot = commands.Bot(config["DEFAULT"]["PREFIX"], self_bot=True)
tenor = tenorpy.Tenor()
color = ()
requests = urllib3.PoolManager()


@bot.event
async def on_ready():
	os.system("cls")
	print(
		"""[bold cyan]
										
			@@@  @@@  @@@  @@@  @@@  @@@  @@@@@@@@  
			@@@  @@@  @@@  @@@  @@@  @@@  @@@@@@@@  
			@@!  @@!  @@!  @@!  @@@  @@!       @@!  
			!@!  !@!  !@!  !@!  @!@  !@!      !@!   
			@!!  !!@  @!@  @!@!@!@!  !!@     @!!    
			!@!  !!!  !@!  !!!@!!!!  !!!    !!!     
			!!:  !!:  !!:  !!:  !!!  !!:   !!:      
			:!:  :!:  :!:  :!:  !:!  :!:  :!:       
			 :::: :: :::   ::   :::   ::   :: ::::  
			  :: :  : :     :   : :  :    : :: : :  
										
		[/bold cyan]""".center(
			os.get_terminal_size().columns
		)
	)


@bot.command()
async def pingspam(ctx, user: discord.Member, times: int, wait: int = None):
	await ctx.message.delete()
	for ping in range(times):
		await ctx.send(user.mention)
		time.sleep(wait if wait else 0)


@bot.command()
async def meme(ctx):
	await ctx.message.delete()
	content = json.loads(
		requests.request("GET", "https://meme-api.herokuapp.com/gimme").data
	)
	await ctx.send(content["url"])


@bot.command()
async def gif(ctx, *, query):
	await ctx.message.delete()
	await ctx.send(tenor.random(query))


@bot.command()
async def massping(ctx, times: int, delay: float):
	await ctx.message.delete()
	bot = discum.Client(token=config["DEFAULT"]["TOKEN"])

	def close_after_fetching(resp, guild_id):
		if bot.gateway.finishedMemberFetching(guild_id):
			lenmembersfetched = len(bot.gateway.session.guild(guild_id).members)
			print(str(lenmembersfetched) + " members fetched")
			bot.gateway.removeCommand(
				{"function": close_after_fetching, "params": {"guild_id": guild_id}}
			)
			bot.gateway.close()

	def get_members(guild_id, channel_id):
		bot.gateway.fetchMembers(guild_id, channel_id, keep="all", wait=1)
		bot.gateway.command(
			{"function": close_after_fetching, "params": {"guild_id": guild_id}}
		)
		bot.gateway.run()
		bot.gateway.resetSession()
		return bot.gateway.session.guild(guild_id).members

	message = ""

	for member in get_members(str(ctx.guild.id), str(ctx.channel.id)):
		message += f" <@{member}> "
	for i in range(times):
		requests.request(
			"POST",
			f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
			headers={
				"authorization": config["DEFAULT"]["TOKEN"],
				"content-type": "application/json",
			},
			body=json.dumps(
				{
					"content": message,
					"tts": False,
				}
			),
		)
		time.sleep(delay)


@bot.command()
async def hentai(ctx):
	await ctx.message.delete()
	content = json.loads(
		requests.request("GET", "https://hmtai.herokuapp.com/nsfw/creampie").data
	)["url"]
	await ctx.send(content)


@bot.command()
async def purge(ctx, amount: int):
	await ctx.message.delete()
	for message in await ctx.channel.history(limit=amount).flatten():
		await message.delete()


@bot.command()
async def regional(ctx, *, text):
	await ctx.message.delete()
	A = text.lower()
	D = {
		"a": "<:regional_indicator_a:803940414524620800>",
		"b": "<:regional_indicator_b:803940414524620800>",
		"c": "<:regional_indicator_c:803940414524620800>",
		"d": "<:regional_indicator_d:803940414524620800>",
		"e": "<:regional_indicator_e:803940414524620800>",
		"f": "<:regional_indicator_f:803940414524620800>",
		"g": "<:regional_indicator_g:803940414524620800>",
		"h": "<:regional_indicator_h:803940414524620800>",
		"i": "<:regional_indicator_i:803940414524620800>",
		"j": "<:regional_indicator_j:803940414524620800>",
		"k": "<:regional_indicator_k:803940414524620800>",
		"l": "<:regional_indicator_l:803940414524620800>",
		"m": "<:regional_indicator_m:803940414524620800>",
		"n": "<:regional_indicator_n:803940414524620800>",
		"o": "<:regional_indicator_o:803940414524620800>",
		"p": "<:regional_indicator_p:803940414524620800>",
		"q": "<:regional_indicator_q:803940414524620800>",
		"r": "<:regional_indicator_r:803940414524620800>",
		"s": "<:regional_indicator_s:803940414524620800>",
		"t": "<:regional_indicator_t:803940414524620800>",
		"u": "<:regional_indicator_u:803940414524620800>",
		"v": "<:regional_indicator_v:803940414524620800>",
		"w": "<:regional_indicator_w:803940414524620800>",
		"x": "<:regional_indicator_x:803940414524620800>",
		"y": "<:regional_indicator_y:803940414524620800>",
		"z": "<:regional_indicator_z:803940414524620800>",
	}
	B = ""
	A = list(A)
	for C in A:
		if C in D:
			B = B + D[C] + " "
		else:
			B = B + C
	await ctx.send(B)


@bot.command()
async def pornhub(ctx, text, _text):
	await ctx.message.delete()
	await ctx.send(
		file=discord.File(
			io.BytesIO(
				requests.request(
					"GET",
					f"http://api.timbw.xyz:5000/pornhub?text={text}&text2={_text}",
				).data
			),
			"pornhub.jpg",
		)
	)


@bot.command()
async def joke(ctx):
	await ctx.message.delete()
	content = json.loads(
		requests.request(
			"GET",
			"https://v2.jokeapi.dev/joke/Programming,Dark,Spooky?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=twopart",
		).data
	)
	await ctx.send(content["setup"] + "\n" + content["delivery"])


@bot.command()
async def drake(ctx, text, _text):
	await ctx.message.delete()
	await ctx.send(
		file=discord.File(
			io.BytesIO(
				requests.request(
					"GET",
					f"https://apimeme.com/meme?meme=Drake-Bad-Good&top={text}&bottom={_text}",
				).data
			),
			"drake.jpg",
		)
	)


@bot.command()
async def msgspam(ctx, message, amount: int, delay: float = None):
	await ctx.message.delete()
	for _ in range(amount):
		requests.request(
			"POST",
			f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
			headers={
				"authorization": config["DEFAULT"]["TOKEN"],
				"content-type": "application/json",
			},
			body=json.dumps(
				{
					"content": message,
					"tts": False,
				}
			),
		)
		time.sleep(delay if delay else 0)


@bot.command()
async def insult(ctx, user: discord.Member):
	await ctx.message.delete()
	await ctx.send(
		user.mention
		+ ", "
		+ json.loads(
			requests.request(
				"GET", "https://evilinsult.com/generate_insult.php?lang=en&type=json"
			).data
		)["insult"]
	)


@bot.command()
async def ghostpingspam(ctx, user: discord.Member, amount: int, delay: float = None):
	await ctx.message.delete()
	for _ in range(amount):
		await ctx.send(user.mention, delete_after=0.5)
		await asyncio.sleep(delay if delay else 0)


@bot.command()
async def deletechannels(ctx):
	if ctx.author.guild_permissions.manage_channels:
		for channel in ctx.guild.channels:
			try:
				await channel.delete()
			except:
				pass


@bot.command()
async def createchannels(ctx, amount: int, delay: float = None):
	await ctx.message.delete()
	if ctx.author.guild_permissions.manage_channels:
		for _ in range(amount):
			requests.request(
				"POST",
				f"https://discord.com/api/v9/guilds/{ctx.guild.id}/channels",
				headers={
					"authorization": config["DEFAULT"]["TOKEN"],
					"content-type": "application/json",
				},
				body=json.dumps(
					{"type": 0, "name": "Whiz SelfBot", "permission_overwrites": []}
				),
			)
			time.sleep(delay if delay else 0)


@bot.command()
async def banmembers(ctx, delay: float = None):
	await ctx.message.delete()
	if ctx.author.guild_permissions.ban_members:
		for member in ctx.guild.members:
			await ctx.guild.ban(member)


if os.listdir("./modules"):
	for filename in os.listdir("./modules"):
		if filename.endswith(".py"):
			bot.load_extension(f"modules.{filename[:-3]}")

if __name__ == "__main__":
	bot.run(config["DEFAULT"]["TOKEN"])
