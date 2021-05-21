"""
Module that handles the interaction with the youtube_dl library

References:
- https://github.com/ytdl-org/youtube-dl/blob/master/README.md#embedding-youtube-dl
- https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
"""
import logging
from typing import List

import youtube_dl

from pytubekit.static import LOGGER_NAME


def youtube_dl_download_urls(urls: List[str]) -> None:
    logger = logging.getLogger(LOGGER_NAME)
    # all options are here:
    # https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L128-L278
    ydl_opts = {
        # this shuts everything down
        # 'logger': logger,
        'extract_flat': True,
        'usenetrc': True,
        # 'username': "mark.veltzer@gmail.com",
        # 'password': "",
    }
    logger.debug(f"passing options {ydl_opts}")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
