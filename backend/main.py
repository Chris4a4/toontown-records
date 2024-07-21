from fastapi import FastAPI

from api.records.router import records_router
from api.submissions.router import submissions_router
from api.accounts.router import accounts_router
from api.namechange.router import namechange_router
from api.logging.router import logging_router
from api.leaderboards.router import leaderboards_router
from api.oauth.router import oauth_router


tags_metadata = [
    {
        'name': 'Records',
        'description': 'Provides information about the supported records',
    },
    {
        'name': 'Submissions',
        'description': 'Provides functions to submit, edit, and view record objects',
    },
    {
        'name': 'Accounts',
        'description': 'Provides functions to query account information',
    },
    {
        'name': 'Namechanges',
        'description': 'Provides functions to request/view/approve/deny namechanges',
    },
    {
        'name': 'Leaderboards',
        'description': 'Allows fetching and updating of leaderboards from database',
    },
    {
        'name': 'Logging',
        'description': 'Allows the retrieval of logs from the database',
    },
    {
        'name': 'Oauth2',
        'description': 'Allows Discord oauth2 token/code management',
    },
    {
        'name': 'Logged',
        'description': 'These endpoints require a user interaction and are logged. audit_id is the discord id of the user interacting with the endpoint',
    },
    {
        'name': 'Unlogged',
        'description': 'These endpoints do not require a user interaction and are not logged',
    }
]

app = FastAPI(openapi_tags=tags_metadata,
              title='Toontown Records Backend',
              description='FastAPI backend for Toontown Records website and Discord bot',
              version='0.0.1'
              )
app.include_router(records_router, tags=['Records'])
app.include_router(submissions_router, tags=['Submissions'])
app.include_router(accounts_router, tags=['Accounts'])
app.include_router(namechange_router, tags=['Namechanges'])
app.include_router(leaderboards_router, tags=['Leaderboards'])
app.include_router(logging_router, tags=['Logging'])
app.include_router(oauth_router, tags=['Oauth2'])
