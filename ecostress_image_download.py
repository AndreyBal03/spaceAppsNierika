import re
from playwright.async_api import async_playwright
import time
import clipboard
import asyncio


async def run(playwright, url, lat, lon):
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    await page.goto(
        "https://search.earthdata.nasa.gov/search/granules?p=C1534729776-LPDAAC_ECS!C1534729776-LPDAAC_ECS!C2076114664-LPCLOUD&pg[1][v]=t&pg[1][gsk]=-start_date&pg[1][m]=download&pg[1][cd]=f&pg[2][a]=3168642103!LPCLOUD&pg[2][v]=t&pg[2][gsk]=-start_date&pg[2][m]=download&q=ecostress&sp[0]=41.76563%2C4.94247&ac=true&tl=1728164359!3!!&lat=2.4609375&long=28.546875&zoom=4")
    await page.goto(
        "https://search.earthdata.nasa.gov/search/granules?p=C1534729776-LPDAAC_ECS!C1534729776-LPDAAC_ECS!C2076114664-LPCLOUD&pg[1][v]=t&pg[1][gsk]=-start_date&pg[1][m]=download&pg[1][cd]=f&pg[2][a]=3168642103!LPCLOUD&pg[2][v]=t&pg[2][gsk]=-start_date&pg[2][m]=download&q=ecostress&sp[0]=41.76563%2C4.94247&ac=true&tl=1728164359!3!!&lat=2.4609375&long=28.546875&zoom=4")
    await page.goto(
        "https://search.earthdata.nasa.gov/search/granules?p=C1534729776-LPDAAC_ECS!C1534729776-LPDAAC_ECS!C2076114664-LPCLOUD&pg[1][v]=t&pg[1][gsk]=-start_date&pg[1][m]=download&pg[1][cd]=f&pg[2][a]=3168642103!LPCLOUD&pg[2][v]=t&pg[2][gsk]=-start_date&pg[2][m]=download&q=ecostress&sp[0]=41.76563%2C4.94247&ac=true&tl=1728164359!3!!&lat=2.4609375&long=28.546875&zoom=4")

    await page.goto(
        f"https://urs.earthdata.nasa.gov/oauth/authorize?response_type=code&client_id=OLpAZlE4HqIOMr0TYqg7UQ&redirect_uri=https%3A%2F%2Fd53njncz5taqi.cloudfront.net%2Furs_callback&state=https%3A%2F%2Fsearch.earthdata.nasa.gov%2Fsearch%2Fgranules%3Fp%3DC1534729776-LPDAAC_ECS%2521C1534729776-LPDAAC_ECS%2521C2076114664-LPCLOUD%26q%3Decostress%26sp%255B0%255D%3D{lon:.6}%252C{lat:.6}%26ac%3Dtrue%26tl%3D1728164359%25213%2521%2521%26lat%3D{lat}%26long%3D{lon}%26zoom%3D4%26ee%3Dprod")

    await page.get_by_label("Username").fill("heisenberg11401")
    await page.get_by_label("Password").fill("Heisenberg11401@gmail.com")

    url = f"https://urs.earthdata.nasa.gov/oauth/authorize?response_type=code&client_id=OLpAZlE4HqIOMr0TYqg7UQ&redirect_uri=https%3A%2F%2Fd53njncz5taqi.cloudfront.net%2Furs_callback&state=https%3A%2F%2Fsearch.earthdata.nasa.gov%2Fsearch%2Fgranules%3Fp%3DC1534729776-LPDAAC_ECS%2521C1534729776-LPDAAC_ECS%2521C2076114664-LPCLOUD%26q%3Decostress%26sp%255B0%255D%3D{lon:.6}%252C{lat:.6}%26ac%3Dtrue%26tl%3D1728164359%25213%2521%2521%26lat%3D{lat}%26long%3D{lon}%26zoom%3D4%26ee%3Dprod"

    await page.get_by_role("button", name="Log in").click()
    await page.goto(url)
    await page.get_by_role("button", name="End Date, Newest First").click()

    await asyncio.sleep(20)
    await page.locator("body").press("ControlOrMeta+a")
    await page.locator("body").press("ControlOrMeta+c")

    # Cerramos el contexto y el navegador
    await context.close()
    await browser.close()


async def main(lat, lon):
    url = f"https://search.earthdata.nasa.gov/auth_callback?redirect=https%3A%2F%2Fsearch.earthdata.nasa.gov%2Fsearch%2Fgranules%3Fp%3DC1534729776-LPDAAC_ECS%21C1534729776-LPDAAC_ECS%21C2076114664-LPCLOUD%26q%3Decostress%26sp%5B0%5D%3D{lon}%2C{lat}%26ac%3Dtrue%26tl%3D1728164359%213%21%21%26lat%3D{lat}%26long%3D{lon}%26zoom%3D4%26ee%3Dprod"

    async with async_playwright() as playwright:
        await run(playwright, url, lat, lon)

        text = clipboard.paste()
        print(text)

        # Usar expresión regular para encontrar el patrón "ECOSTRESS_L2_LSTE_XXXXXXXX_XXXXXXXXXXXXX_XXXX_XX"
        pattern = r"ECOSTRESS_L2_LSTE_\d{5}_\d{3}_\d{8}T\d{6}_\d{4}_\d{2}"
        text = "ECOSTRESS_L2_LSTE_35103_011_20240914T094818_0601_02.h5"
        match = re.search(pattern, text)
        print(match)

        if match:
            granular = match.group(0)  # Obtener el primer valor que coincida con el patrón
            print(f"Granular: {granular}")

            # Extraer la fecha del nombre del granular
            fecha = granular[28:32] + "." + granular[32:34] + "." + granular[34:36]

            # Crear la URL de la imagen
            image_url = f"https://e4ftl01.cr.usgs.gov/ECOSTRESS/ECO2LSTE.001/{fecha}/{granular}.1.jpg"
            print(f"URL de la imagen: {image_url}")
        else:
            print("No se encontró ningún valor con el formato ECOSTRESS_L2_LSTE")

        return image_url