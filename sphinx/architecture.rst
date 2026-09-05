Architecture
============

Project Structure
-----------------

::

   pytubekit/
   ├── src/pytubekit/          # Main package
   │   ├── __init__.py         # Module init, defines LOGGER_NAME
   │   ├── main.py             # CLI entry point and all command endpoints
   │   ├── configs.py          # Configuration classes for CLI parameters
   │   ├── constants.py        # API constants, scopes, and sentinel values
   │   ├── static.py           # Version string, description, app name
   │   ├── util.py             # YouTube API utility functions
   │   └── youtube.py          # yt-dlp integration
   ├── config/                 # Project metadata for the tera templates (lua)
   │   ├── project.lua         # Project name, description, keywords
   │   ├── version.lua         # Version tuple
   │   └── personal.lua        # Author information
   ├── tera.templates/         # Tera templates for README.md and static.py
   ├── tests/                  # Test suite
   │   └── unit_tests/
   │       └── test_basic.py   # Placeholder test
   ├── doc/                    # Documentation source files
   ├── mkdocs/                 # MkDocs documentation site
   ├── pyproject.toml          # PEP 517/518 project metadata
   ├── rsconstruct.toml        # Build automation (rsconstruct)
   └── uv.lock                 # Pinned dependency closure

Module Descriptions
-------------------

.. _mainpy:

``main.py``
~~~~~~~~~~~

The application entry point. Contains:

- All CLI command functions decorated with ``@register_endpoint``
- The ``main()`` function decorated with ``@register_main``
- Uses the ``pytconf`` framework for CLI argument parsing and dispatch

The ``main()`` function:

1. Sets up logging via ``pylogconf``
2. Configures OAuth2 scopes and credential location
3. Registers helper functions from ``pygooglehelper``
4. Launches the argument parser to dispatch to the selected endpoint

.. _configspy:

``configs.py``
~~~~~~~~~~~~~~

Declarative configuration classes using ``pytconf.Config`` and ``pytconf.ParamCreator``. Each class maps to a set of CLI parameters:

+-----------------------------+-----------------------------------------------------+
| Config Class                | Purpose                                             |
+=============================+=====================================================+
| ``ConfigPagination``        | API pagination page size                            |
+-----------------------------+-----------------------------------------------------+
| ``ConfigDump``              | Output folder for dump command                      |
+-----------------------------+-----------------------------------------------------+
| ``ConfigSubtract``          | Playlist names for subtraction                      |
+-----------------------------+-----------------------------------------------------+
| ``ConfigPlaylist``          | Single playlist selection (by name or ID)           |
+-----------------------------+-----------------------------------------------------+
| ``ConfigVideo``             | Single video ID                                     |
+-----------------------------+-----------------------------------------------------+
| ``ConfigPlaylists``         | Multiple playlist names                             |
+-----------------------------+-----------------------------------------------------+
| ``ConfigCleanupPlaylists``  | Playlist names for cleanup                          |
+-----------------------------+-----------------------------------------------------+
| ``ConfigDelete``            | Delete confirmation flag                            |
+-----------------------------+-----------------------------------------------------+
| ``ConfigCleanup``           | Cleanup behavior flags (dedup, deleted, privatized) |
+-----------------------------+-----------------------------------------------------+
| ``ConfigPrint``             | Output format (full JSON vs IDs only)               |
+-----------------------------+-----------------------------------------------------+
| ``ConfigDiff``              | Source playlists and seen files for diffing         |
+-----------------------------+-----------------------------------------------------+
| ``ConfigAddData``           | Input/output files for metadata enrichment          |
+-----------------------------+-----------------------------------------------------+
| ``ConfigOverflow``          | Source and destination for overflow moves           |
+-----------------------------+-----------------------------------------------------+
| ``ConfigCopy``              | Source and destination for playlist copy            |
+-----------------------------+-----------------------------------------------------+
| ``ConfigClear``             | Playlist name for clearing                          |
+-----------------------------+-----------------------------------------------------+
| ``ConfigMerge``             | Source playlists and destination for merge          |
+-----------------------------+-----------------------------------------------------+
| ``ConfigSort``              | Playlist name and sort key                          |
+-----------------------------+-----------------------------------------------------+
| ``ConfigSearch``            | Playlists and query for searching                   |
+-----------------------------+-----------------------------------------------------+
| ``ConfigExportCsv``         | Playlist name and CSV path for export               |
+-----------------------------+-----------------------------------------------------+
| ``ConfigRename``            | Old and new playlist names                          |
+-----------------------------+-----------------------------------------------------+
| ``ConfigLeftToSee``         | All-videos and seen playlists                       |
+-----------------------------+-----------------------------------------------------+
| ``ConfigCount``             | Playlist names for counting                         |
+-----------------------------+-----------------------------------------------------+
| ``ConfigCollectIds``        | Files to scan for video IDs                         |
+-----------------------------+-----------------------------------------------------+
| ``ConfigAddFileToPlaylist`` | File path and playlist for bulk add                 |
+-----------------------------+-----------------------------------------------------+

