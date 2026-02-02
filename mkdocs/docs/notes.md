# Notes

Miscellaneous design notes, reference links, test data, and ideas for future work.

## API Quota

The YouTube Data API v3 has a 10,000 API calls/day quota limit. If you hit it, wait a day to continue working.

References:

- <https://developers.google.com/youtube/v3/getting-started>

## Design Notes

- Marking all elements of a list as "seen" appears to be impossible via the YouTube API.
- **Deleted video:** A video with the title `"Deleted video"`, or one whose details request returns an empty `items` array.
- **Private video:** A video with the title `"Private video"`.

## Reference Links

YouTube API documentation:

| Resource | URL |
|----------|-----|
| Home | <https://developers.google.com/youtube/v3> |
| Python quickstart | <https://developers.google.com/youtube/v3/quickstart/python> |
| Reference docs | <https://developers.google.com/youtube/v3/docs> |
| Getting started | <https://developers.google.com/youtube/v3/getting-started> |

Other useful references:

- [Gist: remove videos from Watch Later](https://gist.github.com/astamicu/eb351ce10451f1a51b71a1287d36880f)

## Test Video IDs

For manual testing:

| Type | Video ID |
|------|----------|
| Regular video | `xL_sMXfzzyA` |
| Deleted video | `6k2nFwVqQFw` |
| Private video | `MZnlL8uCCU0` |

## TODO / Future Ideas

- Implement a single playlist dump that includes video metadata (not just IDs).
- Investigate "saw1" playlist showing unavailable videos in the YouTube UI even after cleanup.
- Since the Watch Later playlist can't be accessed via the API, explore browser-based scraping approaches.
    - Reference: <https://github.com/longpdo/youtube-dl-watch-later-playlist>
- Implement argument-free dump.
- Find how to list "builtin" playlists (e.g. "Watch Later") and clean them up.
- Download a channel's full video list so you can subtract already-watched videos and get a "left to see" list.

Features to implement:

- Download Watch Later
- Clear Watch Later
- Add list to list
- Add file to list
- Clear list
