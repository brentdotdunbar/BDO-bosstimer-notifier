import requests
from bs4 import BeautifulSoup
import discord
import asyncio
#provide token here
#TOKEN = 
client = discord.Client()

timer_channels = []


async def look_for_bosstime():
	while True:
		await client.wait_until_ready()
		await asyncio.sleep(5)
		soup = BeautifulSoup(requests.get('https://mmotimer.com/bdo/?server=na').text, 'html.parser')
		boss_list = soup.find_all(class_ = 'next-boss-title')
		boss_timers = soup.find_all(class_ = 'next-boss-timer countdown')
		previous_boss_timers = soup.find_all(class_ = 'previous-boss-timer countup')
		offset = len(previous_boss_timers)		
		
		next_boss = boss_list[0+offset].contents[0]
		boss_after_next = boss_list[1+offset].contents[0]

		next_boss_timer = boss_timers[0].contents[0].strip()
		boss_after_next_timer = boss_timers[1].contents[0].strip()
		hours_until_boss = int(next_boss_timer[1:2])
		minutes_until_boss = int(next_boss_timer[3:5])

		if hours_until_boss == 0 and minutes_until_boss < 30:
			print('Sending Notification')
			for i in timer_channels:
				await i.send('Get Ready! ' + next_boss + ' is in ' + next_boss_timer.strip())
			await asyncio.sleep(900)
		else:
			await asyncio.sleep(900)


@client.event
async def on_ready():
	print('Running')
	for guild in client.guilds:
		for channel in guild.channels:
			if str(channel.name) == 'auto-boss-alerts':
				timer_channels.append(channel)
@client.event
async def on_guild_join(guild):
	new_chan = await guild.create_text_channel('auto-boss-alerts')
	timer_channels.append(new_chan)
	

	

@client.event
async def on_message(message): 
	if message.author == client.user:
		return

	if message.content.lower() == ('bosstimes'):
		soup = BeautifulSoup(requests.get('https://mmotimer.com/bdo/?server=na').text, 'html.parser')

		boss_list = soup.find_all(class_ = 'next-boss-title')
		boss_timers = soup.find_all(class_ = 'next-boss-timer countdown')
		previous_boss_timers = soup.find_all(class_ = 'previous-boss-timer countup')
		offset = len(previous_boss_timers)
		
		next_boss = boss_list[0+offset].contents[0]
		boss_after_next = boss_list[1+offset].contents[0]

		next_boss_timer = boss_timers[0].contents[0].strip()
		boss_after_next_timer = boss_timers[1].contents[0].strip()
	
		embed=discord.Embed(title="**Boss Times**", description= 'The Next bosses are: \n' + next_boss + ' in ' + next_boss_timer + '\n' + 
		boss_after_next + ' in ' + boss_after_next_timer, color=0x0fb717)

		await message.channel.send(embed=embed)



	if message.content.lower() == ('bosslist'):
		soup = BeautifulSoup(requests.get('https://mmotimer.com/bdo/?server=na').text, 'html.parser')


		boss_list = soup.find_all(class_ = 'next-boss-title')
		boss_timers = soup.find_all(class_ = 'next-boss-timer countdown')
		previous_boss_timers = soup.find_all(class_ = 'previous-boss-timer countup')
		offset = len(previous_boss_timers)
		
		next_boss = boss_list[0+offset].contents[0]
		boss_after_next = boss_list[1+offset].contents[0]

		next_boss_timer = boss_timers[0].contents[0].strip()
		boss_after_next_timer = boss_timers[1].contents[0].strip()
		long_boss_list = soup.find_all(class_  = 'align-middle table-first-col')

		long_counter_list = soup.find_all(class_ = 'countdown')
		test = ""
		for i in range(10):
			test += (long_boss_list[i].contents[2].strip() + ' in ' + long_counter_list[i+2].contents[0].strip() + '\n')
		test = next_boss + ' in ' + next_boss_timer + '\n' + boss_after_next + ' in ' + boss_after_next_timer + '\n' + test
		embed = discord.Embed(title="**Boss Times**", description= test,  color=0x0fb717)
		await message.channel.send(embed=embed)
		
		
		
		
	if message.content.lower() == ('nextboss'):
		soup = BeautifulSoup(requests.get('https://mmotimer.com/bdo/?server=na').text, 'html.parser')
		boss_list = soup.find_all(class_ = 'next-boss-title')
		boss_timers = soup.find_all(class_ = 'next-boss-timer countdown')
		previous_boss_timers = soup.find_all(class_ = 'previous-boss-timer countup')
		offset = len(previous_boss_timers)		
		
		next_boss = boss_list[0+offset].contents[0]
		boss_after_next = boss_list[1+offset].contents[0]

		next_boss_timer = boss_timers[0].contents[0].strip()
		boss_after_next_timer = boss_timers[1].contents[0].strip()
		if str(next_boss_timer) == str(boss_after_next_timer):
			await message.channel.send('The Next boss: ' + next_boss + ' and ' + boss_after_next +' are in ' + next_boss_timer.strip() )
		else:
			await message.channel.send('The Next boss: ' + next_boss + ' is in ' + next_boss_timer.strip())


	if message.content.lower() == 'resettime':
		soup = BeautifulSoup(requests.get('https://mmotimer.com/bdo/?server=na').text, 'html.parser')
		reset_timer = soup.find(class_ = 'countdown3').contents[0]
		await message.channel.send('The reset happens in: ' + str(reset_timer))
	
	
client.loop.create_task(look_for_bosstime())
client.run(TOKEN)
