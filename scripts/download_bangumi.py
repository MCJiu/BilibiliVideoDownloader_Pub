import requests
from exceptions import (VideoNotFoundError, APIRequestError, IsPreviewError)
from api_url import (bangumi_get_cid_API, bangumi_get_StreamURL)
from settings import header
from loguru import logger
import json

# 配置logger
logger.add("downloaderLog.log", rotation="1 MB")

# 获取番剧信息


def get_streamURL(ep_id: int, cookie={}):
    r = requests.get(bangumi_get_StreamURL,
                     headers=header,
                     cookies=cookie,
                     params={
                         "ep_id": ep_id,
                         "qn": 120,
                         "fnval": 144,
                         "fourk": 1,
                     })
    # 处理API访问的异常和preview的情况
    try:
        if r.status_code != 200:
            raise ConnectionError
        if r.json()["code"] == -404:
            raise VideoNotFoundError
        elif r.json()["code"] != 0:
            raise APIRequestError
        if r.json()["result"]["is_preview"] == 1:
            raise IsPreviewError
    except ConnectionError:
        logger.warning("HTTP request faild with status code: " +
                       str(r.status_code))
        return 0
    except VideoNotFoundError:
        logger.warning(ep_id + " Not Found")
        return 0
    except APIRequestError:
        logger.warning("API request faild with status code: " +
                       str(r.json()["code"]))
        return 0
    except IsPreviewError:
        print(
            "\033[31;1m" +
            "Can't access this movie/anime, probably because you have not provide your Bilibili SESSDATA or your Bilibili account does not have permisson of this movie/anime"
            + "\033[0m")
        return 0

    qualityIDDict = {
        6: "240P 极速",
        16: "360P 流畅",
        32: "480P 清晰",
        64: "720P 高清",
        74: "720P60 高帧率",
        80: "1080P 高清",
        112: "1080P+ 高码率",
        116: "1080P60 高帧率",
        120: "4K 超清",
        125: "HDR 真彩色",
        126: "杜比视界",
        127: "8K 超高清",
    }
    accept_quality = r.json()["result"]["dash"]["video"]
    print("\033[36m" + "The supported qualities are as follows: " + "\033[0m")
    count = 0
    for x in accept_quality:
        print("\033[36m" + "-" * 40 + "\033[0m")
        print("\033[36m" + "Choice ID: " + "\033[0m", end="")
        print(count)
        count += 1
        print("\033[36m" + "Quality ID: " + "\033[0m", end="")
        print(x["id"])
        print("\033[36m" + "Quality name: " + "\033[0m", end="")
        print(qualityIDDict[x["id"]])
        print("\033[36m" + "Codecs: " + "\033[0m", end="")
        print(x["codecs"])
        print("\033[36m" + "" + "\033[0m", end="")
    print("\033[36m" + "-" * 40 + "\033[0m")
    print("")

    while True:
        try:
            qualityChoice = int(
                input("\033[36m" + "Please input the " + "\033[31;1m" +
                      "Choice ID " + "\033[0m\033[36m" +
                      "of the dimension you want: " + "\033[0m"))
            break
        except ValueError:
            print("\033[31;1m" + "Invalid input, Please try again!" +
                  "\033[0m")

    urls = []
    if qualityChoice < len(
            r.json()["result"]["dash"]["video"]) and qualityChoice >= 0:
        urls.append(
            r.json()["result"]["dash"]["video"][qualityChoice]["baseUrl"])
    else:
        print("\033[31;1m" + "Choice ID " + str(qualityChoice) +
              " Not found!" + "\033[0m")
        return 0

    urls.append(r.json()["result"]["dash"]["audio"][0]["baseUrl"])

    return urls


def downloader(streamURLs: list):
    '''
    下载成功返回1，否则返回0
    '''
    print("\033[36m" + "Downloading, please wait..." + "\033[0m")
    video_r = requests.get(streamURLs[0], headers=header, stream=True)
    try:
        if video_r.status_code != 200:
            raise ConnectionError
    except ConnectionError:
        logger.warning(
            "Download video: HTTP request faild with status code: " +
            str(video_r.status_code))
        return 0

    with open("video.mp4", "wb") as video:
        for chunk in video_r.iter_content(chunk_size=1024 * 1024):
            video.write(chunk)

    audio_r = requests.get(streamURLs[1], headers=header, stream=True)
    try:
        if audio_r.status_code != 200:
            raise ConnectionError
    except ConnectionError:
        logger.warning(
            "Download audio: HTTP request faild with status code: " +
            str(audio_r.status_code))
        return 0

    with open("audio.wav", "wb") as audio:
        for chunk in audio_r.iter_content(chunk_size=1024 * 1024):
            audio.write(chunk)

    return 1