import os
from dataclasses import dataclass, field

import yaml

GS_DOCS_ENV_PREFIX = 'GSDOCS_'
GS_DOCS_FILE = os.getenv('GSDOCS_CONFIG_FILE', 'gs_docs.yaml')


def loader(
    data_type: callable, file_name: str, field_name: str, default=None
) -> callable:
    """Tries to load data from file or environment variable
    Field name will use lowercase
    Env will use UPPERCASE with GSDOCS_ prefix
    """

    if (origin := getattr(data_type, '__origin__')) and origin is list:
        is_iterable = True
        data_type = data_type.__args__[0]
    else:
        is_iterable = False

    def func():
        env_name = f'{GS_DOCS_ENV_PREFIX}{field_name}'.upper()
        if not (value := os.getenv(env_name)):
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


@dataclass
class Configuration:
    users: list[str] = field(
        default_factory=loader(str, GS_DOCS_FILE, 'users', [], True)
    )
    organizations: list[str] = field(
        default_factory=loader(list[str], GS_DOCS_FILE, 'organizations')
    )


@dataclass
class ProjectConfig:
    doc_folder: str
    enabled: bool
    project_title: str
    project_description: str


#     doc_folder: "docs"  #


# enabled: true
# project_title: "Name of the project"
# project_description: "Description of the project"
