from telegram import Update
from telegram.ext import ContextTypes

from playwright.async_api import async_playwright

async def handle_response(text: str):
    req = text.split(" ")
    print(req)
    match req[0].lower():
        case "ecostress":
            if len(req) < 3:
                return "Recuerda agregar la latitud y longitud :)"

            return await ecostress_response(req[1], req[2])

    return "Respuesta generica"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am Nierika_bot. Use my commands to start.')



async def ecostress_response(lat, lon):
    lat = float(lat)
    lon = float(lon)

    url = f"https://search.earthdata.nasa.gov/search/granules?p=C1534729776-LPDAAC_ECS!C1534729776-LPDAAC_ECS&pg[1][v]=t&pg[1][gsk]=-start_date&pg[1][m]=download&pg[1][cd]=f&q=ecostress&sp[0]={lon:.6}%2C{lat:.6}&ac=true&lat={lat}&long={lon}&zoom=5"

    # Use Playwright to open the browser asynchronously
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await page.goto(url)

        # Wait for the elements to load
        await page.wait_for_selector("h3.granule-results-item__title")

        # Get all h3 elements with the specific class
        granule_titles = await page.query_selector_all("h3.granule-results-item__title")

        # Extract the texts from the h3 elements
        titles = [await title.inner_text() for title in granule_titles]

        # Close the browser
        await browser.close()

    return titles


async def handle_messageTEXT(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    #diff users and groups
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = await handle_response(new_text)
        else:
            return
    else:
        response: str = await handle_response(text)
        
    print('Bot: ', response)
    await update.message.reply_text(response)

