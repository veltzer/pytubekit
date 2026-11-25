:orphan:

Privacy policy
==============

*Last updated: 2026-11-25*

pytubekit is a command-line program that runs on your own computer. It uses
Google's OAuth to access your YouTube account (playlists, subscriptions and videos), with this permission:

- ``https://www.googleapis.com/auth/youtube``, ``youtube.force-ssl`` and ``youtube.readonly`` (manage your YouTube account)

What it does with your data
---------------------------

- Your your YouTube account (playlists, subscriptions and videos) is read and changed only on your computer, by the commands you
  run. Nothing is sent to the author of pytubekit or to anyone else; there is no
  pytubekit server.
- The OAuth token Google issues is stored on your computer (in your pass(1)
  store or under ``~/.config/google_tokens/``) and is used only to talk to
  Google's API. Delete it, or revoke access at
  https://myaccount.google.com/permissions, to stop pytubekit using your account.
- pytubekit does not collect analytics, does not share, sell or transfer data, and
  does not use Google user data to train AI or machine-learning models.

pytubekit's use of information received from Google APIs adheres to the
`Google API Services User Data Policy
<https://developers.google.com/terms/api-services-user-data-policy>`_,
including the Limited Use requirements.

Contact
-------

Mark Veltzer, mark.veltzer@gmail.com. Source code:
https://github.com/veltzer/pytubekit
