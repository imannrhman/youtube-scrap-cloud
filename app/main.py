from fastapi import FastAPI, HTTPException

import app.scraping as scraping

apps = FastAPI()


@apps.get("/")
async def root():
    return {"message": "Welcome"}


@apps.get("/youtube/search_video")
async def search_video(query: str):
    try:
        if query:
            return scraping.get_video_result(query)
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
