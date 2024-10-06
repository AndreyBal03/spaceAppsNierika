from telegram import Update
from telegram.ext import ContextTypes
from geopy.geocoders import Nominatim

import requests
import re

def handle_response(text: str):
    text_ = text.split(" ")
    if len(text) < 2: 
        return "Respuesta generica"

    match text_[0].lower():
        case 'coords':
            if len(text_) != 2:
                return "Incorrect args :(, make sure you are not leaving two spaces between coors 'link'"
            coords = extract_coordinates_from_maps_url(get_final_url(text_[1]))
            print(get_final_url(text_[1]))
            return f"lat, lon = {coords[0]}, {coords[1]}"

    
    return "Respuesta generica"

def extract_coordinates_from_maps_url(url):
    pattern = r"(-?\d+\.\d+),(-?\d+\.\d+)"
    match = re.search(pattern, url)

    pattern = r"\d(5)"
    match2 = re.search(pattern,url)

    if match:
        latitude = float(match.group(1))
        longitude = float(match.group(2))
        return latitude, longitude
    if match2:
        return get_coordinates_from_postal_code(match2.group(1)) 
    
    return None


def get_coordinates_from_postal_code(postal_code, country='Mexico'):
    # Usamos Nominatim con un agente de usuario definido
    geolocator = Nominatim(user_agent="abcd")
    
    # Hacemos la búsqueda del código postal
    print("A")
    location = geolocator.geocode(f"{postal_code}, {country}")

    print("A")
    
    if location:
        return location.latitude, location.longitude
    else:
        raise ValueError(f"No se encontraron coordenadas para el código postal: {postal_code}")


def get_final_url(initial_url):
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
    
    #diff users and groups
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
        
    print('Bot: ', response)
    await update.message.reply_text(response)

