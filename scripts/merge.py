from loguru import logger
import os

# 配置logger
logger.add("downloaderLog.log", rotation="1 MB")


def mergeVA(video: str, audio: str):
    os.system("ffmpeg -i " + video + " -i " + audio +
              " -c:v copy -c:a copy -v quiet output.mp4")
    os.system("del " + video)
    os.system("del " + audio)
