#! /usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @name   : Discordpy-ECommerce-System - Digital Currency Trade System for Discord Servers!
# @url    : https://github.com/Cisc0-gif/Discordpy-ECommerce-System
# @author : Cisc0-gif

import discord
import asyncio
import logging
import os
import random
import time
import sys
import sqlite3

client = discord.Client(command_prefix='/', description='Basic Commands')
TOKEN = ''

# Go To https://discordapp.com/developers/applications/ and start a new application for Token

print('Checking if REGISTRY exists...')
dbcheck = os.path.isfile('REGISTRY.db')
if dbcheck == True:
  print('File exists!')
else:
  print('File not found! Creating REGISTRY.db...')
  conn = sqlite3.connect('REGISTRY.db')
  crsr = conn.cursor()
  crsr.execute("CREATE TABLE users (uid INTEGER PRIMARY KEY, duid TEXT, username TEXT, credits TEXT);")
  conn.commit()
  conn.close()
  os.system("sudo chmod 777 REGISTRY.db")
  print('Done!')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s'))
logger.addHandler(handler)

def client_run():
  client.loop.create_task(background_loop())
  client.run(TOKEN)

def logwrite(msg):
  with open('messages.log', 'a+') as f:
    f.write(msg + '\n')
  f.close()

async def background_loop():
  await client.wait_until_ready()
  while not client.is_closed:
    print("Booted Up @ " + time.ctime())
    logwrite("Booted Up @ " + time.ctime())
    await asyncio.sleep(3600)

@client.event
async def on_ready():
  print('--------------------------------------------------------------------------------------')
  print('Server Connect Link:')
  print('https://discordapp.com/api/oauth2/authorize?scope=bot&client_id=' + str(client.user.id))
  print('--------------------------------------------------------------------------------------')
  print('Logged in as:')
  print(client.user.name)
  print("or")
  print(client.user)
  print("UID:")
  print(client.user.id)
  print('---------------------------------------------')
  print("LIVE CHAT LOG - See MESSAGES.log For History")
  print("---------------------------------------------")
  await client.change_presence(activity=discord.Game("Running..."), status=discord.Status.online)

@client.event
async def on_member_join(member):
  print("Member:", member, "joined!")
  logwrite("Member: " + str(member) + " joined!")

@client.event
async def on_member_remove(member):
  print("Member:", member, "removed!")
  logwrite("Member: " + str(member) + " removed!")

@client.event
async def on_guild_role_create(role):
  print("Role:", role, "was created!")
  logwrite("Role: " + str(role) + " was created!")

@client.event
async def on_guild_role_delete(role):
  print("Role:", role, "was deleted!")
  logwrite("Role: " + str(role) + " was deleted!")

@client.event
async def on_guild_channel_create(channel):
  print("Channel:", channel, "was created!")
  logwrite("Channel: " + str(channel) + " was created!")

@client.event
async def on_guild_channel_delete(channel):
  print("Channel:", channel, "was deleted!")
  logwrite("Channel: " + str(channel) + " was deleted!")

@client.event
async def on_guild_channel_update(before, after):
  print("Channel Updated:", after)
  logwrite("Channel Updated: " + str(after))

