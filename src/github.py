from dataclasses import dataclass, field
from datetime import datetime
import os
import httpx

from .utils import new_dataclass

CACHE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cache'))


@dataclass
class Repository:
    full_name: str
    private: bool
    description: str
    git_url: str
    created_at: datetime
    updated_at: datetime
    pushed_at: datetime
    default_branch: str
    language: str

    _extra: dict = field(default_factory=dict)

    def _file_exists(self, extra_name: str, filename: str) -> str:
        if extra_name in self._extra:
            return self._extra[extra_name]
        url = f'https://github.com/{self.full_name}/raw/refs/heads/{self.default_branch}/{filename}'
        resp = httpx.head(url, headers=self._extra.get('headers', {}))
        if resp.status_code < 400:
            self._extra[extra_name] = url
            return url

    @property
    def mkdocs(self) -> str:
        return self._file_exists('mkdocs', 'mkdocs.yml')

    @property
    def gsdocs(self) -> str:
        return self._file_exists('gsdocs', '.gsdocs.yml')

    def download_zip(self) -> str:
        file_name = os.path.join(
            CACHE_FOLDER, f'{self.full_name}.{self.updated_at:%Y%m%d%H%M%S}.zip'
        )
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        if os.path.isfile(file_name):
            return file_name
        url = f'https://github.com/{self.full_name}/archive/refs/heads/{self.default_branch}.zip'
        # https://github.com/guionardo/ambevtech-csharp/archive/refs/heads/main.zip
        headers = self._extra['headers'].copy()
        resp = httpx.get(url, headers=headers, follow_redirects=True)
        if resp.status_code < 300:
            with open(file_name, 'wb') as f:
                f.write(resp.content)
            return file_name


def get_user_repositories(user: str, auth: str = None) -> list[Repository]:
    # https://api.github.com/users/Acidbytes/repos
    url = f'https://api.github.com/users/{user}/repos'
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    if auth:
        headers['Authorization'] = f'Bearer {auth}'

    page = 1
    while True:
        resp = httpx.get(f'{url}?page={page}&per_page=100', headers=headers)
        if resp.status_code != 200:
            break
        repos = resp.json()
        if len(repos) == 0:
            break
        for repo in repos:
            yield new_dataclass(Repository, repo, {'headers': headers.copy()})
        page += 1
