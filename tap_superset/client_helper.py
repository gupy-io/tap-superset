from typing import List, Dict, Any
from datetime import datetime


def update_dict_with(
    source: List[Dict[str, Any]], field: str, field_list: List[int]
) -> List[Dict[str, Any]]:
    result = []
    for k, obj in enumerate(source):
        new_obj = obj.copy()
        new_obj.update({field: field_list[k]})
        result.append(new_obj)
    return result


def get_start_timestamp(timestamp):
    if timestamp:
        start_timestamp = datetime.fromisoformat(timestamp)
        start_timestamp = start_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return start_timestamp
    else:
        return None
