# Suggestions for pytubekit

## New commands

### `add_file_to_playlist`
Read video IDs from a local file (one per line) and add them all to a named playlist.
This is the inverse of `dump` and is already listed in `TODO.txt`.

### `clear_playlist`
Delete every item from a playlist. Useful for resetting overflow playlists.
Also listed in `TODO.txt`.

### `copy_playlist`
Copy all videos from one playlist to another (like `overflow` but without deleting from source and without the 5000 cap).

### `count`
Print the item count for one or more playlists. Quick way to check which playlists are approaching the 5000 limit without fetching full item lists through the UI.

### `merge`
Merge several playlists into one destination playlist, deduplicating along the way.

### `sort_playlist`
Sort a playlist by title, upload date, or channel name. YouTube's UI only offers limited sorting.

### `search_playlist`
Search for a video title or channel name across one or more playlists and print matching entries.

### `export_csv`
Export a playlist as CSV with columns for video ID, title, channel, and position. More structured than the current plain-ID `dump`.

### `rename_playlist`
Rename a playlist via the API (uses `playlists().update()`).

### `left_to_see`
Given a channel or playlist, subtract already-seen videos (from other playlists or dump files) and output the remainder. Already described in `TODO.txt`.

## Improvements to existing commands

### Progress indicators
Long-running commands (`cleanup`, `overflow`, `subtract`, `dump`, `add_data`) produce no output until they finish. Adding a progress bar or periodic log line (e.g. "processed 200/1500 items") would improve usability.

### Dry-run mode for `overflow`
`cleanup` and `subtract` already accept `ConfigDelete.do_delete`. `overflow` should support the same flag so users can preview how many videos would move before committing.

### Retry / back-off on API errors
YouTube API v3 returns 403 when the daily quota is exhausted and 429 on rate-limit. Adding exponential back-off with a configurable max-retry count would make bulk operations more reliable.

### `collect_ids` is a stub
The current implementation only prints file extensions in the working directory. Either implement the intended functionality (extract YouTube video IDs from local files) or remove the command.

### `watch_later` uses youtube-dl
`youtube-dl` is unmaintained since late 2021. The `add_data` command already shells out to `yt-dlp`. Migrate `watch_later` (and the `youtube.py` module) to use `yt-dlp` as well.

### Consistent output formatting
Some commands use `print()`, others use `logger.info()`. Standardizing on logging for operational messages and reserving `print()` / stdout for data output would make it easier to pipe results.

### `remove_unavailable_from_all_playlists` still uses `ConfigPlaylists`
It accepts `--names` but never actually uses the value — it fetches all playlist IDs with `get_my_playlists_ids`. The `ConfigPlaylists` config could be dropped from its config list to avoid confusing the user.

## Code quality

### Test coverage
The only test is an empty placeholder. Priority areas for unit tests:
- `PagedRequest` pagination logic (mock the API, verify all pages are consumed).
- `get_playlist_ids_from_names` — verify behaviour when a name is missing.
- `overflow` logic — verify the 5000 cap is respected and videos are added before deleted.

### Type annotations
Many utility functions lack return-type annotations (e.g. `get_all_items`, `get_items_from_playlist_names`). Adding them would let mypy catch more issues.

### Magic number 5000
The playlist limit in `overflow` is a bare literal. Extract it to a constant in `constants.py` (e.g. `MAX_PLAYLIST_ITEMS = 5000`).

### Duplicate deletion logic
`cleanup` and `remove_unavailable_from_all_playlists` share nearly identical loops for detecting deleted/private videos. Extract the shared logic into a helper in `util.py`.

### `subprocess` call in `get_video_metadata`
Calling `yt-dlp` via `subprocess.run` works but is fragile. The `yt-dlp` Python package exposes `yt_dlp.YoutubeDL` which can be used directly, avoiding shell escaping issues and giving structured output natively.
