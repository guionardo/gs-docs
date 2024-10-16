import os
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
import yaml

GS_DOCS_ENV_PREFIX = 'GSDOCS_'
GS_DOCS_FILE = os.getenv('GSDOCS_CONFIG_FILE', 'gs_docs.yaml')
GS_DOC_PROJECT_FILE = '.gsdocs.yaml'


def loader(
    data_type: callable, file_name: str, field_name: str, default=None
) -> callable:
    """Tries to load data from file or environment variable
    Field name will use lowercase
    """

    if (origin := getattr(data_type, '__origin__', None)) and origin is list:
        is_iterable = True
        data_type = data_type.__args__[0]
    else:
        is_iterable = False

    def func():
        try:
            with open(file_name or '') as f:
                data = yaml.load(f, Loader=yaml.SafeLoader)
                value = data[field_name.lower()]
        except Exception:
            value = default

        if is_iterable:
            if not isinstance(value, list):
                value = [data_type(v) for v in value.split(',')]
        else:
            value = data_type(value)

        return value

    return func


@dataclass_json
@dataclass
class Configuration:
    users: list[str] = field(default_factory=loader(list[str], GS_DOCS_FILE, 'users'))
    organizations: list[str] = field(
        default_factory=loader(list[str], GS_DOCS_FILE, 'organizations')
    )


@dataclass_json
@dataclass
class Repository:
    name: str
    enabled: bool = field(default=True)


@dataclass_json
@dataclass
class ProjectConfig:
    doc_folder: str = field(
        default_factory=loader(str, GS_DOC_PROJECT_FILE, 'doc_folder', 'docs')
    )
    enabled: bool = field(
        default_factory=loader(bool, GS_DOC_PROJECT_FILE, 'enabled', True)
    )
    title: str = field(default_factory=loader(str, GS_DOC_PROJECT_FILE, 'title'))
    description: str = field(
        default_factory=loader(str, GS_DOC_PROJECT_FILE, 'description')
    )
