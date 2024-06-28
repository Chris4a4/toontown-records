from fastapi import FastAPI
from api.records.router import records_router
from api.submissions.router import submissions_router
from api.users.router import users_router

app = FastAPI()


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
        'name': 'Users',
        'description': 'Provides functions to manage usernames',
    }
]

app = FastAPI(openapi_tags=tags_metadata,
              title='Toontown Records Backend',
              description='FastAPI backend for Toontown Records website and Discord bot',
              version='0.0.1'
              )
app.include_router(records_router, tags=['Records'])
app.include_router(submissions_router, tags=['Submissions'])
app.include_router(users_router, tags=['Users'])
