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
import aiohttp
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
  await asyncio.sleep(1)
  async with client.db.cursor() as cursor:
    await cursor.execute('CREATE TABLE IF NOT EXISTS nivel (nivel INTEGER, xp INTEGER, usuario INTEGER, guild INTEGER)')
  print('Conexión con la base de datos')
  await asyncio.sleep(1)

   #Que se muestra en la consola al iniciar el bot
  print("THE ROCKPORT está en línea")















#Bienvenidas--------------------------------------------------------------------------
@client.event
async def on_member_join(usuario):

#Autorol
 rolMiembros = nextcord.utils.get(usuario.guild.roles, id=1012189850167943209)
 rolNiveles = nextcord.utils.get(usuario.guild.roles, id=1017258189739270224)
 rolEco = nextcord.utils.get(usuario.guild.roles, id=1017258625468743701)
 rolAuto = nextcord.utils.get(usuario.guild.roles, id=1017258787192717392)
 await usuario.add_roles(rolMiembros, rolNiveles, rolEco, rolAuto)

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

  if message.content.startswith('>'):
    await client.process_commands(message)
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

       #Test

    xpNivel = nivel
    nivelAñadir = xpNivel + 1
    xpMax = (xpNivel * 500) + 500

    if nivel == xpNivel and xp >= xpMax:
      await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (nivelAñadir, autor.id, guild.id))
      await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, autor.id, guild.id))
      await canalxp.send(f'{autor.mention} ha llegado al nivel **{nivelAñadir}**, sigue así :D')


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
    nextxp = (nivel * 500) + 500
    

    #Hacer la imagen del comando de rango
    canvas = Canvas((1500, 500), color = 'black')
    fondo = Editor('NIVEL.png')

    try:
      pfp = await load_image_async(str(usuario.avatar.url))
    except:
      pfp = await load_image_async('https://external-preview.redd.it/4PE-nlL_PdMD5PrFNLnjurHQ1QKPnCvg368LTDnfM-M.png?auto=webp&s=ff4c3fbc1cce1a1856cff36b5d2a40a6d02cc1c3')
    cargarpfp = Editor(pfp).resize((380, 380)).circle_image()

    poppins = ImageFont.truetype("Uni_Sans_Heavy.otf", 90)
    spoppins = ImageFont.truetype("Uni_Sans_Heavy.otf", 60)

    #Añadir foto si hay
    rankPathimg = os.path.join(os.getcwd(), "rankCards", str(usuario.id) + ".png")

    if (os.path.exists(rankPathimg)):
      fondoCustom = Image.open(rankPathimg)
      fondoCustomEditor = Editor(fondoCustom).resize((1500, 500))
      fondo.paste(fondoCustomEditor, (0, 0))
    else:
      fondoCustom = Image.open('NIVEL.png')
      fondo.paste(fondoCustom, (0, 0))

    fondo.paste(cargarpfp, (65, 60))
    fondo.text((487, 114), usuario.display_name, font=poppins, color='#ffffff')
    fondo.text((1480, 440), f'Nivel {nivel}', font=spoppins, color='#ffffff', align='right')
    fondo.text((487, 340), f'{xp} / {nextxp}xp', font=spoppins, color='#ffffff')
    fondo.rectangle((487, 230), width=905, height=87, color='#ffffff', radius=60)
    fondo.bar((487, 230), max_width=905, height=87, percentage=((xp / nextxp) * 100), color=f'{usuario.color}', radius=60)



    fotorango = nextcord.File(fp=fondo.image_bytes, filename='nivelación.png')
    await ctx.send(file=fotorango)


#Foto custom de nivel
@client.command(name='nivel-img')
async def nivelimg(ctx, quitar=''):

  #Si no tiene el nivel 30, no deja usarlo
  lvl30 = nextcord.utils.get(ctx.guild.roles, id=1014229437304287253)
  if not lvl30 in ctx.author.roles:
    await ctx.reply('Necesitas tener el rol <@&1014229437304287253> para usar esta función <:niggawhaat:1015035386319343616>')
    return

  if quitar == "quitar":
    if (os.path.exists(os.path.join(os.getcwd(), "rankCards", f'{ctx.author.id}.png'))):

      os.remove(os.path.join(os.getcwd(), "rankCards", f'{ctx.author.id}.png'))
      await ctx.send(f"Se ha quitado el fondo de tu carta de nivel")
    #Si no tiene una    
    else:
      await ctx.send(f"No puedo quitar la imagen, no hay")



  if valid_image_url(ctx.message.attachments[0].url):
    await download_image(ctx.message.attachments[0].url, "rankCards", f'{ctx.author.id}.png')

    await ctx.send('¡He actualizado tu fondo de la carta de nivel! <:Niceguy:1015068562072817734>')


