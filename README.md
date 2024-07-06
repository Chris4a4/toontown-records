# Toontown Records
Database, API, Discord Bot, and Website for Toontown Records project.

Discord: 

Website: 

## Install/Run (requires docker installed):

1. Clone the github repository
```
git clone https://github.com/Chris4a4/toontown-records
```

2. Create a file for installation-specific information at ``toontown-records/bot/private_config.yaml``. Be sure to change token to the bot's actual token:
```
SUBMIT_CHANNEL_ID: 1254667676630913047
WELCOME_CHANNEL_ID: 1259239130068553810
GUILD: 1254667676630913044
AUTHORIZED_ROLE: basic rights
TOKEN: asdf
```

3. Run docker-compose in the toontown-records directory
```
docker-compose up --build
```

## Creating the Virtual Environment on Windows
Attaching your code editor to this virtual environment will let it understand non-base packages. Although this isn't necessary for anything to run, it helps with debugging.

Run these commands in powershell at the toontown-records directory:
```
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
./setup-venv.ps1
```

## Known Issues

- Not checking the length of messages/embeds.