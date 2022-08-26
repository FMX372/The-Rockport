from distutils.log import error
import os
from webbrowser import get
import nextcord
import PIL
import io
import random
import datetime
import humanfriendly
from nextcord import ActivityType, File
from nextcord.ext import commands
from PIL import Image, ImageDraw, ImageSequence, ImageFont

#Cosos del bot
intents = nextcord.Intents.all()
client = commands.Bot(command_prefix='>', intents=intents)
client.remove_command('help')

#Variables - Constantes
TOKEN = 'TOKEN DEL BOT'

#On Start
@client.event
async def on_ready():
  #Actividad custom (pijadas)
 await client.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="PornHub"))
  #Que se muestra en la consola al iniciar el bot
 print("THE ROCKPORT está en línea")    


#Bienvenidas--------------------------------------------------------------------------
@client.event
async def on_member_join(usuario):

#Autorol
 rol = nextcord.utils.get(usuario.guild.roles, name="Miembros 🏆")
 await usuario.add_roles(rol)

#Mandar el mensaje en el canal del sistema
 canal = usuario.guild.system_channel
#Imagenes de bienvenida (Lo puedo poner en un archivo a parte, ¿pero ves que me importe? xdddd)
 imagenesfondo = ["welcums/welcum.gif",
                  "welcums/welcum2.gif",
                  "welcums/welcum3.gif",
                  "welcums/welcum4.gif",
                  "welcums/welcum5.gif",
                  "welcums/welcum6.gif",
                  "welcums/welcum7.gif",
                  "welcums/welcum8.gif",
                  "welcums/welcum9.gif",
                  "welcums/welcum10.gif",
                  "welcums/welcum11.gif",
                  "welcums/welcum12.gif",
                  "welcums/welcum13.gif",
                  "welcums/welcum14.gif"]

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
print("El módulo de moderación está en línea")
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



#RUN
client.run(TOKEN)
