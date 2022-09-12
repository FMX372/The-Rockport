#AVISO esto no está organizado, no me responsabilizo del derrame cerebral que te pueda dar viendo este código
from distutils.log import error
from email import message
import os
from webbrowser import get
import nextcord
import PIL
import easy_pil
import io
import random
import asyncio
import datetime
import humanfriendly
import aiosqlite
import requests
from io import BytesIO
from easy_pil import *
from nextcord import ActivityType, File
from nextcord.ext import commands
from PIL import Image, ImageDraw, ImageSequence, ImageFont

#Cosos del bot
intents = nextcord.Intents.all()
client = commands.Bot(command_prefix='>', intents=intents)
client.remove_command('help')

#Variables - Constantes
TOKEN = 'TOKEN'

#On Start
@client.event
async def on_ready():
  #Actividad custom (pijadas)
 await client.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="PornHub"))
   #Conectar a la base de datos
 setattr(client, 'db', await aiosqlite.connect('niveles.db'))
 await asyncio.sleep(3)
 async with client.db.cursor() as cursor:
  await cursor.execute('CREATE TABLE IF NOT EXISTS nivel (nivel INTEGER, xp INTEGER, usuario INTEGER, guild INTEGER)')
   #Que se muestra en la consola al iniciar el bot
 print("THE ROCKPORT está en línea")















#Bienvenidas--------------------------------------------------------------------------
@client.event
async def on_member_join(usuario):

#Autorol
 rol = nextcord.utils.get(usuario.guild.roles, id=1012189850167943209)
 await usuario.add_roles(rol)

#Mandar el mensaje en el canal del sistema
 canal = usuario.guild.system_channel

 #El lío que hay que hacer para la imagen de bienvenida siendo Gif
 im = Image.open("welcums/bienvenida.gif")
 frames = []
 for frame in ImageSequence.Iterator(im):
  frame = frame.convert('RGBA')

  dibujar = ImageDraw.Draw(frame)

  Upheaval = ImageFont.truetype(font='UpheavalPro.ttf', size=36)
  SUpheaval = ImageFont.truetype(font='UpheavalPro.ttf', size=30)

  dibujar.text((18, 232), f"{usuario.name}",color="white", font=Upheaval, align="left")
  dibujar.text((15, 267), f"#{usuario.discriminator}",color="white", font=SUpheaval, align="left")

  b = io.BytesIO()
  frame.save(b, format="GIF")
  frame = Image.open(b)
  frames.append(frame)
 frames[0].save('out.gif', save_all=True, append_images=frames[1:])


 #Mandar el mensaje de bienvenida
 await canal.send(f"¡Bienvenid@ {usuario.mention}, espero que lo pases bien!")
 #Mandar la foto de bienvenida
 foto = nextcord.File('out.gif')
 await canal.send(file=foto)




























#Moderación--------------------------------------------------------------------------

#Imagenes custom de moderación
@client.command(name="silenciar-img")
async def muteimg(ctx, *, foto = "sin foto"):

  #Quitar la descripción
  if foto == "quitar":
            if (os.path.exists(os.path.join(os.getcwd(), "fotos", str('fotomute') + ".foto.txt"))):
                os.remove(os.path.join(os.getcwd(), "fotos", str('fotomute') + ".foto.txt"))

                await ctx.send(f"Se ha quitado la imagen de los mutes")
            #Si no tiene una    
            else:
                await ctx.send(f"No puedo quitar la imagen, no hay")

  if foto.startswith("https://"):
    with open(os.path.join(os.getcwd(), "fotos", str('fotomute') + ".foto.txt"), "w") as muteFile:
      muteFile.write(foto)
    await ctx.send("¡Ahora enseñaré esa imagen al silenciar a alguien!")

  else:
    await ctx.send("No parece que eso sea un link válido")



