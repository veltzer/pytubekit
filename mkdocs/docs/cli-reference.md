# CLI Commands Reference

Pytubekit provides a single entry point (`pytubekit`) with multiple subcommands (endpoints). Each endpoint accepts configuration parameters that can be passed via command-line arguments.

## Listing / Info

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

List all playlists in your YouTube account. Shows each playlist name and its item count.

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

### `count`

Print the item count for one or more playlists.

```bash
pytubekit count --count-names "Music" "Talks"
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--count-names` | list[str] | (required) | Playlist names to count items in |
| `--page-size` | int | 50 | Page size for API pagination |

---

### `video_info`

Get detailed information about a specific video (snippet, status, content details).

```bash
pytubekit video_info --id xL_sMXfzzyA
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--id` | str | (required) | YouTube video ID |

---

### `channels`

List your channels and their playlists with full details (snippet, content details, statistics).

```bash
pytubekit channels
```

No additional parameters.

---

### `find_video`

Find which playlists contain a given video. Iterates all playlists and checks each for the specified video ID.

```bash
pytubekit find_video --find-video-id dQw4w9WgXcQ
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--find-video-id` | str | (required) | YouTube video ID to search for |
| `--page-size` | int | 50 | Page size for API pagination |

---

### `stats`

Show summary statistics for all playlists: each playlist name with its item count, then totals (number of playlists, total videos, largest, smallest).

```bash
pytubekit stats
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--page-size` | int | 50 | Page size for API pagination |

---

### `search_playlist`

Search for videos by title or channel name across one or more playlists.

```bash
pytubekit search_playlist --search-playlists "Music" "Talks" --search-query "python"
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--search-playlists` | list[str] | (required) | Playlist names to search in |
| `--search-query` | str | (required) | Text to search for in video title or channel name |
| `--page-size` | int | 50 | Page size for API pagination |

---

## Export / Backup

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

### `export_csv`

Export a playlist to CSV with video ID, title, channel, and position.

```bash
pytubekit export_csv --export-playlist-name "Music" --export-csv-path music.csv
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--export-playlist-name` | str | (required) | Name of playlist to export |
| `--export-csv-path` | str | (required) | Path to CSV file to write |
| `--page-size` | int | 50 | Page size for API pagination |

Output columns: `position`, `video_id`, `title`, `channel`.

---

### `collect_ids`

Extract YouTube video IDs from text files.

```bash
pytubekit collect_ids --collect-files notes.txt bookmarks.html
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--collect-files` | list[str] | (required) | Files to scan for YouTube video IDs |

Prints unique video IDs found across all input files.

---

### `add_data`

Fetch extensive metadata for a list of video IDs and write to CSV. Supports resuming from a previous run (skips IDs already present in the output CSV).

```bash
pytubekit add_data --input-file ids.txt --output-csv metadata.csv
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--input-file` | str | (required) | Path to text file with video IDs (one per line) |
| `--output-csv` | str | (required) | Path to CSV file to write metadata to |

---

### `diff`

Find unseen or seen videos by diffing YouTube playlists against local files of video IDs.

```bash
# Find videos in playlists that are NOT in local files (unseen)
pytubekit diff --source-playlists "All" --seen-files seen.txt --output-file unseen.txt

# Find videos in playlists that ARE in local files (seen)
pytubekit diff --source-playlists "All" --seen-files seen.txt --reverse --output-file seen_online.txt
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--source-playlists` | list[str] | (required) | YouTube playlist names to pull videos from |
| `--seen-files` | list[str] | (required) | Local files with video IDs (one per line) |
| `--reverse` | bool | False | `False` = unseen videos, `True` = seen videos |
| `--output-file` | str | (required) | Path to write results to |
| `--page-size` | int | 50 | Page size for API pagination |

---

### `left_to_see`

List unseen videos by subtracting seen playlists from source playlists.

```bash
pytubekit left_to_see --lts-all-playlists "Channel Videos" --lts-seen-playlists "Watched"
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--lts-all-playlists` | list[str] | (required) | Playlist names containing all videos |
| `--lts-seen-playlists` | list[str] | (required) | Playlist names containing already-seen videos |
| `--page-size` | int | 50 | Page size for API pagination |

---

## Cleanup

### `cleanup`

Clean up a set of playlists by removing duplicates, deleted videos, and/or private videos.

```bash
pytubekit cleanup --cleanup-names "Playlist1" "Playlist2"
pytubekit cleanup --cleanup-names "My Playlist" --no-dedup      # Skip deduplication
pytubekit cleanup --cleanup-names "My Playlist" --no-do-delete   # Dry run (report only)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--cleanup-names` | list[str] | (required) | Playlist names to clean up |
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

## Playlist Operations

### `create_playlist`

Create a new playlist with a given name, description, and privacy status.

```bash
pytubekit create_playlist --create-name "My New Playlist"
pytubekit create_playlist --create-name "Private List" --create-description "Personal videos" --create-privacy private
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--create-name` | str | (required) | Name for the new playlist |
| `--create-description` | str | `""` | Description for the new playlist |
| `--create-privacy` | str | `public` | Privacy status: `public`, `unlisted`, or `private` |

---

### `delete_playlist`

Delete a playlist by name.

```bash
pytubekit delete_playlist --delete-playlist-name "Old Playlist"
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--delete-playlist-name` | str | (required) | Name of the playlist to delete |

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

### `copy_playlist`

Copy all videos from one playlist to another.

```bash
pytubekit copy_playlist --copy-source "Original" --copy-destination "Backup"
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--copy-source` | str | (required) | Source playlist name to copy from |
| `--copy-destination` | str | (required) | Destination playlist name to copy to |
| `--page-size` | int | 50 | Page size for API pagination |

