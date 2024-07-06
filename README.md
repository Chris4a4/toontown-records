# toontown-records
Database + Backend + Discord Bot and Web frontends

known issue: not checking the lengths of embeds

## Install/Run (requires docker installed):

1. Pull the github repository
```
git pull https://github.com/Chris4a4/toontown-records
```

2. Add in local config
Create a file named private_config.yaml at toontown-records/bot/private_config.yaml:
```
WELCOME_CHANNEL: 1257178370408583288
GUILD: 1254667676630913044
AUTHORIZED_ROLE: basic rights
TOKEN: token
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
