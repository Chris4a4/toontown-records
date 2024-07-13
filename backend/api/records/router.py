from api.leaderboards.router import get_top_N
from .records import lookup_all_record_info, lookup_record_info
from fastapi import APIRouter
from copy import deepcopy
from pydantic import BaseModel
from typing import List

records_router = APIRouter()


# Gets the record information for a given record
@records_router.get('/api/records/get_info/{record_name}', tags=['Unlogged'])
async def get_record_info(record_name: str):
    record_data = lookup_record_info(record_name)

    if record_data:
        return {
            'success': True,
            'message': 'Got record information',
            'data': record_data
        }

    return {
        'success': False,
        'message': 'Could not find given record',
        'data': None
    }


# Gets the record information for every record
@records_router.get('/api/records/get_all_info', tags=['Unlogged'])
async def get_all_record_info():
    all_data = lookup_all_record_info()

    return {
        'success': True,
        'message': 'Got data for all records',
        'data': all_data
    }


# Gets the record information and top3 information for every record
@records_router.get('/api/records/get_all_records', tags=['Unlogged'])
async def get_all_records():
    records = deepcopy(lookup_all_record_info())
    for record in records:
        record['top3'] = get_top_N(record['record_name'], 3)

    return {
        'success': True,
        'message': 'Got all record data',
        'data': records
    }


class Tags(BaseModel):
    tags: List[str | int]

# Gets the record information and top3 information for record matching tags
@records_router.post('/api/records/get_records_with_tags', tags=['Unlogged'])
async def get_records_with_tags(data: Tags):
    result = []
    for record in lookup_all_record_info():
        if set(record['tags']) == set(data.tags) | set(record['tags']):
            modified_record = deepcopy(record)

            modified_record['top3'] = get_top_N(record['record_name'], 3)
            result.append(modified_record)

    return {
        'success': True,
        'message': 'Got data for records with tags',
        'data': result
    }
