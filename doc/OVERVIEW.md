# pytubekit - Project Overview

**Version:** 0.0.31
**License:** MIT
**Author:** Mark Veltzer
**Python:** >= 3.12
**Status:** Beta

## What is pytubekit?

Pytubekit is a command-line tool for performing bulk operations on your YouTube account. It uses the YouTube Data API v3 to manage playlists, clean up unavailable videos, deduplicate entries, dump playlist contents, and more.

## Key Features

- List all playlists in your YouTube account
- List all items within a specific playlist
- Dump all playlists to files on disk
- Clean up playlists: remove duplicates, deleted videos, and private videos
- Remove unavailable/private videos from all playlists at once
- Subtract one set of playlists from another (set difference)
- Get detailed information about a specific video
- List channels and their playlists
- Download Watch Later playlist via youtube-dl

## Installation

From PyPI:

```bash
pip install pytubekit
```

From source:

```bash
git clone https://github.com/veltzer/pytubekit.git
cd pytubekit
pip install -e .
```

## Quick Start

After installation, the `pytubekit` command becomes available:

```bash
# List all your playlists
pytubekit playlists

# List items in a specific playlist
pytubekit playlist --name "My Playlist"

# Clean up a playlist (remove duplicates, deleted, and private videos)
pytubekit cleanup --names "My Playlist" --do-delete

# Get info about a video
pytubekit video_info --id xL_sMXfzzyA
```

## Authentication

Pytubekit uses OAuth2 to authenticate with the YouTube API. On first run, it will open a browser window for you to authorize access to your YouTube account. The credentials are managed by the `pygooglehelper` library and a `client_secret.json` file bundled with the package.

The following YouTube API scopes are requested:

- `youtube` - full access
- `youtube.force-ssl` - SSL-enforced access
- `youtube.readonly` - read-only access

## API Quota

The YouTube Data API v3 has a quota of **10,000 units per day**. If you hit the limit, wait until the next day for the quota to reset.

Reference: https://developers.google.com/youtube/v3/getting-started

## Links

- **Repository:** https://github.com/veltzer/pytubekit
- **PyPI:** https://pypi.org/project/pytubekit/
- **Website:** https://veltzer.github.io/pytubekit
- **YouTube API v3 Docs:** https://developers.google.com/youtube/v3
- **YouTube API Reference:** https://developers.google.com/youtube/v3/docs