.. _constantspy:

``constants.py``
~~~~~~~~~~~~~~~~

Static constants:

- **SCOPES** - OAuth2 scopes for YouTube API access
- **API_SERVICE_NAME** / **API_VERSION** - YouTube API service identifiers (``youtube``, ``v3``)
- **MAX_PLAYLIST_ITEMS** - YouTube's 5,000-item playlist limit
- **NEXT_PAGE_TOKEN** / **PAGE_TOKEN** / **ITEMS_TOKEN** - API response field names for pagination
- **DELETED_TITLE** / **PRIVATE_TITLE** - Sentinel strings (``"Deleted video"``, ``"Private video"``) used to identify unavailable videos

.. _utilpy:

``util.py``
~~~~~~~~~~~

Core utility layer between the CLI endpoints and the YouTube API:

- **``PagedRequest``** - A class that wraps paginated YouTube API calls. Handles ``nextPageToken`` iteration and collects all results across pages via ``get_all_items()``.
- **``get_youtube()``** - Initializes an authenticated YouTube API client using OAuth2 credentials from ``pygooglehelper``.
- **``create_playlists_request()``** / **``create_playlist_request()``** - Factory functions that create ``PagedRequest`` objects for listing playlists or playlist items.
- **``get_playlist_ids_from_names()``** - Maps playlist names to their API IDs.
- **``get_all_items()``** - Fetches all items from a playlist specified by the ``ConfigPlaylist`` config.
- **``delete_playlist_item_by_id()``** - Deletes a single item from a playlist.
- **``get_video_info()``** - Fetches snippet, status, and content details for a video.
- **``pretty_print()``** - JSON pretty-printer.

.. _youtubepy:

``youtube.py``
~~~~~~~~~~~~~~

Thin wrapper around yt-dlp:

- **``youtube_dl_download_urls()``** - Downloads videos/playlists using yt-dlp with ``extract_flat`` mode and ``.netrc`` authentication.

.. _staticpy:

``static.py``
~~~~~~~~~~~~~

Auto-generated from ``tera.templates/src/pytubekit/static.py.tera`` by rsconstruct. Contains:

- ``VERSION_STR`` - Current version as a string
- ``DESCRIPTION`` - Project description
- ``APP_NAME`` - Application name
- ``LOGGER_NAME`` - Logger identifier

Key Design Patterns
-------------------

Pagination Abstraction
~~~~~~~~~~~~~~~~~~~~~~

The ``PagedRequest`` class in ``util.py`` encapsulates YouTube API pagination. It accepts any YouTube API list function and its keyword arguments, then iterates through pages by tracking ``nextPageToken``. This allows all endpoints to fetch complete result sets without duplicating pagination logic.

Configuration via pytconf
~~~~~~~~~~~~~~~~~~~~~~~~~

CLI parameters are defined declaratively as ``pytconf.Config`` subclasses. Each endpoint declares which config classes it uses via the ``configs`` parameter in ``@register_endpoint``. The ``pytconf`` framework handles argument parsing, validation, help generation, and populating the config class attributes.

OAuth2 Authentication
~~~~~~~~~~~~~~~~~~~~~

Authentication is handled by ``pygooglehelper``, which manages the OAuth2 flow:

1. Reads ``client_secret.json`` from ``~/.config/pytubekit/``, falling back to the copy shipped in the package
2. Opens browser for user consent on first run
3. Caches credentials for subsequent runs

Deleted/Private Video Detection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Videos are identified as deleted or private by checking their title against the sentinel strings ``"Deleted video"`` and ``"Private video"``. This is how the YouTube API reports unavailable videos in playlist item responses.

Dependencies
------------

Runtime
~~~~~~~

======================== ============================
Package                  Purpose
======================== ============================
google-api-python-client YouTube Data API v3 client
pygooglehelper           OAuth2 credential management
pytconf                  CLI configuration framework
pylogconf                Logging configuration
youtube-dl               Video/playlist downloading
browsercookie            Browser cookie extraction
======================== ============================

Development
~~~~~~~~~~~

=========== ============================
Package     Purpose
=========== ============================
pytest      Test runner
mypy        Static type checking
ruff        Linter and formatter
pylint      Code analysis
rsconstruct Build tool / code generation
hatchling   PEP 517 build backend
=========== ============================

Build System
------------

The project uses two build mechanisms:

1. **hatchling** (via ``pyproject.toml``) - Standard Python packaging for wheel/sdist builds and PyPI distribution.
2. **rsconstruct** (via ``rsconstruct.toml``) - Development workflow: runs tests, linters (ruff, pylint), type checking (mypy), and renders files from tera templates.

Run ``rsconstruct build`` to execute every check and render the templates; CI runs the same command.

Code Generation
---------------

Two files are auto-generated from tera templates in the ``tera.templates/`` directory by rsconstruct:

- ``src/pytubekit/static.py`` from ``tera.templates/src/pytubekit/static.py.tera``
- ``README.md`` from ``tera.templates/README.md.tera``

These templates pull values from the ``config/*.lua`` files to keep metadata consistent across the project.
