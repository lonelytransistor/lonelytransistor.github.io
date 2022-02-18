#!/usr/bin/env python
from github import Github
import json
import requests
from pathlib import Path

g = Github()

with open('repos.json') as f:
	repos = [g.get_repo(r) for r in json.load(f)]

session = requests.Session()

for repo in repos:
	release = repo.get_latest_release()
	asset = release.get_assets()[0]
	response = session.get(asset.browser_download_url)
	dest = Path() / asset.name
	with open(dest, 'wb') as f:
		for chunk in response.iter_content(1024 * 1024):
			f.write(chunk)
