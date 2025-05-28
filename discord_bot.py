import discord
import re
import asyncio
import aiohttp
import json
from discord.ext import commands

# Configuración
BOT_TOKEN = "AQUI_TU_NUEVO_TOKEN"  # ⚠️ REEMPLAZA CON TU NUEVO TOKEN DESPUÉS DE REGENERARLO
WEBAPP_URL = "https://tu-aplicacion.com"  # URL de tu aplicación Albion (opcional)

# Configurar el bot
intents = discord.Intents.default()
intents.message_content = True  # Necesario para leer contenido de mensajes
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    print(f'🔍 Monitoreando mensajes BODYGUARD...')

@bot.event
async def on_message(message):
    # Ignorar mensajes del propio bot
    if message.author == bot.user:
        return
    
    # Verificar si el mensaje contiene "BODYGUARD"
    if 'BODYGUARD' in message.content.upper():
        print(f"📨 Mensaje BODYGUARD detectado de {message.author}")
        print(f"🔍 Contenido: {message.content}")
        
        # Extraer menciones usando regex
        mention_pattern = r'@(\w+)'
        mentions = re.findall(mention_pattern, message.content)
        
        # Filtrar menciones válidas (no @everyone, @here)
        valid_mentions = [m for m in mentions if m not in ['everyone', 'here']]
        
        if valid_mentions:
            print(f"👥 Usuarios mencionados: {', '.join(valid_mentions)}")
            
            # Enviar datos a tu aplicación web
            await send_to_webapp(message.content, str(message.author), valid_mentions)
            
            # Opcional: Confirmar en Discord
            await message.add_reaction('✅')
        else:
            print("⚠️ No se encontraron menciones válidas")
    
    # Procesar otros comandos
    await bot.process_commands(message)

async def send_to_webapp(message_content, author_name, mentions):
    """Envía los datos a tu aplicación web"""
    try:
        data = {
            'type': 'bodyguard_message',
            'content': message_content,
            'author': author_name,
            'mentions': mentions,
            'timestamp': discord.utils.utcnow().isoformat()
        }
        
        async with aiohttp.ClientSession() as session:
            # Aquí enviarías los datos a tu aplicación web
            # Por ahora solo imprimimos para debug
            print(f"📤 Enviando a webapp: {json.dumps(data, indent=2)}")
            
            # Ejemplo de cómo enviar HTTP POST a tu aplicación:
            # Si tienes tu aplicación web en línea, descomenta esto:
            # async with session.post(WEBAPP_URL + '/api/discord-bodyguard', json=data) as response:
            #     if response.status == 200:
            #         print("✅ Datos enviados exitosamente")
            #     else:
            #         print(f"❌ Error al enviar: {response.status}")
            
            # Por ahora, simula el procesamiento local
            print("🔄 Simulando procesamiento de menciones...")
            for username in mentions:
                print(f"  ✅ '{username}' marcado como BODY + PRIO")
    except Exception as e:
        print(f"❌ Error enviando a webapp: {e}")

@bot.command(name='test')
async def test_command(ctx):
    """Comando de prueba"""
    await ctx.send('🤖 Bot funcionando correctamente!')

@bot.command(name='bodyguard_test')
async def bodyguard_test(ctx, *, users):
    """Comando para simular un mensaje BODYGUARD
    Uso: !bodyguard_test @JeffMVA @assbreakerUY
    """
    test_message = f"BODYGUARD {users}"
    print(f"🧪 Simulando mensaje: {test_message}")
    
    # Simular el procesamiento
    mention_pattern = r'@(\w+)'
    mentions = re.findall(mention_pattern, test_message)
    valid_mentions = [m for m in mentions if m not in ['everyone', 'here']]
    
    if valid_mentions:
        await send_to_webapp(test_message, str(ctx.author), valid_mentions)
        await ctx.send(f'✅ Test completado. Usuarios procesados: {", ".join(valid_mentions)}')
    else:
        await ctx.send('❌ No se encontraron menciones válidas')

# Función para integrar con tu aplicación web
def process_mentions_for_webapp(mentions):
    """
    Esta función simula cómo tu aplicación web recibiría y procesaría las menciones
    """
    print("🔄 Procesando menciones para webapp...")
    for username in mentions:
        print(f"  ➕ Agregando '{username}' con BODY + PRIO")
        # Aquí iría la lógica para actualizar Firebase
        # Similar a tu función processDiscordMessage()

# Ejecutar el bot
if __name__ == "__main__":
    print("🚀 Iniciando Discord Bot BODYGUARD Monitor...")
    print("📋 Configuración:")
    print(f"   - Monitoreando palabra clave: BODYGUARD")
    print(f"   - Extrayendo menciones: @usuario")
    print(f"   - Enviando a webapp: {WEBAPP_URL}")
    print("🔧 Para configurar:")
    print("   1. Reemplaza BOT_TOKEN con tu token real del Discord Developer Portal")
    print("   2. Reemplaza WEBAPP_URL con la URL de tu aplicación Albion")
    print("   3. Ejecuta: python discord_bot.py")
    print("   4. Escribe 'BODYGUARD @usuario @usuario2' en tu canal de Discord")
    
    # Ejecutar el bot (descomenta la siguiente línea cuando tengas el nuevo token)
    bot.run(BOT_TOKEN)