def valid_image_url(url: str):
    image_extensions = ['png', 'jpg', 'jpeg']
    for image_extension in image_extensions:
        if url.endswith('.' + image_extension):
            return True
    return False


async def download_image(url: str, images_path: str, image_name: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(os.path.join(images_path, image_name), "wb") as f:
                    f.write(await resp.read())





#Cuando alguien se va, resetear los niveles.
@client.event
async def on_member_remove(member):

  guildid = 1012177305449271386
  async with client.db.cursor() as cursor:
    await cursor.execute('UPDATE nivel SET nivel = ? WHERE usuario = ? AND guild = ?', (0, member.id, guildid))
    await cursor.execute('UPDATE nivel SET xp = ? WHERE usuario = ? AND guild = ?', (0, member.id, guildid))

  await client.db.commit()












#Economía------------------------------------------------------------------------------------------------

#BALANCE
@client.command(name='balance')
async def balance(ctx, usuario:nextcord.Member=None):

  if usuario == None:
    usuario = ctx.author

  dineroPathEco = os.path.join(os.getcwd(), "eco", str(usuario.id) + ".eco.txt")

  if (os.path.exists(dineroPathEco)):
    with open(dineroPathEco) as ecoFile:
      balance = ecoFile.read()
  else:
    await ctx.reply('Parece que este usuario no tiene nada en el banco <a:emoji_51:1015420747688198236>')
    return
  
  embed = nextcord.Embed(title=f'Cuenta de {usuario.display_name}', color=usuario.color)
  embed.add_field(name='Balance:', value=f'> {balance} <a:MonedaOro:1020266130658566175>')
  await ctx.send(embed=embed)





#INGRESAR
@client.command(name='ingresar')
@commands.has_permissions(manage_roles=True)
async def ingresar(ctx, usuario:nextcord.Member=None, cantidad = '0'):

  if usuario == None:
    await ctx.reply('No has indicado a ningún usuario para la operación <:Nimodo:1015068273123012678>')
    return

  if cantidad == '0':
    await ctx.reply('No has dado una cifra que ingresar <:emoji_39:1015420289460490300>')
    return

  try:
    int(cantidad)
  except:
    await ctx.reply(f'¿Es {cantidad} un número? <a:emoji_52:1015420784681963652>')
    return

  dineroPathEco = os.path.join(os.getcwd(), "eco", str(usuario.id) + ".eco.txt")

  if (os.path.exists(dineroPathEco)):
    with open(dineroPathEco) as ecoFile:
      balance = ecoFile.read()
      dineroFinalInt = int(balance) + int(cantidad)
      dineroFinal = str(dineroFinalInt)
    with open(os.path.join(os.getcwd(), "eco", str(usuario.id) + ".eco.txt"), "w") as ecoFile:
      ecoFile.write(dineroFinal)
  else:
    with open(os.path.join(os.getcwd(), "eco", str(usuario.id) + ".eco.txt"), "w") as ecoFile:
      dineroFinal = str(cantidad)
      ecoFile.write(dineroFinal)

  embed = nextcord.Embed(title='¡Ingreso realizado con éxito!', description=f'Se han ingresado **{str(cantidad)}** <a:MonedaOro:1020266130658566175> a **{usuario.display_name}**', color=0xffd20a)
  await ctx.send(embed=embed)



#RETIRAR
@client.command(name='retirar')
@commands.has_permissions(manage_roles=True)
async def retirar(ctx, usuario:nextcord.Member=None, cantidad = '0'):

  if usuario == None:
    await ctx.reply('No has indicado a ningún usuario para la operación <:Nimodo:1015068273123012678>')
    return

  if cantidad == '0':
    await ctx.reply('No has dado una cifra que retirar <:emoji_39:1015420289460490300>')
    return

  try:
    int(cantidad)
  except:
    await ctx.reply(f'¿Es {cantidad} un número? <a:emoji_52:1015420784681963652>')
    return

  dineroPathEco = os.path.join(os.getcwd(), "eco", str(usuario.id) + ".eco.txt")

  if (os.path.exists(dineroPathEco)):
    with open(dineroPathEco) as ecoFile:
      balance = ecoFile.read()
      if int(cantidad) > int(balance):
        dineroFinal = ('0')
      else:
        dineroFinalInt = int(balance) - int(cantidad)
        dineroFinal = str(dineroFinalInt)
    with open(os.path.join(os.getcwd(), "eco", str(usuario.id) + ".eco.txt"), "w") as ecoFile:
      ecoFile.write(dineroFinal)

  else:
    await ctx.reply('Este usuario no tiene nada en el banco <:cry:1015035821742632990>')
    return
  embed = nextcord.Embed(title='¡Retiro realizado con éxito!', description=f'Se le han retirado **{str(cantidad)}** <a:MonedaOro:1020266130658566175> a **{usuario.display_name}**', color=0xf2163e)
  await ctx.send(embed=embed)





#RUN
client.run(TOKEN)