@client.event
async def on_message(message):
  conn = sqlite3.connect('REGISTRY.db')
  crsr = conn.cursor()
  crsr.execute("SELECT username FROM users;")
  users = str(crsr.fetchall()).strip("''[](),")
  userslist = users.split( )
  crsr.execute("SELECT uid FROM users;")
  uids = str(crsr.fetchall()).strip("''[](),")
  uidslist = uids.split( )
  newuid = len(uidslist)
  if message.author == client.user:
    return
  channel = message.channel
  credits = len(str(message.content).split( ))
  if str(message.author) in userslist:
    pass
  else:
    crsr.execute("INSERT INTO users VALUES (?, ?, ?, ?);", (str(newuid), str(message.author.id), str(message.author), str(credits)))
    conn.commit()
    print("User: " + str(message.author) + " added to REGISTRY.db")
    await message.author.send("You've been added to 'REGISTRY.db' by E-Trader!")
    crsr.execute("SELECT * FROM users WHERE username = '" + str(message.author) + "';")
    info = crsr.fetchall()
    convert = [list(ele) for ele in info]
    final = sum(convert, [])
    await message.author.send("\nUID: " + str(final[0]) + "\nDiscord UID: " + str(final[1]) + "\nUsername: " + str(final[2]) + "\nCredits: " + str(final[3]))
  crsr.execute("SELECT credits FROM users WHERE username = '" + str(message.author) + "';")
  wallet = str(crsr.fetchall()).strip("''[](),")
  calc = int(credits) + int(wallet)
  crsr.execute("UPDATE users SET credits = " + str(calc) + " WHERE username = '" + str(message.author) + "';")
  conn.commit()
  updated_wallet = str(crsr.fetchall()).strip("''[](),")
  print(message.author, "said:", message.content, "-- +" + str(credits) + " added -- Time:", time.ctime())
  logwrite(str(message.author) + " said: " + str(message.content) + "-- Time: " + time.ctime())

  if message.content == "/info":
    crsr.execute("SELECT * FROM users WHERE username = '" + str(message.author) + "';")
    info = crsr.fetchall()
    convert = [list(ele) for ele in info]
    final = sum(convert, [])
    await message.author.send("\nUID: " + str(final[0]) + "\nDiscord UID: " + str(final[1]) + "\nUsername: " + str(final[2]) + "\nCredits: " + str(final[3]))

  if message.content == "/wallet":
    crsr.execute("SELECT credits FROM users WHERE username = '" + str(message.author) + "';")
    wallet = crsr.fetchall()
    convert = [list(ele) for ele in wallet]
    final = sum(convert, [])
    await message.author.send("Credits Stored: " + str(final[0]))

  if message.content == "/send":
    crsr.execute("SELECT username FROM users;")
    users = str(crsr.fetchall()).strip("''[](),")
    userslist = users.split( )
    await message.author.send("Select user to send to: ")
    for i in range(0, len(userslist)):
      await message.author.send("[" + str(i) + "] " + str(userslist[i]))
    await message.author.send("Type /user #")
    def check(msg):
      return msg.content.startswith('/user')
    message = await client.wait_for('message', check=check)
    name = message.content[len('/user'):].strip()
    await message.author.send("How much do you want to send?: ")
    await message.author.send("Type /amount #")
    def check(msg):
      return msg.content.startswith('/amount')
    message = await client.wait_for('message', check=check)
    amount = message.content[len('/amount'):].strip()
    await message.author.send("Donating " + str(amount) + " credits to " + str(userslist[int(name)]))
    crsr.execute("SELECT credits FROM users WHERE username = '" + str(message.author) + "';")
    creds = str(crsr.fetchall()).strip("''()[],")
    if int(creds) < int(amount):
      await message.author.send("Insufficient Funds!")
    else:
      await message.author.send("Sending " + str(amount) + " credits...")
      calc = int(creds) - int(amount)
      crsr.execute("UPDATE users SET credits = " + str(calc) + " WHERE username = '" + str(message.author) + "';")
      conn.commit()
      crsr.execute("SELECT credits FROM users WHERE username = '" + str(userslist[int(name)]) + "';")
      doneecreds = str(crsr.fetchall()).strip("'[](),")
      calc = int(doneecreds) + int(amount)
      crsr.execute("UPDATE users SET credits = " + str(calc) + " WHERE username = '" + str(userslist[int(name)]) + "';")
      conn.commit()
      crsr.execute("SELECT credits FROM users WHERE username = '" + str(message.author) + "';")
      newcreds = str(crsr.fetchall()).strip("'[](),")
      await message.author.send("Current Holdings: " + str(newcreds) + " credits")
      crsr.execute("SELECT duid FROM users WHERE username = '" + str(userslist[int(name)]) + "';")
      donee_duid = str(crsr.fetchall()).strip("'[](),")
      donee = client.get_user(int(donee_duid))
      await donee.send(str(message.author) + " sent you " + str(amount) + " credits!")

  if message.content == "/request":
    crsr.execute("SELECT username FROM users;")
    users = str(crsr.fetchall()).strip("''[](),")
    userslist = users.split( )
    await message.author.send("Select user to request from: ")
    for i in range(0, len(userslist)):
      await message.author.send("[" + str(i) + "] " + str(userslist[i]))
    await message.author.send("Type /user #")
    def check(msg):
      return msg.content.startswith('/user')
    message = await client.wait_for('message', check=check)
    name = message.content[len('/user'):].strip()
    await message.author.send("How much do you want to request?: ")
    await message.author.send("Type /amount #")
    def check(msg):
      return msg.content.startswith('/amount')
    message = await client.wait_for('message', check=check)
    amount = message.content[len('/amount'):].strip()
    await message.author.send("Requesting " + str(amount) + " credits from " + str(userslist[int(name)]))
    crsr.execute("SELECT duid FROM users WHERE username = '" + str(message.author) + "';")
    requestee_duid = str(crsr.fetchall()).strip("'[](),")
    requestee = client.get_user(int(requestee_duid))
    crsr.execute("SELECT duid FROM users WHERE username = '" + str(userslist[int(name)]) + "';")
    request_duid = str(crsr.fetchall()).strip("'[](),")
    request = client.get_user(int(request_duid))
    await request.send(str(message.author) + " is requesting " + str(amount) + " credits from you...")
    await request.send("Do you want to accept?[y/N]: ")
    await request.send("Type /op Y or N")
    def check(msg):
      return msg.content.startswith('/op')
    message = await client.wait_for('message', check=check)
    op = message.content[len('/op'):].strip()
    if op.lower() == "y":
      crsr.execute("SELECT credits FROM users WHERE username = '" + str(request) + "';")
      request_credits = str(crsr.fetchall()).strip("'[](),")
      if float(request_credits) < float(amount):
        await requestee.send(str(request) + " didn't have sufficient funds to transfer...")
        await request.send("Insufficient funds to transfer...")
      else:
        crsr.execute("SELECT credits FROM users WHERE username = '" + str(requestee) + "';")
        requestee_credits = str(crsr.fetchall()).strip("'[](),")
        calc = int(requestee_credits) + int(amount)
        crsr.execute("UPDATE users SET credits = " + str(calc) + " WHERE username = '" + str(requestee) + "';")
        conn.commit()
        calc = int(request_credits) - int(amount)
        crsr.execute("UPDATE users SET credits = " + str(calc) + " WHERE username = '" + str(request) + "';")
        conn.commit()
        await requestee.send(str(request) + " sent " + str(amount) + " credits to you!")
        await request.send("Sent " + str(amount) + " credits to " + str(requestee))
    else:
      await requestee.send(str(request) + " denied your request...")
      await request.send("You denied a request from " + str(requestee) + "...")

  if message.content == "/help":
    await channel.send("====Commands====\n/info           Displays user information\n/wallet       Displays credits user has in accounts\n/send          Creates dialogue for sending credits to another user\n/request     Creates dialogue for requesting credits from another user\n/dm             Tests DM feature with a user\n/ulog            Displays Update Log for Discord-ETrader\n/whoami      Returns username\n/ping            Pings ETrader for run checks")

  if message.content == "/dm":
    await channel.send("Creating DM with " + str(message.author))
    await message.author.send('*DM started with ' + str(message.author) + '*')
    await message.author.send('Hello!')

  if message.content == "/ulog":
    try:
      f = open("update_log.txt","r")
      if f.mode == 'r':
        contents = f.read()
        await channel.send(contents)
    finally:
      f.close()

  if message.content == "/whoami":
    await channel.send(message.author)

  if message.content == "/ping":
    await channel.send("Ping Received...E-Trader is up and running!")

client_run()
