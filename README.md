# xenylist

An almost self-hosted anime/manga tracker.

Made this because AniList's mods continued banning me, and I couldn't cope with MyAnimeList's slow servers & outdated UI.

## Features:

- Track Anime/Manga on your desktop
- List editing, filters
- Importing list from AniList
- Lightweight, easy to set up
- Open source

## Images

<img src="https://user-images.githubusercontent.com/44981148/189462374-8232d4dc-8689-4af5-8134-7e4e480bcf15.png" />
<img src="https://user-images.githubusercontent.com/44981148/189462434-669836df-baf8-4f35-bb6a-15db68af209f.png"/>

## Installation

- Clone the repo to a server (or your local machine)
  `git clone https://github.com/1x6/xenylist && cd xenylist`
- Create a [free MongoDB database](https://www.mongodb.com/cloud/atlas/) and put the link in config.json
- Import your lists using `import_from_anilist.py`
- Install the python requirements with `pip install -r requirements.txt`
- Edit the 'endpoint' variable of the files in `frontend/static/js/` to your server's ip
- Run `server.py`
- Done!

## Support

If you have questions or want reasonable support, drop me a DM on discord @ `xeny#0095`.

## Other info

If you are running this on a cloud server, consider adding password protection using nginx. Authentication coming eventually.

For SSL, you can use the Cloudflare proxying feature, which automatically provisions a free SSL cert. You can also use certbot if you'd prefer that.

I run this on a Raspberry Pi on my local network, so no bad actors can touch it.

## To-do:

- Password authentication for exposed instances
- Improved CSS
- Account system (?)

## Disclaimers

No copyright infringement intended with the name or logo of 'xenylist'. Stored list data is scraped from AniList. This may be against their API terms of service, as _xenylist_ could be considered as a 'competing non-complementary services of the same nature'. Even so, what are they going to do? IP ban you from their API? 🙀

As always, the standard applies:

> USE THis AT YoUR OwN riSk. thIS waS madE fOR eDUCatiOnaL pURPOseS.
> or smth.. it's just an anime tracker??
