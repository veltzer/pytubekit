# Suggestions for pytubekit (round 2)

## New commands

### `create_playlist`
Create a new empty playlist by name. Currently the only way to create playlists is through the YouTube UI. Uses `playlists().insert()`.

### `delete_playlist`
Delete a playlist entirely (not just clear its items). Uses `playlists().delete()`.

### `intersect`
Given two or more playlists, output the video IDs that appear in all of them. The inverse of `subtract` — useful for finding overlap between playlists.

### `stats`
Print a summary of the account: total playlists, total videos across all playlists, largest and smallest playlists. A quick health-check command.

### `dump_single`
Dump a single named playlist to a file (like `dump` but for one playlist instead of all). Currently `dump` always dumps everything. Mentioned in `TODO.txt` as "implement argument free dump" (the other direction — dump a specific one by name).

### `reverse_playlist`
Reverse the order of items in a playlist. Similar to `sort_playlist` but simpler — just flip the order. Useful when YouTube imports add items in the wrong direction.

## Improvements to existing commands

### `get_watch_later_playlist_id` description is wrong
The description says "Show me my channel id" (copy-paste from `get_channel_id`). Should say "Show the Watch Later playlist id".

### `remove_unavailable_from_all_playlists` has a typo in description
The description says "unavialable" instead of "unavailable".

### `add_file_to_playlist` should skip duplicates
Currently it blindly adds every ID from the file. If a video is already in the playlist, YouTube will add a duplicate. The command should optionally (or by default) fetch existing video IDs and skip duplicates.

### `copy_playlist` should skip duplicates
Same issue — if the destination already has some of the source videos, they get duplicated. `merge` already handles this; `copy_playlist` should too.

### `sort_playlist` is destructive on failure
If the process crashes after deleting items but before re-adding them, items are lost. A safer approach: first add all items in the new order to a temporary playlist, then clear the original and copy back — or at least warn the user and require a `--force` flag.

### `count` should use `contentDetails.itemCount`
The `count` command currently fetches all items via `get_playlist_item_count` (which calls `get_all_items_from_playlist_id`) just to count them. The YouTube API returns `contentDetails.itemCount` in the `playlists().list()` response, which is a single API call instead of potentially hundreds of paginated calls.

### `playlists` should show item counts
The `playlists` command currently only shows playlist names. Adding the item count (from `contentDetails.itemCount`) would be more useful and costs no extra API calls since it just requires adding `contentDetails` to the `part` parameter.

## Packaging and dependencies

### Drop `youtube-dl` dependency
`pyproject.toml` still lists `youtube-dl` as a dependency. All code has been migrated to `yt-dlp`, but the dependency was never removed. It should be replaced with `yt-dlp`.

### Drop `browsercookie` dependency
`browsercookie` is listed in `pyproject.toml` dependencies but is never imported anywhere in the source code. Remove it.

### Drop `pyvardump` dependency
`pyvardump` is listed in dependencies and has a commented-out import in `main.py` (`# import pyvardump`). If it is not used, remove the dependency and the dead comment.

## Code quality

### Better error message for missing playlist names
`get_playlist_ids_from_names` raises a bare `KeyError` when a playlist name is not found. Wrapping this in a user-friendly message (e.g. "Playlist 'xyz' not found. Available playlists: ...") would save debugging time.

### `main` function missing return type
The `main()` function at the bottom of `main.py` is the only endpoint function without a `-> None` return type annotation.

### Unused imports in `main.py`
`main.py` imports `string` and `time` at the top level. `string` is only used in `dump()` and `time` is only used in `dump()`. These are fine but worth noting — more importantly, `pathlib` is imported but could replace several `os.path` calls for consistency.

### `json` import no longer needed in `util.py`
After migrating `get_video_metadata` from subprocess+JSON parsing to the `yt_dlp` Python API, the `json` module is only used by `pretty_print` (via `json.dump`). This is fine, but worth auditing whether any other dead imports crept in.

### Validate playlist name exists before expensive operations
Commands like `sort_playlist`, `clear_playlist`, and `overflow` resolve playlist names to IDs and then immediately start fetching/deleting. If the name is wrong, the error comes late. Validating upfront (or using the improved error message above) would catch mistakes faster.
