# xenylist

A self-hosted anime/manga tracker that allows you to track your anime/manga on your desktop. It was created as an alternative to AniList and MyAnimeList because of their slow servers and outdated UI.

## Features

- Track anime/manga on your desktop
- List editing and filtering
- Importing lists from AniList
- Lightweight and easy to set up
- Open-source

## Images

<img src="https://user-images.githubusercontent.com/44981148/189462374-8232d4dc-8689-4af5-8134-7e4e480bcf15.png" />
<img src="https://user-images.githubusercontent.com/44981148/189462434-669836df-baf8-4f35-bb6a-15db68af209f.png"/>

## Installation

1. Clone the repo to a server or your local machine: `git clone https://github.com/1x6/xenylist.git && cd xenylist`
2. Install sqlite3: `sudo apt install sqlite3`
3. Import your lists using `import_from_anilist.py` (make sure to edit the hard-coded variables)
4. Install the python requirements: `pip install -r requirements.txt`
5. Run `server.py`
6. Done!

## Support

If you have any questions or need support, please contact me at https://xeny.uk

## Additional Information

If you are running xenylist on a cloud server, consider adding password protection using nginx. Authentication is planned for future releases.

For SSL, you can use the Cloudflare proxying feature, which automatically provisions a free SSL cert. Alternatively, you can use certbot.

I run this on a Raspberry Pi on my local network to prevent bad actors from accessing it.

## To-do

- Alert when a list is already in the list
- Password authentication for exposed instances
- Improved CSS
- Account system (?)

## Disclaimer

xenylist is not intended to infringe on any copyrights. The stored list data is scraped from AniList, which may be against their API terms of service as xenylist could be considered as a "competing non-complementary service of the same nature". However, please note that the worst that can happen is that your IP will be banned from the AniList API.

As always, please use this software at your own risk. It was created for educational purposes and is only an anime tracker.
