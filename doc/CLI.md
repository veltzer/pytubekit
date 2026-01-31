# pytubekit - CLI Commands Reference

Pytubekit provides a single entry point (`pytubekit`) with multiple subcommands (endpoints). Each endpoint accepts configuration parameters that can be passed via command-line arguments.

## Commands

### `get_channel_id`

Show your YouTube channel ID.

```bash
pytubekit get_channel_id
```

No additional parameters.

---

### `get_watch_later_playlist_id`

Get the playlist ID for your "Watch Later" playlist. This is derived from your channel ID by replacing the second character with "L".

```bash
pytubekit get_watch_later_playlist_id
```

No additional parameters.

---

### `playlists`

List all playlists in your YouTube account.

```bash
pytubekit playlists
pytubekit playlists --full    # Output full JSON for each playlist
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--page-size` | int | 50 | Page size for API pagination (max 50) |
| `--full` | bool | False | Output full JSON instead of just titles |

---

### `playlist`

List all entries in a specific playlist.

```bash
pytubekit playlist --name "My Playlist"
pytubekit playlist --playlist-id PLxxxxxxxx
pytubekit playlist --name "My Playlist" --full
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--name` | str | None | Playlist name to look up |
| `--playlist-id` | str | None | Playlist ID to use directly |
| `--page-size` | int | 50 | Page size for API pagination |
| `--full` | bool | False | Output full JSON instead of just video IDs |

Provide either `--name` or `--playlist-id`, not both.

---

### `dump`

Dump all playlists to files in a folder. Each playlist is saved as a separate file named after the playlist title, containing video IDs (or full JSON if `--full` is set).

```bash
pytubekit dump --dump-folder /path/to/output
pytubekit dump --dump-folder '${home}/youtube-backup/${date}'
```

The `--dump-folder` parameter supports template substitution:
- `${date}` - current Unix timestamp
- `${home}` - user's home directory

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--dump-folder` | str | `.` | Folder to dump playlists into |
| `--page-size` | int | 50 | Page size for API pagination |
| `--full` | bool | False | Output full JSON instead of just video IDs |

---

### `cleanup`

Clean up a set of playlists by removing duplicates, deleted videos, and/or private videos.

```bash
pytubekit cleanup --names "Playlist1" "Playlist2"
pytubekit cleanup --names "My Playlist" --no-dedup      # Skip deduplication
pytubekit cleanup --names "My Playlist" --no-do-delete   # Dry run (report only)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--names` | list[str] | (required) | Playlist names to clean up |
| `--dedup` | bool | True | Detect and remove duplicate entries |
| `--deleted` | bool | True | Remove deleted videos |
| `--privatized` | bool | True | Remove private videos |
| `--do-delete` | bool | True | Actually perform deletions (set to False for dry run) |
| `--page-size` | int | 50 | Page size for API pagination |

---

### `remove_unavailable_from_all_playlists`

Remove unavailable (deleted/private) videos from all of your playlists.

```bash
pytubekit remove_unavailable_from_all_playlists
pytubekit remove_unavailable_from_all_playlists --no-do-delete   # Dry run
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--deleted` | bool | True | Remove deleted videos |
| `--privatized` | bool | True | Remove private videos |
| `--do-delete` | bool | True | Actually perform deletions |
| `--page-size` | int | 50 | Page size for API pagination |

---

### `subtract`

Subtract one set of playlists from another. Finds videos present in both sets and removes them from the "subtract from" playlists.

```bash
pytubekit subtract --subtract-what "Watched" --subtract-from "To Watch"
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--subtract-what` | list[str] | (required) | Playlist names containing items to subtract |
| `--subtract-from` | list[str] | (required) | Playlist names to subtract from |
| `--do-delete` | bool | True | Actually perform deletions |
| `--page-size` | int | 50 | Page size for API pagination |

---

### `video_info`

Get detailed information about a specific video.

```bash
pytubekit video_info --id xL_sMXfzzyA
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--id` | str | (required) | YouTube video ID |

Returns snippet, status, and content details as JSON.

---

### `collect_ids`

Collect YouTube video IDs from files in the current directory. Lists file extensions found.

```bash
pytubekit collect_ids
```

No additional parameters.

---

### `channels`

List your channels and their playlists with full details (snippet, content details, statistics).

```bash
pytubekit channels
```

No additional parameters.

---

### `watch_later`

Download the Watch Later playlist using youtube-dl.

```bash
pytubekit watch_later
```

No additional parameters. Uses youtube-dl with `.netrc` authentication.
