# API Quota Guide

The YouTube Data API v3 enforces a daily quota of **10,000 units**. Every API call
costs a certain number of units, and once the quota is exhausted you must wait
until the next day (Pacific Time) for it to reset. This page explains how
pytubekit commands consume quota and what you can do to stay within the limit.

## Quota costs per API method

| API method | Cost (units) | pytubekit usage |
|------------|:------------:|-----------------|
| `playlists.list` | 1 | Listing playlists, resolving names to IDs |
| `playlistItems.list` | 1 | Fetching items from a playlist (per page) |
| `playlistItems.insert` | 50 | Adding a video to a playlist |
| `playlistItems.delete` | 50 | Removing a video from a playlist |
| `playlists.insert` | 50 | Creating a new playlist |
| `playlists.delete` | 50 | Deleting a playlist |
| `playlists.update` | 50 | Renaming a playlist |
| `channels.list` | 1 | Fetching channel info |
| `videos.list` | 1 | Fetching video info |

**Key takeaway:** Read operations (`*.list`) cost 1 unit per page, while write
operations (`*.insert`, `*.delete`, `*.update`) cost 50 units each.

## Command quota profiles

### Low-cost commands (read-only)

These commands only call `*.list` methods — typically a few units total.

| Command | Approximate cost |
|---------|:----------------:|
| `playlists` | 1 per page of playlists |
| `stats` | 1 per page of playlists |
| `get_channel_id` | 1 |
| `channels` | 2–3 |
| `count` | 1 per page of playlists + 1 per page per counted playlist |
| `video_info` | 1 |

### Medium-cost commands (read-heavy)

These iterate playlist items. Cost depends on playlist size — each page of 50
items is 1 unit plus 1 per page to resolve playlist names.

| Command | Approximate cost |
|---------|:----------------:|
| `playlist` | 1 (name lookup) + 1 per page of items |
| `dump` | 1 per page of playlists + 1 per page per playlist |
| `export_csv` | 1 (name lookup) + 1 per page of items |
| `search_playlist` | 1 (name lookup) + 1 per page per searched playlist |
| `find_video` | 1 per page of playlists + 1 per page per playlist (worst case) |
| `left_to_see` | name lookups + 1 per page per playlist |
| `diff` | name lookups + 1 per page per playlist |

### High-cost commands (write-heavy)

Each inserted or deleted item costs 50 units. A playlist of 200 videos that gets
cleared consumes **10,000 units** — your entire daily quota.

| Command | Approximate cost |
|---------|:----------------:|
| `cleanup` | reads + 50 per deleted item |
| `remove_unavailable_from_all_playlists` | reads + 50 per deleted item |
| `subtract` | reads + 50 per deleted item |
| `clear_playlist` | reads + 50 × playlist size |
| `copy_playlist` | reads + 50 × playlist size |
| `merge` | reads + 50 per new item added |
| `sort_playlist` | reads + 50 × size (delete all) + 50 × size (re-add) = **100 × size** |
| `overflow` | reads + 50 per moved item (insert + delete = 100 per item) |
| `add_file_to_playlist` | reads + 50 per video added |
| `create_playlist` | 50 |
| `delete_playlist` | 1 (name lookup) + 50 |
| `rename_playlist` | 1 (name lookup) + 50 |

## Strategies to reduce quota usage

### 1. Use `--page-size 50` (the default)

The API returns at most 50 items per page. Using a smaller `--page-size` means
more pages and more API calls for the same data. Keep it at 50 unless you have a
specific reason to lower it.

### 2. Prefer `stats` and `count` over `playlist` for size checks

`stats` and `count` read the `itemCount` field from the playlist metadata — no
need to iterate every item. Use them instead of fetching full playlist contents
when you only need counts.

### 3. Use `dump` for offline analysis

Run `dump` once to save all playlists to local files, then work with the files
locally (search, diff, grep) instead of repeatedly querying the API.

### 4. Use `diff` with local files instead of repeated API calls

After dumping, use `diff --seen-files` with your local dump files to compare
playlists without fetching them again.

### 5. Run `cleanup` on specific playlists, not all

`remove_unavailable_from_all_playlists` iterates every playlist you own and
deletes items from each. If you know which playlists have problems, target them
with `cleanup --cleanup-names` instead.

### 6. Avoid `sort_playlist` on large playlists

Sorting deletes every item and re-adds them in order. A 200-item playlist costs
200 × 100 = **20,000 units** (twice your daily quota). Consider whether sorting
is truly necessary, or sort locally in an exported CSV.

### 7. Use dry-run mode before committing

Many write commands support `--no-do-delete` for a dry run. Use it first to
verify what would happen, then run the real operation only when you're sure.

```bash
# See what would be deleted without spending write quota
pytubekit cleanup --cleanup-names "My Playlist" --no-do-delete

# Then actually do it
pytubekit cleanup --cleanup-names "My Playlist"
```

### 8. Batch your work across days

If you need to perform large write operations (clearing, sorting, or merging big
playlists), split the work across multiple days. For example, clear one large
playlist per day rather than all at once.

### 9. Use `collect_ids` and `add_data` offline

`collect_ids` works entirely on local files — zero API cost. `add_data` uses
yt-dlp instead of the YouTube Data API, so it does not consume your API quota at
all.

### 10. Use `local_*` commands after `dump`

After running `dump` once, use the `local_*` family of commands to search, diff,
count, and deduplicate entirely offline. These commands read the dump files
directly and make zero API calls:

```bash
# Dump once (costs API quota)
pytubekit dump --dump-folder ~/youtube-dump

# All subsequent analysis is free
pytubekit local_count --local-dump-folder ~/youtube-dump
pytubekit local_find_video --local-dump-folder ~/youtube-dump --local-video-id dQw4w9WgXcQ
pytubekit local_search --local-dump-folder ~/youtube-dump --local-search-pattern "python"
pytubekit local_dedup --local-dump-folder ~/youtube-dump
pytubekit local_diff --local-diff-a ~/youtube-dump --local-diff-b ~/seen-dump
pytubekit local_left_to_see --local-lts-all-folder ~/youtube-dump --local-lts-seen-folder ~/seen-dump
```

### 11. Monitor usage in the Google Cloud Console

Check your current quota usage at any time:

1. Open the [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services** > **Dashboard**
3. Select **YouTube Data API v3**
4. View the **Quotas** tab

This shows real-time usage and lets you plan operations around remaining budget.

## Quick-reference: zero-quota commands

These commands do not call the YouTube Data API at all:

| Command | Why it's free |
|---------|---------------|
| `collect_ids` | Scans local files only |
| `add_data` | Uses yt-dlp, not the API |
| `watch_later` | Uses yt-dlp, not the API |
| `local_find_video` | Reads dump files only |
| `local_search` | Reads dump files only |
| `local_count` | Reads dump files only |
| `local_diff` | Reads dump files only |
| `local_left_to_see` | Reads dump files only |
| `local_dedup` | Reads dump files only |
