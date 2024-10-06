from telegram import Update
from telegram.ext import ContextTypes
from geopy.geocoders import Nominatim
import requests
import re
import ecostress_image_download
import aiohttp

async def handle_response(text: str):
    text_ = text.split(" ")

    if len(text_) < 2:
        return "It looks like you're trying to ask something. Try '/help' to see what I can do for you 😊."

    command = text_[0].lower()

    if command == 'coords':
        if len(text_) != 2:
            return "I need a Google Maps URL to extract the coordinates! 😊 Make sure you're not leaving two spaces between the URL."
        coords = await extract_coordinates_from_maps_url(await get_final_url(text_[1]))
        return f"Here are the coordinates: lat, lon = {coords[0]}, {coords[1]} 🌍"

    elif command == 'ecostress':
        if len(text_) != 2:
            return "Please provide the Google Maps URL! I will get the ECOSTRESS image for you. 😊"

        coords = await extract_coordinates_from_maps_url(await get_final_url(text_[1]))
        image_url = await ecostress_image_download.main(coords[0], coords[1])
        return image_url  # Aquí retornamos la URL de la imagen para usarla en el bot

    elif command == 'aster':
        if len(text_) != 2:
            return "Incorrect args :(, make sure you are not leaving two spaces between coords 'link'"

        # Descargamos el archivo tar.bz2
        url = "https://aster.geogrid.org/ASTER/fetchL3A/ASTB151220013331.tar.bz2"
        file_path = await download_tar_bz2(url)
        
        # Descomprimimos el archivo y obtenemos la ruta del archivo deseado
        tif_file_path = await extract_tif_from_tar(file_path, "data1.l3a.vnir2.tif")
        
        if tif_file_path:
            return tif_file_path  # URL o ruta del archivo
        else:
            return "El archivo 'data1.l3a.vnir2.tif' no se encontró en el tar."

    return "I'm here to help! Type '/help' to see what I can do for you. If you need something specific, let me know! 😄"

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🤖 Here's how I can assist you:

/start - Start a conversation with me 😊
/help - See all the available commands
/coords <maps_url> - Extract coordinates from a Google Maps link 🌍
/ecostress <maps_url> - Get ECOSTRESS image based on coordinates 🛰️

Feel free to ask questions like "How do I get coordinates?" or "What is ECOSTRESS?".
I’m here to make your life easier!
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def suggest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if 'coords' in text:
        await update.message.reply_text("It seems you're asking for coordinates. Use '/coords <maps_url>' to extract them from a Google Maps URL! 😊")
    elif 'ecostress' in text:
        await update.message.reply_text("It seems you want an ECOSTRESS image. Use '/ecostress <maps_url>' to get one from a Google Maps URL! 🌍")
    else:
        await update.message.reply_text("Not sure what you need? Type '/help' for a list of commands or just ask! I'm here to assist you. 😊")

async def download_tar_bz2(url):
    # Descarga el archivo desde la URL
    local_filename = url.split("/")[-1]
    local_filepath = f'/tmp/{local_filename}'
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(local_filepath, 'wb') as f:
                    f.write(await response.read())
                return local_filepath
            else:
                raise Exception(f"Failed to download file: {response.status}")

async def extract_tif_from_tar(file_path, target_filename):
    # Ruta temporal para extraer el contenido
    extract_path = '/tmp/extracted_files'
    os.makedirs(extract_path, exist_ok=True)
    
    # Extraemos el archivo .tar.bz2
    with tarfile.open(file_path, 'r:bz2') as tar:
        tar.extractall(path=extract_path)

        # Buscamos el archivo .tif dentro de la carpeta extraída
        for root, dirs, files in os.walk(extract_path):
            for file in files:
                if file == target_filename:
                    return os.path.join(root, file)
    
    return None

async def extract_coordinates_from_maps_url(url):
    pattern = r"(-?\d+\.\d+),(-?\d+\.\d+)"
    match = re.search(pattern, url)

    pattern2 = r"\d{5}"
    match2 = re.search(pattern2, url)

    if match:
        latitude = float(match.group(1))
        longitude = float(match.group(2))
        return latitude, longitude
    if match2:
        return await get_coordinates_from_postal_code(match2.group(0))

    return None


async def get_coordinates_from_postal_code(postal_code, country='Mexico'):
    # Usamos Nominatim con un agente de usuario definido
    geolocator = Nominatim(user_agent="abcd")

    # Hacemos la búsqueda del código postal de forma asíncrona
    location = geolocator.geocode(f"{postal_code}, {country}")

    if location:
        return location.latitude, location.longitude
    else:
        raise ValueError(f"No se encontraron coordenadas para el código postal: {postal_code}")


async def get_final_url(initial_url):
    try:
        response = requests.get(initial_url, allow_redirects=True)
        final_url = response.url
        return final_url
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am Nierika_bot. Use my commands to start.')


async def coords_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am Nierika_bot. Use my commands to start.')


async def handle_messageTEXT(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = await handle_response(new_text)
        else:
            return
    else:
        response: str = await handle_response(text)

    print('Bot: ', response)

    if response.startswith('http'):
        await context.bot.send_photo(chat_id=update.message.chat.id, photo=response)
    else:
        await update.message.reply_text(response)
