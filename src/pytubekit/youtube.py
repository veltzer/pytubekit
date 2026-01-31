"""
Module that handles the interaction with the yt_dlp library

References:
- https://github.com/yt-dlp/yt-dlp#embedding-yt-dlp
"""
import logging

import yt_dlp

from pytubekit.static import LOGGER_NAME


def youtube_dl_download_urls(urls: list[str]) -> None:
    logger = logging.getLogger(LOGGER_NAME)
    ydl_opts = {
        "extract_flat": True,
        "usenetrc": True,
    }
    logger.debug(f"passing options {ydl_opts}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
