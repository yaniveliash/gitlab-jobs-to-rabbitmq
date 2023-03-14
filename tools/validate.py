import re


def mandatoryFields(payload):
    mandatory_keys = ['gitlab_token', 'index_name', 'project_id', 'job_id']
    for key in payload.keys():
        if key in mandatory_keys and payload[key] == '':
            return False
    return True


def indexName(index_name):
    pattern = r'^[A-Za-z][A-Za-z0-9-]*$'
    return bool(re.match(pattern, index_name))
