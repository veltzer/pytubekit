# TOFIX

Findings from a code scan on 2026-10-04.

## High

- `src/pytubekit/youtube.py:16-19` - `watch_later` (`src/pytubekit/main.py:686`) relies on `"usenetrc": True` to log in, but the bundled yt-dlp ignores password login for YouTube ("Login with password is not supported for YouTube", `yt_dlp/extractor/youtube/_base.py:690-696`), so the private `list=WL` playlist cannot be read; and `"extract_flat": True` means nothing is downloaded even when it is. Use yt-dlp's `cookiesfrombrowser`/`cookiefile` option and drop `extract_flat` (or rename the command to what it does).
- `sphinx/cli-reference.rst:343-349` (and ~100 other flags there, `doc/CLI.md`, `doc/OVERVIEW.md:53`, `sphinx/overview.rst:64`) - documented flag syntax does not parse: `--cleanup-names "A" "B"` gives "unknown flags [cleanup-names]", `--no-dedup` gives "argument [no-dedup] needs a follow-up argument"; pytconf actually takes `--cleanup_names=A,B` and `--dedup=false`. Rewrite the examples in the real syntax.

## Medium

- `CLAUDE.md:35` - says mutating commands are dry-run by default and need `--do-delete`, but `src/pytubekit/configs.py:86-89` defaults `do_delete` to `True`, so `cleanup`, `subtract`, `clear_playlist` mutate immediately; decide which is intended (a dry-run default is the safer one) and make code and docs agree.
- `doc/CLI.md:19-25`, `doc/CLI.md:31-45`, `doc/CLI.md:118-134` - document `get_watch_later_playlist_id`, `playlists` and `remove_unavailable_from_all_playlists`, none of which exist any more (now `get_channel_id --watch-later` and `cleanup` with no names), while `merge`, `diff`, `stats`, `overflow`, `sort_playlist` and a dozen other real commands are missing; regenerate it from `pytubekit` usage or delete it in favour of `sphinx/cli-reference.rst`.
- `doc/OVERVIEW.md:47` and `sphinx/overview.rst:58` - Quick Start's first example is `pytubekit playlists`, a command that no longer exists.
- `pyproject.toml:41` - `browsercookie` is a runtime dependency but is imported nowhere in `src/`; remove it (or actually use it for the Watch Later cookie problem above).
- `CLAUDE.md:25`, `doc/DEVELOPMENT.md:17`, `doc/DEVELOPMENT.md:33`, `doc/DEVELOPMENT.md:42`, `doc/ARCHITECTURE.md:137`, `doc/ARCHITECTURE.md:146`, `sphinx/development.rst:21-50`, `sphinx/architecture.rst:216-227` - say the build runs `pylint` with a `.pylintrc`; `rsconstruct.toml` has no pylint processor and there is no `.pylintrc`; drop pylint from the docs.
- `sphinx/architecture.rst:90`, `sphinx/architecture.rst:104`, `sphinx/architecture.rst:106` - list config classes `ConfigCopy`, `ConfigLeftToSee`, `ConfigCount` that do not exist in `src/pytubekit/configs.py`; update the table.
- `doc/DEVELOPMENT.md:14-17` - dev setup uses `python -m venv` + `pip install -e .` + an ad-hoc `pip install` of tools, bypassing `uv.lock` and the `[dependency-groups] dev` group; replace with `uv sync`.
- `rsconstruct.toml:67` and `rsconstruct.toml:71` - `ruff` and `mypy` list `config` in `src_dirs`, but `config/` holds only `.lua` files; drop `config`.

## Low

- `CLAUDE.md:31` - tells readers to ignore a "black" badge in the README; the README has no black badge any more; delete the sentence.
- `src/pytubekit/util.py:423` - `# pylint: disable=broad-exception-caught` is a leftover suppression for a linter this repo no longer runs; keep only the `noqa`.
- `doc/suggestions.md:5-52` - most items are done or obsolete (`create_playlist`, `delete_playlist`, `stats` exist; `get_watch_later_playlist_id`, `remove_unavailable_from_all_playlists`, `copy_playlist`, `count`, `playlists` no longer exist; `youtube-dl` is no longer a dependency); prune the list.
- `hatch_build.py:9-13` - the docstring says sources are tried in order env var, config dir, then in-tree copy, but `initialize` checks the in-tree copy first (`hatch_build.py:32-33`); fix the docstring order.
