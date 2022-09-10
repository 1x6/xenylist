
# xenylist
An almost selfhosted anime/manga tracker. 

Made this because AniList's mods continued banning me, and I couldn't cope with MyAnimeList's slow servers & outdated UI.

## Features:
 - Track Anime/Manga on your desktop
 - List editing, filters
 - Importing list from AniList
 - Lightweight, easy to set up
 - Open source

## Images
![Anime list page](https://user-images.githubusercontent.com/44981148/189462374-8232d4dc-8689-4af5-8134-7e4e480bcf15.png)
![Add entry page](https://user-images.githubusercontent.com/44981148/189462434-669836df-baf8-4f35-bb6a-15db68af209f.png)

## Installation

 - Clone the repo to a server (or your local machine)
  `git clone https://github.com/1x6/xenylist && cd xenylist`
 - Create a [free mongodb database](https://www.mongodb.com/cloud/atlas/) and put the link in config.json
 - Import your lists using `import_from_anilist.py`
 - Install the python requirements with `pip install -r requirements.txt`
 - Edit the 'endpoint' variable of the files in `frontend/static/js/` to your server's ip
 - Run `server.py`
 - Done!

## Support
If you have questions or want reasonable support, drop me a DM on discord @ `xeny#0095`.

### Other info
If you are running this on a cloud server, consider adding password protection using nginx. authentication coming eventually.

For SSL, you can use the Cloudflare proxying feature, which automatically provisions a free SSL cert. You can also use certbot if you'd prefer that. 

I run this on a raspberry pi on my local network, so no bad actors can touch it.

### Todo:
- Password authentication for exposed instances
- Improved CSS
- Account system (?)

## Disclaimer
 Stored list data is scraped from AniList. This may be against their API terms of service as *xenylist* could be considered as a 'competing noncomplementary services of the same nature'. Even so, what are they going to do? IP ban you from their API? 🙀

As always, the standard applies:
> USE THis AT YoUR OwN riSk. thIS waS madE fOR eDUCatiOnaL pURPOseS.

