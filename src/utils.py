from datetime import datetime
from typing import ClassVar

from pendulum.parser import parse


def new_dataclass(dc: ClassVar, source: dict, extra: dict = None):
    new_source = {}
    for k, v in dc.__dataclass_fields__.items():
        if k in source:
            if v.type == datetime:
                new_source[k] = parse(source[k])
            else:
                new_source[k] = source[k]

    if extra:
        new_source['_extra'] = extra
    return dc(**new_source)