@client.command(name="kick-img")
async def kickimg(ctx, *, foto = "sin foto"):

  #Quitar la descripción
  if foto == "quitar":
            if (os.path.exists(os.path.join(os.getcwd(), "fotos", str('fotokick') + ".foto.txt"))):
                os.remove(os.path.join(os.getcwd(), "fotos", str('fotokick') + ".foto.txt"))

                await ctx.send(f"Se ha quitado la imagen de los kicks")
            #Si no tiene una    
            else:
                await ctx.send(f"No puedo quitar la imagen, no hay")

  if foto.startswith("https://"):
    with open(os.path.join(os.getcwd(), "fotos", str('fotokick') + ".foto.txt"), "w") as kickFile:
      kickFile.write(foto)
    await ctx.send("¡Ahora enseñaré esa imagen al echar a alguien!")

  else:
    await ctx.send("No parece que eso sea un link válido")



@client.command(name="ban-img")
async def banimg(ctx, *, foto = "sin foto"):

  #Quitar la descripción
  if foto == "quitar":
            if (os.path.exists(os.path.join(os.getcwd(), "fotos", str('fotoban') + ".foto.txt"))):
                os.remove(os.path.join(os.getcwd(), "fotos", str('fotoban') + ".foto.txt"))

                await ctx.send(f"Se ha quitado la imagen de los bans")
            #Si no tiene una    
            else:
                await ctx.send(f"No puedo quitar la imagen, no hay")

  if foto.startswith("https://"):
    with open(os.path.join(os.getcwd(), "fotos", str('fotoban') + ".foto.txt"), "w") as banFile:
      banFile.write(foto)
    await ctx.send("¡Ahora enseñaré esa imagen al banear a alguien!")

  else:
    await ctx.send("No parece que eso sea un link válido")






  #---KICK---
@client.command(name="kick")
#Si tiene permiso para kickear
@commands.has_permissions(kick_members=True)
async def kick(ctx, usuario:nextcord.Member=None, *, razon="No se ha dado una razón"):

 #Si no menciona a nadie, error
  if usuario==None:
    embed = nextcord.Embed(title="Error", description="¡No has mencionado a nadie!", color=0xEC0D0D)
    return await ctx.send(embed=embed)
  
  roladmin = nextcord.utils.get(ctx.guild.roles, id=1012187870792007720)
  if roladmin in usuario.roles:
    embederror = nextcord.Embed(title="**Error**", description= "No puedo echar a un admin del servidor <:mkultra:1012546239780376676>", color=0xEC0D0D)
    return await ctx.send(embed=embederror)

  embed = nextcord.Embed(title="**Miembro expulsado**", color=0xFF7000)
  embed.set_thumbnail(url=usuario.avatar.url)
  embed.add_field(name='Afectado:',value=usuario.display_name,inline=False)
  embed.add_field(name='Razón proporcionada:',value=razon,inline=False)
   #Añadir foto si hay
  kickPathimg = os.path.join(os.getcwd(), "fotos", str('fotokick') + ".foto.txt")

  if (os.path.exists(kickPathimg)):
    with open(kickPathimg) as kickFile:
     url = kickFile.read()
  else:
     url = "sin foto"

  if url != "sin foto":
    embed.set_image(url=url)

  embed.set_footer(text=f'Acción realizada por: {ctx.author}', icon_url=ctx.author.avatar.url)
  
  #Echa al usuario
  await usuario.kick(reason=razon)
  #Mandar la notificación (Después de la acción, así si hay un error, no se mandará la notificación)
  await ctx.send(embed=embed)

