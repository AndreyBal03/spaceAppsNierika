import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import clipboard

def run(playwright: Playwright, url, lat, lon) -> None:
browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(
        "https://search.earthdata.nasa.gov/search/granules?p=C1534729776-LPDAAC_ECS!C1534729776-LPDAAC_ECS!C2076114664-LPCLOUD&pg[1][v]=t&pg[1][gsk]=-start_date&pg[1][m]=download&pg[1][cd]=f&pg[2][a]=3168642103!LPCLOUD&pg[2][v]=t&pg[2][gsk]=-start_date&pg[2][m]=download&pg[2][cd]=f&q=ecostress&sp[0]=41.76563%2C4.94247&ac=true&tl=1728164359!3!!&lat=2.4609375&long=28.546875&zoom=4")
    page.goto(
        "https://search.earthdata.nasa.gov/search/granules?p=C1534729776-LPDAAC_ECS!C1534729776-LPDAAC_ECS!C2076114664-LPCLOUD&q=ecostress&sp[0]=41.76563%2C4.94247&ac=true&tl=1728164359!3!!&lat=2.4609375&long=28.546875&zoom=4")
    page.goto(
        "https://search.earthdata.nasa.gov/search/granules?p=C1534729776-LPDAAC_ECS!C1534729776-LPDAAC_ECS!C2076114664-LPCLOUD&pg[1][v]=t&pg[1][gsk]=-start_date&pg[1][m]=download&pg[2][a]=3168642103!LPCLOUD&pg[2][v]=t&pg[2][gsk]=-start_date&pg[2][m]=download&q=ecostress&sp[0]=41.76563%2C4.94247&ac=true&tl=1728164359!3!!&lat=2.4609375&long=28.546875&zoom=4")
    page.goto(
        f"https://urs.earthdata.nasa.gov/oauth/authorize?response_type=code&client_id=OLpAZlE4HqIOMr0TYqg7UQ&redirect_uri=https%3A%2F%2Fd53njncz5taqi.cloudfront.net%2Furs_callback&state=https%3A%2F%2Fsearch.earthdata.nasa.gov%2Fsearch%2Fgranules%3Fp%3DC1534729776-LPDAAC_ECS%2521C1534729776-LPDAAC_ECS%2521C2076114664-LPCLOUD%26q%3Decostress%26sp%255B0%255D%3D{lon:.6}%252C{lat:.6}%26ac%3Dtrue%26tl%3D1728164359%25213%2521%2521%26lat%3D{lat}%26long%3D{lon}%26zoom%3D4%26ee%3Dprod")
    page.get_by_label("Username").fill("heisenberg11401")
    url = f"https://urs.earthdata.nasa.gov/oauth/authorize?response_type=code&client_id=OLpAZlE4HqIOMr0TYqg7UQ&redirect_uri=https%3A%2F%2Fd53njncz5taqi.cloudfront.net%2Furs_callback&state=https%3A%2F%2Fsearch.earthdata.nasa.gov%2Fsearch%2Fgranules%3Fp%3DC1534729776-LPDAAC_ECS%2521C1534729776-LPDAAC_ECS%2521C2076114664-LPCLOUD%26q%3Decostress%26sp%255B0%255D%3D{lon:.6}%252C{lat:.6}%26ac%3Dtrue%26tl%3D1728164359%25213%2521%2521%26lat%3D{lat}%26long%3D{lon}%26zoom%3D4%26ee%3Dprod"
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("Heisenberg11401@gmail.com")
    page.get_by_role("button", name="Log in").click()
    page.goto(url)
    page.get_by_role("button", name="End Date, Newest First").click()
    time.sleep(20)

    page.locator("body").press("ControlOrMeta+a")
    page.locator("body").press("ControlOrMeta+c")

    # ---------------------
    context.close()
    browser.close()


def main(lat, lon):
    url = f"https://search.earthdata.nasa.gov/auth_callback?redirect=https%3A%2F%2Fsearch.earthdata.nasa.gov%2Fsearch%2Fgranules%3Fp%3DC1534729776-LPDAAC_ECS%21C1534729776-LPDAAC_ECS%21C2076114664-LPCLOUD%26q%3Decostress%26sp%5B0%5D%3D{lon}%2C{lat}%26ac%3Dtrue%26tl%3D1728164359%213%21%21%26lat%3D{lat}%26long%3D{lon}%26zoom%3D4%26ee%3Dprod&jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDEwNDAxLCJ1c2VybmFtZSI6ImhlaXNlbmJlcmcxMTQwMSIsInByZWZlcmVuY2VzIjp7fSwidXJzUHJvZmlsZSI6eyJlbWFpbF9hZGRyZXNzIjoiaGVpc2VuYmVyZzExNDAxQGdtYWlsLmNvbSIsImZpcnN0X25hbWUiOiJIZWkifSwiZWFydGhkYXRhRW52aXJvbm1lbnQiOiJwcm9kIiwiaWF0IjoxNzI4MTk3NDM0fQ.p-RXFeeA4exQeUxQKrqBydIMU0_kzfmHm8PvnivuMSE"

    with sync_playwright() as playwright:
        run(playwright, url, lat, lon)

        text = clipboard.paste()
        loc = text.find('matching granules')
        print(text)
        pre_granular = text[(loc + 23):(loc + 150)]
        loc2 = pre_granular.find('ECOSTRESS')
        granular = pre_granular[(loc2):(loc2 + 51)]
        print("gran: ",granular)
        fecha = granular[28:32] + "." + granular[32:34] + "." + granular[34:36]
        url = "https://e4ftl01.cr.usgs.gov/ECOSTRESS/ECO2LSTE.001/" + fecha + "/" + granular + ".1.jpg"
        print(url)


