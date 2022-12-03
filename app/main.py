from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


import app.scraping as scraping

apps = FastAPI()


def set_chrome_options():
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_prefs = {}

    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


@apps.get("/")
async def root():
    return {"message": "Welcome"}


@apps.get("/youtube/search_video")
async def search_video(query: str):
    try:
        if query:
            driver = webdriver.Chrome(options=set_chrome_options())
            return scraping.get_video_result(driver, query)
        else:
            raise HTTPException(status_code=400, detail="Query kosong")
    except Exception as error:
        raise HTTPException(status_code=500, detail="{}".format(error))

# @app.get("/youtube/detail")
# async def detail_video(link: str):
#     try:
#         if link:
#             return scraping.get_comment_video(link)
#         else:
#             raise HTTPException(status_code=400, detail="Query kosong")
#     except Exception as error:
#         raise HTTPException(status_code=500, detail="{}".format(error))