@client.command(name="ban")
#Si tiene permiso para banear
@commands.has_permissions(ban_members=True)
async def ban(ctx, usuario:nextcord.Member=None, *, razon="No se ha dado una razón"):

 #Si no menciona a nadie, error
  if usuario==None:
    embed = nextcord.Embed(title="Error", description="¡No has mencionado a nadie!", color=0xEC0D0D)
    return await ctx.send(embed=embed)

  #Si el afectado es admin, dar error
  roladmin = nextcord.utils.get(ctx.guild.roles, id=1012187870792007720)
  if roladmin in usuario.roles:
    embederror = nextcord.Embed(title="**Error**", description= "No puedo banear a un admin del servidor <:mkultra:1012546239780376676>", color=0xEC0D0D)
    return await ctx.send(embed=embederror)

  #Si no lo es, al carré
  embed = nextcord.Embed(title="**Miembro baneado**", color=0xEC0D0D)
  embed.set_thumbnail(url=usuario.avatar.url)
  embed.add_field(name='Afectado:',value=usuario.display_name,inline=False)
  embed.add_field(name='Razón proporcionada:',value=razon,inline=False)
   #Añadir foto si hay
  banPathimg = os.path.join(os.getcwd(), "fotos", str('fotoban') + ".foto.txt")

  if (os.path.exists(banPathimg)):
    with open(banPathimg) as banFile:
     url = banFile.read()
  else:
     url = "sin foto"

  if url != "sin foto":
    embed.set_image(url=url)

  embed.set_footer(text=f'Acción realizada por: {ctx.author}', icon_url=ctx.author.avatar.url)
  
  #Banear al usuario
  await usuario.ban(reason=razon)
  #Mandar la notificación (Después de la acción, así si hay un error, no se mandará la notificación)
  await ctx.send(embed=embed)
  

  #---UNBAN---
@client.command(name="unban")
#Si tiene permiso para banear miembros
@commands.has_permissions(ban_members=True)
async def unban(ctx, usuario:nextcord.User=None, *, razon="No se ha dado una razón"):

 #Si no menciona a nadie, error
  if usuario == None:
    embed = nextcord.Embed(title="Error", description="¡No has proporcionado una ID!", color=0xEC0D0D)
    return await ctx.send(embed=embed)

  guild = ctx.guild
  
  embed = nextcord.Embed(title="**Miembro desbaneado**", color=0x2ECC71)
  embed.set_thumbnail(url=usuario.avatar.url)
  embed.add_field(name='Afectado:',value=usuario.display_name,inline=False)
  embed.add_field(name='Razón proporcionada:',value=razon,inline=False)
  embed.set_footer(text=f'Acción realizada por: {ctx.author}',icon_url=ctx.author.avatar.url)
  
  #Desbanea al usuario
  await guild.unban(user=usuario, reason=razon)
  #Mandar la notificación (Después de la acción, así si hay un error, no se mandará la notificación)
  await ctx.send(embed=embed)


  #---SILENCIAR A UN USUARIO---
@client.command(name="silenciar")
#Si tiene permiso para asignar roles
@commands.has_permissions(manage_roles=True)
async def silenciar(ctx, usuario:nextcord.Member, tiempoT, *, razon="No se ha dado una razón"):

 tiempo = humanfriendly.parse_timespan(tiempoT)

 #Si es admin el afectado error
 embed_muted = nextcord.Embed(title=f"¡Se ha silenciado a {usuario.name} por {tiempoT}!", color=0xEC0D0D)
 embed_muted.add_field(name="Razón proporcionada:", value=razon)
 embed_muted.set_thumbnail(url = usuario.avatar.url)
 #Añadir foto si hay
 mutePathimg = os.path.join(os.getcwd(), "fotos", str('fotomute') + ".foto.txt")

 if (os.path.exists(mutePathimg)):
    with open(mutePathimg) as muteFile:
     url = muteFile.read()
 else:
     url = "sin foto"

 if url != "sin foto":
    embed_muted.set_image(url=url)
    
 embed_muted.set_footer(text=f'Acción realizada por: {ctx.author}', icon_url=ctx.author.avatar.url) 
 await usuario.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=tiempo))
 await ctx.send(embed = embed_muted)


  #---DESILENCIAR A UN USUARIO---
@client.command(name="desilenciar")
#Si tiene permiso para asignar roles
@commands.has_permissions(manage_roles=True)
async def desilenciar(ctx, usuario:nextcord.Member=None):
 #Desilenciar
 #Si no menciona a nadie, error
 if usuario == None:
  embed = nextcord.Embed(title="Error", description="¡No has mencionado a nadie!", color=0xEC0D0D)
  return await ctx.send(embed=embed)

 else:
  await usuario.edit(timeout=None)
  embed_unmuted = nextcord.Embed(title=f"¡Se ha desilenciado a {usuario.name}!", color=0x80f75c)
  embed_unmuted.set_thumbnail(url = usuario.avatar.url)
  embed_unmuted.set_footer(text=f'Acción realizada por: {ctx.author}', icon_url=ctx.author.avatar.url) 
  await ctx.send(embed = embed_unmuted)

  #---PURGAR MENSAJES---
