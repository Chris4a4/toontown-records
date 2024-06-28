from collections import Counter
from .records import get_record_data, get_top_N
from fastapi import APIRouter

records_router = APIRouter()


@records_router.get('/api/records/get_all_record_infos')
async def get_all_record_infos():
    return get_record_data()


@records_router.get('/api/records/get_all_records')
async def get_all_records():
    records = get_record_data()
    for record in records:
        record['top3'] = get_top_N(record, 3)

    return records


@records_router.get('/api/records/get_leaderboards')
async def get_leaderboards():
    ttr_counter = Counter()
    ttcc_counter = Counter()

    # Accumulate points for each record defined in records.yaml
    records = get_record_data()
    for record in records:
        points = record['points']
        tags = record['tags']

        # Get the best placement if it exists
        best = get_top_N(record, 1)
        if not best:
            continue
        best = best[0]

        # Loop through users and add points for them
        users = best['user_ids']
        for user in users:
            if 'ttr' in tags:
                ttr_counter.update({user: points})
            elif 'ttcc' in tags:
                ttcc_counter.update({user: points})

    return {
        'ttr': dict(ttr_counter),
        'ttcc': dict(ttcc_counter),
        'all': dict(ttr_counter + ttcc_counter)
    }

