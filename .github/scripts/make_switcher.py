"""Write switcher.json, the list of versions shown in the docs version switcher.

The list is main plus every release-* tag of this repo that is published on
GitHub Pages (has a /<tag>/ directory on gh-pages), newest first. Tags passed
as arguments count as published; the release workflow passes the tag it is
deploying. Nothing here needs editing when a release is added.

Usage (from inside a clone of this repo):
  python3 make_switcher.py OUTPUT_FILE [TAG ...]
"""

import json
import re
import subprocess
import sys

SITE_URL = 'https://movensys.github.io/wmx-r2-doc/'
TAG_RE = re.compile(r'^release-\d+(\.\d+)*$')


def git(*args):
    return subprocess.run(['git', *args], check=True, capture_output=True, text=True).stdout


def release_tags():
    out = git('ls-remote', '--tags', '--refs', 'origin', 'refs/tags/release-*')
    tags = (line.split('refs/tags/', 1)[1] for line in out.splitlines())
    return [t for t in tags if TAG_RE.match(t)]


def published_dirs():
    try:
        git('fetch', '--quiet', '--depth=1', 'origin', 'gh-pages')
    except subprocess.CalledProcessError:
        return set()  # gh-pages does not exist yet
    return set(git('ls-tree', '-d', '--name-only', 'FETCH_HEAD').split())


def main():
    output, deploying = sys.argv[1], set(sys.argv[2:])
    published = published_dirs() | deploying
    tags = [t for t in release_tags() if t in published]
    tags.sort(key=lambda t: [int(n) for n in re.findall(r'\d+', t)], reverse=True)

    versions = [{'name': 'main (latest)', 'version': 'main', 'url': SITE_URL, 'preferred': True}]
    versions += [{'name': t, 'version': t, 'url': f'{SITE_URL}{t}/'} for t in tags]

    with open(output, 'w') as f:
        json.dump(versions, f, indent=2)
        f.write('\n')
    print('switcher.json:', ', '.join(v['version'] for v in versions))


if __name__ == '__main__':
    main()
