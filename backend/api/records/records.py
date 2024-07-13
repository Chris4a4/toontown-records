from itertools import product
from functools import cache
from os import path
import yaml


RULE_GROUPS = [  # LEFT tags count as RIGHT
    [
        (None, None),
        ('rl', 'nr'),
    ],
    [
        (None, None),
        ('hl', None),
    ],
    [
        (None, None),
        (1, 2),
        (1, 4),
        (1, 6),
        (1, 8),
        (2, 4),
        (2, 6),
        (2, 8),
        (4, 6),
        (4, 8),
        (6, 8)
    ]
]

# Gets all of the records that count as this
@cache
def counts_for_this(record_name):
    tags = lookup_record_info(record_name)['tags']

    # Search through every record. Check if we can make the conversion and end up at the original record's tags
    results = []
    for record in lookup_all_record_info():
        for rules in product(*RULE_GROUPS):
            check_tags = list(record['tags'])
            for from_val, to_val in rules:
                if from_val in check_tags:
                    check_tags.remove(from_val)
                if to_val:
                    check_tags.append(to_val)

            if set(check_tags) == set(tags):
                results.append(record['record_name'])
                break

    return results


# Gets all of the records that this record counts for
@cache
def this_counts_as(record_name):
    tags = lookup_record_info(record_name)['tags']

    # Search through every record. Check if we can make the conversion and end up at the original record's tags
    results = []
    for record in lookup_all_record_info():
        for rules in product(*RULE_GROUPS):
            check_tags = list(record['tags'])
            for to_val, from_val in rules:
                if from_val in check_tags:
                    check_tags.remove(from_val)
                if to_val:
                    check_tags.append(to_val)

            if set(check_tags) == set(tags):
                results.append(record['record_name'])
                break

    return results


# Does the record require that the user submit a time?
def time_required(tags):
    sorting = get_sorting(tags)

    return 'value_time' in sorting


# Does the record require that the user submit a score?
def score_required(tags):
    sorting = get_sorting(tags)

    return 'value_score' in sorting


# Gets the pymongo sort for a record
def get_sorting(tags):
    # LOWEST SCORE, LOWEST TIME, LOWEST TIMESTAMP
    score_tags = {'min_rewards', 'golf'}
    if set(tags) & score_tags:
        return {
            'value_score': 1,
            'value_time': 1,
            'timestamp': 1
        }

    # LOWEST TIME, LOWEST TIMESTAMP
    return {
        'value_time': 1,
        'timestamp': 1
    }


# Recursive function to flatten out the nested dictionary format in records.yaml
def flatten_yaml(d):
    if not isinstance(d, dict):
        return [([], d)]

    result = []
    for k, v in d.items():
        new_tag = []
        if k:
            new_tag.append(k)

        for sub_tags, record_data in flatten_yaml(v):
            result.append((new_tag + sub_tags, record_data))

    return result


# Gets all record info
@cache
def lookup_all_record_info():
    cur_dir = path.dirname(path.abspath(__file__))
    record_data_path = path.join(cur_dir, 'data', 'records.yaml')

    with open(record_data_path) as f:
        all_records = yaml.safe_load(f)

    records = []
    for tags, data in flatten_yaml(all_records):
        max_players = [a for a in tags if isinstance(a, int)][0]

        records.append({
            'record_name': data[0],
            'tags': tags,
            'points': data[1],
            'max_players': max_players,
            'time_required': time_required(tags),
            'score_required': score_required(tags)
        })

    return records


# Gets info for one record
@cache
def lookup_record_info(record_name: str):
    all_records = lookup_all_record_info()

    for record in all_records:
        if record['record_name'] == record_name:
            return record
