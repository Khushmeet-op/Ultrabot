# Ultra - UserBot
A stable pluggable Telegram userbot, based on Telethon.

<p align="center">
  <img src="https://telegra.ph/file/40a9824c3ba55ccfae9a0.jpg">
</p>

[![Stars](https://img.shields.io/github/stars/TeamUltroid/Ultroid?style=social)](https://github.com/Khushmeet-op/Ultrabot)
[![Forks](https://img.shields.io/github/forks/TeamUltroid/Ultroid?style=social)](https://github.com/Khushmeet-op/Ultrabot)
[![Python Version](https://img.shields.io/badge/Python-v3.9-blue)](https://www.python.org/)
[![Contributors](https://img.shields.io/github/contributors/TeamUltroid/Ultra)](https://github.com/Khushmeet-op/Ultrabot)
[![License](https://img.shields.io/badge/License-AGPL-blue)](https://github.com/TeamUltroid/Ultroid/blob/main/LICENSE)
[![Size](https://img.shields.io/github/repo-size/Khushmeet-op/ultrabot)](https://github.com/Khushmeet-op/Ultrabot)

<details>
<summary>More Info</summary>
<br>
  Documentation soon..  <br />
</details>

# Deploy 
- [Heroku](https://github.com/Khushmeet-op/Ultrabot#Deploy-to-Heroku)
- [Local Machine](https://github.com/Khushmeet-op/Ultrabot#Deploy-Locally)

## Deploy to Heroku
- Get your `API_ID` and `API_HASH` from [here](https://my.telegram.org/)    
- Get your `SESSION` from [here](https://repl.it/@TeamUltroid/UltroidStringSession#main.py).   
and click the below button!  <br />  

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Deploy Locally
- Get your `API_ID` and `API_HASH` from [here](https://my.telegram.org/)
- Get your `REDIS_URI` and `REDIS_PASSWORD` from [here](https://redislabs.com), tutorial [here](./resources/extras/redistut.md).
- Clone the repository: <br />
`git clone https://github.com/TeamUltroid/Ultroid.git`
- Go to the cloned folder: <br />
`cd Ultroid`
- Create a virtual env:   <br />
`virtualenv -p /usr/bin/python3 venv`   
`. ./venv/bin/activate`
- Install the requirements:   <br />
`pip install -r requirements.txt`   
- Generate your `SESSION`:   
`bash sessiongen`
- Fill your details in a `.env` file, as given in [`.env.sample`](https://github.com/TeamUltroid/Ultroid/blob/main/.env.sample).    
(You can either edit and rename the file or make a new file.)
- Run the bot:   
`bash resources/startup/startup.sh`

Made with 💕 by [@Khushmeet1](https://t.me/Khushmeet1). <br />