---

### `merge`

Merge several playlists into one destination playlist, deduplicating along the way.

```bash
pytubekit merge --merge-sources "Rock" "Pop" --merge-destination "All Music"
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--merge-sources` | list[str] | (required) | Source playlist names to merge from |
| `--merge-destination` | str | (required) | Destination playlist name to merge into |
| `--page-size` | int | 50 | Page size for API pagination |

---

### `sort_playlist`

Sort a playlist by title, channel, or date. This deletes and re-adds all items in sorted order.

```bash
pytubekit sort_playlist --sort-playlist-name "Music" --sort-key title
pytubekit sort_playlist --sort-playlist-name "Music" --sort-key channel
pytubekit sort_playlist --sort-playlist-name "Music" --sort-key date
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--sort-playlist-name` | str | (required) | Name of playlist to sort |
| `--sort-key` | str | `title` | Sort key: `title`, `channel`, or `date` |
| `--page-size` | int | 50 | Page size for API pagination |

!!! warning
    Sorting deletes all items from the playlist and re-adds them in order. This consumes significant API quota.

---

### `rename_playlist`

Rename a playlist.

```bash
pytubekit rename_playlist --rename-playlist-name "Old Name" --rename-new-name "New Name"
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--rename-playlist-name` | str | (required) | Current name of the playlist |
| `--rename-new-name` | str | (required) | New name for the playlist |

---

### `clear_playlist`

Delete all items from a playlist.

```bash
pytubekit clear_playlist --clear-name "Temp"
pytubekit clear_playlist --clear-name "Temp" --no-do-delete   # Dry run
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--clear-name` | str | (required) | Name of playlist to clear |
| `--do-delete` | bool | True | Actually perform deletions |
| `--page-size` | int | 50 | Page size for API pagination |

---

### `overflow`

Move videos from a source playlist to a destination playlist, respecting YouTube's 5,000-item playlist limit.

```bash
pytubekit overflow --source "Big Playlist" --destination "Big Playlist Overflow"
pytubekit overflow --source "Big Playlist" --destination "Overflow" --no-do-delete   # Dry run
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--source` | str | (required) | Source playlist name |
| `--destination` | str | (required) | Destination playlist name |
| `--do-delete` | bool | True | Actually move (set to False for dry run) |
| `--page-size` | int | 50 | Page size for API pagination |

---

### `add_file_to_playlist`

Add video IDs from a file to a playlist.

```bash
pytubekit add_file_to_playlist --add-file ids.txt --add-playlist "My Playlist"
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--add-file` | str | (required) | Path to text file with video IDs (one per line) |
| `--add-playlist` | str | (required) | Name of playlist to add videos to |
| `--page-size` | int | 50 | Page size for API pagination |

---

## Local Commands (Zero API Quota)

These commands work entirely on dump files produced by `dump`. They make **zero YouTube API calls** and consume no quota.

### `local_find_video`

Find which dump files contain a given video ID.

```bash
pytubekit local_find_video --local-video-id dQw4w9WgXcQ
pytubekit local_find_video --local-dump-folder /path/to/dump --local-video-id dQw4w9WgXcQ
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--local-dump-folder` | str | `.` | Path to dump folder |
| `--local-video-id` | str | (required) | Video ID to search for |

---

### `local_search`

Case-insensitive substring search across all dump files. Output is grep-like: `filename:lineno: line`.

```bash
pytubekit local_search --local-search-pattern "dQw4"
pytubekit local_search --local-dump-folder /path/to/dump --local-search-pattern "dQw4"
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--local-dump-folder` | str | `.` | Path to dump folder |
| `--local-search-pattern` | str | (required) | Case-insensitive substring to search for |

---

### `local_count`

Count lines per dump file and print a summary (total, largest, smallest).

```bash
pytubekit local_count
pytubekit local_count --local-dump-folder /path/to/dump
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--local-dump-folder` | str | `.` | Path to dump folder |

---

### `local_diff`

Read two paths (each can be a file or folder) and compute the set difference A−B (default) or intersection A∩B (`--local-diff-reverse`).

```bash
# IDs in folder A but not in folder B
pytubekit local_diff --local-diff-a /dump/all --local-diff-b /dump/seen

# IDs in both A and B
pytubekit local_diff --local-diff-a /dump/all --local-diff-b /dump/seen --local-diff-reverse
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--local-diff-a` | str | (required) | Path A (file or folder) |
| `--local-diff-b` | str | (required) | Path B (file or folder) |
| `--local-diff-reverse` | bool | False | `False` = A−B, `True` = A∩B |

---

### `local_left_to_see`

Compute unseen video IDs from two dump folders: all − seen.

```bash
pytubekit local_left_to_see --local-lts-all-folder /dump/all --local-lts-seen-folder /dump/seen
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--local-lts-all-folder` | str | (required) | Folder with all video IDs |
| `--local-lts-seen-folder` | str | (required) | Folder with seen video IDs |

---

### `local_dedup`

Report intra-playlist duplicates (same ID appears more than once in a single file) and cross-playlist duplicates (same ID appears in multiple files).

```bash
pytubekit local_dedup
pytubekit local_dedup --local-dump-folder /path/to/dump
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--local-dump-folder` | str | `.` | Path to dump folder |

Output lines are prefixed with `INTRA` (within one file) or `CROSS` (across files).

---

## Download

### `watch_later`

Download the Watch Later playlist using yt-dlp.

```bash
pytubekit watch_later
```

No additional parameters. Uses yt-dlp with `.netrc` authentication.