@client.command(name="purgar")
#Si tiene permiso para borrar mensajes
@commands.has_permissions(manage_messages=True)
async def purgar(ctx, cantidad=11):

  embed = nextcord.Embed(title=f"¡Se han purgado {cantidad} mensajes!", color=0xEC0D0D)
  embed.set_footer(text=f'Acción realizada por: {ctx.author}',icon_url=ctx.author.avatar.url)

  #Borrar los mensajes
  await ctx.channel.purge(limit=cantidad + 1)#El mensaje del comando se borra también, así si pones 10, se borran 10 mensajes y el comando
  #Notificación después de la acción
  await ctx.send(embed=embed)























#Nivelación-------------------------------------------------------------
#Sistema de niveles

@client.event
async def on_message(message):

  canalxp = client.get_channel(1012183828619595866)

  if message.author.bot:
    return

  autor = message.author
  guild = message.guild

  async with client.db.cursor() as cursor:
    await cursor.execute('SELECT xp FROM nivel WHERE usuario = ? AND guild = ?', (autor.id, guild.id,))
    xp = await cursor.fetchone()
    await cursor.execute('SELECT nivel FROM nivel WHERE usuario = ? AND guild = ?', (autor.id, guild.id,))
    nivel = await cursor.fetchone()

    if not xp or not nivel:
      await cursor.execute('INSERT INTO nivel (nivel, xp, usuario, guild) VALUES (?, ?, ?, ?)', (0, 0, autor.id, guild.id))
      await client.db.commit()

    try:
      xp = xp[0]
      nivel = nivel[0]
    except TypeError:
      xp = 0
      nivel = 0

    #Cuanta xp dar por mensaje
    xp += random.randint(10, 50) 
    await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (xp, autor.id, guild.id))

    #Lo que hace cada nivel 100% custom, es una excusa para dejarlo así de feo, que asco
    if nivel == 0 and xp >= 500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (1, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **1**, sigue así :D')

    elif nivel == 1 and xp >= 1000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (2, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **2**, sigue así :D')

    elif nivel == 2 and xp >= 1500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (3, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **3**, sigue así :D')

    elif nivel == 3 and xp >= 2000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (4, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **4**, sigue así :D')

    elif nivel == 4 and xp >= 2500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (5, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **5** y ahora tiene el rol <@&1014326564697165856>, sigue así :D')
      lvl1 = nextcord.utils.get(message.author.guild.roles, id=1014326564697165856)
      await message.author.add_roles(lvl1)

    elif nivel == 5 and xp >= 3000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (6, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **6**, sigue así :D')

    elif nivel == 6 and xp >= 3500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (7, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **7**, sigue así :D')

    elif nivel == 7 and xp >= 4000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (8, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **8**, sigue así :D')

    elif nivel == 8 and xp >= 4500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (9, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **9**, sigue así :D')

    elif nivel == 9 and xp >= 5000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (10, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **10** y ahora tiene el rol <@&1014230481950228511>, sigue así :D')
      lvl2 = nextcord.utils.get(message.author.guild.roles, id=1014230481950228511)
      await message.author.add_roles(lvl2)

    elif nivel == 10 and xp >= 5500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (11, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **11**, sigue así :D')

    elif nivel == 11 and xp >= 6000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (12, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **12**, sigue así :D')

    elif nivel == 12 and xp >= 6500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (13, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **13**, sigue así :D')

    elif nivel == 13 and xp >= 7000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (14, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **14**, sigue así :D')

    elif nivel == 14 and xp >= 7500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (15, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **15**, sigue así :D')

    elif nivel == 15 and xp >= 8000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (16, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **16**, sigue así :D')

    elif nivel == 16 and xp >= 8500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (17, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **17**, sigue así :D')

    elif nivel == 17 and xp >= 9000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (18, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **18**, sigue así :D')

    elif nivel == 18 and xp >= 9500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (19, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **19**, sigue así :D')

    elif nivel == 19 and xp >= 10000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (20, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **20** y ahora tiene el rol <@&1014231355753762816>, sigue así :D')
      lvl3 = nextcord.utils.get(message.author.guild.roles, id=1014231355753762816)
      await message.author.add_roles(lvl3)

    elif nivel == 20 and xp >= 10500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (21, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **21**, sigue así :D')

    elif nivel == 21 and xp >= 11000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (22, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **22**, sigue así :D')

    elif nivel == 22 and xp >= 11500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (23, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **23**, sigue así :D')

    elif nivel == 23 and xp >= 12000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (24, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **24**, sigue así :D')

    elif nivel == 24 and xp >= 12500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (25, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **25**, sigue así :D')

    elif nivel == 25 and xp >= 13000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (26, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **26**, sigue así :D')

    elif nivel == 26 and xp >= 13500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (27, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **27**, sigue así :D')

    elif nivel == 27 and xp >= 14000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (28, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **28**, sigue así :D')

    elif nivel == 28 and xp >= 14500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (29, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **29**, sigue así :D')

    elif nivel == 29 and xp >= 15000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (30, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **30** y ahora tiene el rol <@&1014229437304287253>, sigue así :D')
      lvl4 = nextcord.utils.get(message.author.guild.roles, id=1014229437304287253)
      await message.author.add_roles(lvl4)

    elif nivel == 30 and xp >= 15500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (31, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **31**, sigue así :D')

    elif nivel == 31 and xp >= 16000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (32, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **32**, sigue así :D')

    elif nivel == 32 and xp >= 16500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (33, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **33**, sigue así :D')

    elif nivel == 33 and xp >= 17000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (34, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **34**, sigue así :D')

    elif nivel == 34 and xp >= 17500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (35, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **35**, sigue así :D')

    elif nivel == 35 and xp >= 18000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (36, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **36**, sigue así :D')

    elif nivel == 36 and xp >= 18500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (37, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **37**, sigue así :D')

    elif nivel == 37 and xp >= 19000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (38, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **38**, sigue así :D')

    elif nivel == 38 and xp >= 19500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (39, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **39**, sigue así :D')

    elif nivel == 39 and xp >= 20000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (40, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **40** y ahora tiene el rol <@&1014229305963855902>, sigue así :D')
      lvl5 = nextcord.utils.get(message.author.guild.roles, id=1014229305963855902)
      await message.author.add_roles(lvl5)

    elif nivel == 40 and xp >= 20500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (41, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **41**, sigue así :D')

    elif nivel == 41 and xp >= 21000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (42, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **42**, sigue así :D')

    elif nivel == 42 and xp >= 21500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (43, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **43**, sigue así :D')

    elif nivel == 43 and xp >= 22000:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (44, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **44**, sigue así :D')

    elif nivel == 44 and xp >= 22500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (45, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **45**, sigue así :D')


  #Hacer los cambios a la Database
  await client.db.commit()
  #Esto permite los comandos
  await client.process_commands(message)





#Ver el nivel
@client.command(name='nivel')
async def nivel(ctx, usuario:nextcord.Member=None):
  if usuario == None:
    usuario = ctx.author
  print(usuario)
  async with client.db.cursor() as cursor:
    await cursor.execute('SELECT xp FROM nivel WHERE usuario = ? AND guild = ?', (usuario.id, ctx.guild.id))
    xp = await cursor.fetchone()
    print(xp)

    await cursor.execute('SELECT nivel FROM nivel WHERE usuario = ? AND guild = ?', (usuario.id, ctx.guild.id))
    nivel = await cursor.fetchone()
    print(nivel)

    if not xp or not nivel:
      await cursor.execute('INSERT INTO nivel (nivel, xp, usuario, guild) VALUES (?, ?, ?, ?)', (0, 0, usuario.id, ctx.guild.id))


    try:
      xp = xp[0]
      nivel = nivel[0]
    except TypeError:
      xp = 0
      nivel = 0

    print(xp)
    print(nivel)
    
    #XP necesaria para cada nivel
    if nivel == 0:
      nextxp = 500
    elif nivel == 1:
      nextxp = 1000
    elif nivel == 2:
      nextxp = 1500
    elif nivel == 3:
      nextxp = 2000
    elif nivel == 4:
      nextxp = 2500
    elif nivel == 5:
      nextxp = 3000
    elif nivel == 6:
      nextxp = 3500
    elif nivel == 7:
      nextxp = 4000
    elif nivel == 8:
      nextxp = 4500
    elif nivel == 9:
      nextxp = 5000
    elif nivel == 10:
      nextxp = 5500
    elif nivel == 11:
      nextxp = 6000
    elif nivel == 12:
      nextxp = 6500
    elif nivel == 13:
      nextxp = 7000
    elif nivel == 14:
      nextxp = 7500
    elif nivel == 15:
      nextxp = 8000
    elif nivel == 16:
      nextxp = 8500
    elif nivel == 17:
      nextxp = 9000
    elif nivel == 18:
      nextxp = 9500
    elif nivel == 19:
      nextxp = 10000
    elif nivel == 20:
      nextxp = 10500
    elif nivel == 21:
      nextxp = 11000
    elif nivel == 22:
      nextxp = 11500
    elif nivel == 23:
      nextxp = 12000
    elif nivel == 24:
      nextxp = 12500
    elif nivel == 25:
      nextxp = 13000
    elif nivel == 26:
      nextxp = 13500
    elif nivel == 27:
      nextxp = 14000
    elif nivel == 28:
      nextxp = 14500
    elif nivel == 29:
      nextxp = 15000
    elif nivel == 30:
      nextxp = 15500
    elif nivel == 31:
      nextxp = 16000
    elif nivel == 32:
      nextxp = 16500
    elif nivel == 33:
      nextxp = 17000
    elif nivel == 34:
      nextxp = 17500
    elif nivel == 35:
      nextxp = 18000
    elif nivel == 36:
      nextxp = 18500
    elif nivel == 37:
      nextxp = 19000
    elif nivel == 38:
      nextxp = 19500
    elif nivel == 39:
      nextxp = 20000
    elif nivel == 40:
      nextxp = 20500
    elif nivel == 41:
      nextxp = 21000
    elif nivel == 42:
      nextxp = 21500
    elif nivel == 43:
      nextxp = 22000
    elif nivel == 44:
      nextxp = 22500
    elif nivel == 45:
      nextxp = 23000
    elif nivel == 46:
      nextxp = 23500
    

    #Hacer la imagen del comando de rango
    fondo = Editor('NIVEL.png')
    pfp = await load_image_async(str(usuario.avatar.url))
    cargarpfp = Editor(pfp).resize((380, 380)).circle_image()

    poppins = ImageFont.truetype("Uni_Sans_Heavy.otf", 100, encoding="unic")
    spoppins = ImageFont.truetype("Uni_Sans_Heavy.otf", 60, encoding="unic")


    fondo.paste(cargarpfp, (65, 60))
    fondo.text((487, 114), usuario.display_name, font=poppins, color='#ffffff')
    fondo.text((1480, 440), f'Nivel {nivel}', font=spoppins, color='#ffffff', align='right')
    fondo.text((487, 340), f'{xp} / {nextxp}xp', font=spoppins, color='#ffffff')
    fondo.rectangle((487, 239), width=905, height=87, color='#ffffff', radius=30)
    fondo.bar((487, 239), max_width=905, height=87, percentage=((xp / nextxp) * 100), color='#dc4c56', radius=30) 



    fotorango = nextcord.File(fp=fondo.image_bytes, filename='nivelación.png')
    await ctx.send(file=fotorango)





#RUN
client.run(TOKEN)
