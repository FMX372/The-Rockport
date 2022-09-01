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
from easy_pil import *
from nextcord import ActivityType, File
from nextcord.ext import commands
from PIL import Image, ImageDraw, ImageSequence, ImageFont

#Cosos del bot
intents = nextcord.Intents.all()
client = commands.Bot(command_prefix='>', intents=intents)
client.remove_command('help')

#Variables - Constantes
TOKEN = 'TOKEN DEL BOT ;D'

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
 rol = nextcord.utils.get(usuario.guild.roles, id=ID DEL AUTOROL)
 await usuario.add_roles(rol)

#Mandar el mensaje en el canal del sistema
 canal = usuario.guild.system_channel
#Imagenes de bienvenida (Lo puedo poner en un archivo a parte, ¿pero ves que me importe? xdddd)
 imagenesfondo = ["GIFS QUE QUIERES QUE SALGAN DE FONDO"]

 #El lío que hay que hacer para la imagen de bienvenida siendo Gif
 im = Image.open(random.choice(imagenesfondo))
 frames = []
 for frame in ImageSequence.Iterator(im):
  frame = frame.convert('RGBA')


  dibujar = ImageDraw.Draw(frame)

  with Image.open("avatar.png") as perfils:
    perfilchiko = perfils.resize((160, 160))

  Upheaval = ImageFont.truetype(font='UpheavalPro.ttf', size=30)
  SUpheaval = ImageFont.truetype(font='UpheavalPro.ttf', size=25)

  dibujar.text((15, 189), f"{usuario.name}",color="white", font=Upheaval, align="left")
  dibujar.text((15, 225), f"#{usuario.discriminator}",color="white", font=SUpheaval, align="left")
  dibujar.text((15, 274), f"{usuario.guild.name}",color="white", font=Upheaval, align="right")
  perfilchiko.paste(frame, (15, 15), frame)

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
@client.command(name="mute-img")
async def desc(ctx, *, foto = "sin foto"):

  #Quitar la descripción
  if foto == "quitar":
            if (os.path.exists(os.path.join(os.getcwd(), "fotos", str('fotomute') + ".foto.txt"))):
                os.remove(os.path.join(os.getcwd(), "descripciones", str('fotomute') + ".foto.txt"))

                await ctx.send(f"Se ha quitado la imagen de los mutes")
            #Si no tiene una    
            else:
                await ctx.send(f"No puedo quitar la imagen, no hay")

  if foto.startswith("https://"):
    with open(os.path.join(os.getcwd(), "imgs", str('fotomute') + ".foto.txt"), "w") as descriptionFile:
      descriptionFile.write(foto)

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
  
  embed = nextcord.Embed(title="**Miembro expulsado**", color=0xFF7000)
  embed.set_thumbnail(url=usuario.avatar.url)
  embed.add_field(name='Afectado:',value=usuario.display_name,inline=False)
  embed.add_field(name='Razón proporcionada:',value=razon,inline=False)
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
  if nextcord.errors.Forbidden:
    embederror = nextcord.Embed(title="**Error**", description= "No puedo banear a un admin del servidor <:mkultra:1012546239780376676>", color=0xEC0D0D)
    return await ctx.send(embed=embederror)

  #Si no lo es, al carré
  embed = nextcord.Embed(title="**Miembro baneado**", color=0xEC0D0D)
  embed.set_thumbnail(url=usuario.avatar.url)
  embed.add_field(name='Afectado:',value=usuario.display_name,inline=False)
  embed.add_field(name='Razón proporcionada:',value=razon,inline=False)
  embed.set_footer(text=f'Acción realizada por: {ctx.author}',icon_url=ctx.author.avatar.url)
  
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
 descriptionPathDesc = os.path.join(os.getcwd(), "imgs", str('fotomute') + ".foto.txt")

 if (os.path.exists(descriptionPathDesc)):
    with open(descriptionPathDesc) as descriptionFile:
     url = descriptionFile.read()
 else:
     url = "sin banner"

 if url != "sin banner":
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

  canalxp = client.get_channel(ID DEL CANAL DE LEVEL UP)

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
    xp += random.randint(2, 5) 
    await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (xp, autor.id, guild.id))

    #Lo que hace cada nivel 100% custom, es una excusa para dejarlo así de feo, que asco
    if nivel == 0 and xp >= 50:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (1, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **1**, sigue así :D')

    elif nivel == 1 and xp >= 100:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (2, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **2**, sigue así :D')

    elif nivel == 2 and xp >= 150:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (3, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **3**, sigue así :D')

    elif nivel == 3 and xp >= 200:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (4, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **4**, sigue así :D')

    elif nivel == 4 and xp >= 250:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (5, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **5**, sigue así :D')

    elif nivel == 5 and xp >= 300:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (6, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **6**, sigue así :D')

    elif nivel == 6 and xp >= 350:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (7, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **7**, sigue así :D')

    elif nivel == 7 and xp >= 400:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (8, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **8**, sigue así :D')

    elif nivel == 8 and xp >= 450:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (9, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **9**, sigue así :D')

    elif nivel == 9 and xp >= 500:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (10, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **10**, sigue así :D')

    elif nivel == 10 and xp >= 550:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (11, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **11**, sigue así :D')

    elif nivel == 11 and xp >= 600:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (12, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **12**, sigue así :D')

    elif nivel == 12 and xp >= 650:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (13, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **13**, sigue así :D')

  #Hacer los cambios a la Database
  await client.db.commit()
  #Esto permite los comandos
  await client.process_commands(message)





#Ver el nivel
@client.command(name='nivel')
async def nivel(ctx, usuario:nextcord.Member=None):
  if usuario == None:
    usuario = ctx.author

  async with client.db.cursor() as cursor:
    await cursor.execute('SELECT xp FROM nivel WHERE usuario = ? AND guild = ?', (usuario.id, ctx.guild.id))
    xp = await cursor.fetchone()

    await cursor.execute('SELECT nivel FROM nivel WHERE usuario = ? AND guild = ?', (usuario.id, ctx.guild.id))
    nivel = await cursor.fetchone()

    if not xp or not nivel:
      await cursor.execute('INSERT INTO nivel (nivel, xp, usuario, guild) VALUES (?, ?, ?, ?)', (0, 0, usuario.id, ctx.guild.id))

    try:
      xp = xp[0]
      nivel = nivel[0]
    except TypeError:
      xp = 0
      nivel = 0
    
    #XP necesaria para cada nivel
    if nivel == 0:
      nextxp = 50
    elif nivel == 1:
      nextxp = 100
    elif nivel == 2:
      nextxp = 150
    elif nivel == 3:
      nextxp = 200
    elif nivel == 4:
      nextxp = 250
    elif nivel == 5:
      nextxp = 300
    elif nivel == 6:
      nextxp = 350
    elif nivel == 7:
      nextxp = 400
    elif nivel == 8:
      nextxp = 450
    elif nivel == 9:
      nextxp = 500
    elif nivel == 10:
      nextxp = 550
    elif nivel == 11:
      nextxp = 600
    elif nivel == 12:
      nextxp = 650

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
