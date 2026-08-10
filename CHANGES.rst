Changelog
=========

0.6.0 (2026-08-10)
------------------
------------------------

Fix
~~~
- Resolve bugs and modernize codebase. [Mateusz Hajder]

  - fix type comparisons using isinstance() instead of type() == (E721)
  - fix inverted remote logic that ran `git remote rm origin` when origin didn't exist
  - fix missing password not halting execution (log_error → log_fail)
  - fix get_repo_url returning None without error, causing cryptic git failures
  - fix file handle leaks for FNULL and token file reads
  - fix leaked file handles in setup.py open_file helper
  - replace deprecated `git lfs clone` with `git clone` (LFS auto-handled since 2.3.0)
  - remove dead Python 2 compatibility code
  - update Python version classifiers to 3.10–3.14
- Add setuptools. [Jose Diaz-Gonzalez]

Other
~~~~~
- Chore(deps): bump packaging in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [packaging](https://github.com/pypa/packaging).


  Updates `packaging` from 26.2 to 26.3
  - [Release notes](https://github.com/pypa/packaging/releases)
  - [Changelog](https://github.com/pypa/packaging/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pypa/packaging/compare/26.2...26.3)

  ---
  updated-dependencies:
  - dependency-name: packaging
    dependency-version: '26.3'
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump actions/setup-python from 4 to 7. [dependabot[bot]]

  Bumps [actions/setup-python](https://github.com/actions/setup-python) from 4 to 7.
  - [Release notes](https://github.com/actions/setup-python/releases)
  - [Commits](https://github.com/actions/setup-python/compare/v4...v7)

  ---
  updated-dependencies:
  - dependency-name: actions/setup-python
    dependency-version: '7'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Chore(deps): bump actions/checkout from 4 to 7. [dependabot[bot]]

  Bumps [actions/checkout](https://github.com/actions/checkout) from 4 to 7.
  - [Release notes](https://github.com/actions/checkout/releases)
  - [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/actions/checkout/compare/v4...v7)

  ---
  updated-dependencies:
  - dependency-name: actions/checkout
    dependency-version: '7'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Chore: fix indentation. [Jose Diaz-Gonzalez]
- Ci: add github-actions to dependabot config. [Jose Diaz-Gonzalez]
- Ci(docker): add multi-arch Docker build and publish workflow. [Mateusz
  Hajder]
- Fix(auth): pass authentication via http.extraHeader. [Mateusz Hajder]
- Fix(lfs): remove unsupported --force and --tags flags from git lfs
  fetch. [Mateusz Hajder]

  git lfs fetch does not accept --force or --tags flags. Passing them causes git-lfs to fail with exit code 127.
- Fix(ssl): invert ssl_verify boolean logic. [Mateusz Hajder]

  Pass ssl_verify=not args.disable_ssl_verification so --disable-ssl-verification actually disables SSL verification instead of enabling it.
- Fix(gitlab): set get_all=True on projects list. [Mateusz Hajder]

  Replace deprecated as_list=False parameter with get_all=True in client.projects.list to prevent UserWarning and ensure all repositories are fetched.
- Refactor(docker): modernize Dockerfile build and initialize git-lfs.
  [Mateusz Hajder]

  - Copy uv binary directly from official image
  - Add git lfs install in runtime container stage
  - Copy only .venv from builder stage
  - Update Python and Alpine Linux
- Chore(deps): bump twine from 6.2.0 to 7.0.0 in the python-packages
  group. [dependabot[bot]]

  Bumps the python-packages group with 1 update: [twine](https://github.com/pypa/twine).


  Updates `twine` from 6.2.0 to 7.0.0
  - [Release notes](https://github.com/pypa/twine/releases)
  - [Changelog](https://github.com/pypa/twine/blob/main/docs/changelog.rst)
  - [Commits](https://github.com/pypa/twine/compare/6.2.0...7.0.0)

  ---
  updated-dependencies:
  - dependency-name: twine
    dependency-version: 7.0.0
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump tqdm in the python-packages group. [dependabot[bot]]

  Bumps the python-packages group with 1 update: [tqdm](https://github.com/tqdm/tqdm).


  Updates `tqdm` from 4.69.0 to 4.70.0
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.69.0...v4.70.0)

  ---
  updated-dependencies:
  - dependency-name: tqdm
    dependency-version: 4.70.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [certifi](https://github.com/certifi/python-certifi) and [platformdirs](https://github.com/tox-dev/platformdirs).


  Updates `certifi` from 2026.6.17 to 2026.7.22
  - [Commits](https://github.com/certifi/python-certifi/compare/2026.06.17...2026.07.22)

  Updates `platformdirs` from 4.10.1 to 4.11.0
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/docs/changelog.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.10.1...4.11.0)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2026.7.22
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: platformdirs
    dependency-version: 4.11.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [platformdirs](https://github.com/tox-dev/platformdirs) and [tqdm](https://github.com/tqdm/tqdm).


  Updates `platformdirs` from 4.10.0 to 4.10.1
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/docs/changelog.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.10.0...4.10.1)

  Updates `tqdm` from 4.68.4 to 4.69.0
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.68.4...v4.69.0)

  ---
  updated-dependencies:
  - dependency-name: platformdirs
    dependency-version: 4.10.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: tqdm
    dependency-version: 4.69.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump charset-normalizer in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [charset-normalizer](https://github.com/jawah/charset_normalizer).


  Updates `charset-normalizer` from 3.4.7 to 3.4.9
  - [Release notes](https://github.com/jawah/charset_normalizer/releases)
  - [Changelog](https://github.com/jawah/charset_normalizer/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/jawah/charset_normalizer/compare/3.4.7...3.4.9)

  ---
  updated-dependencies:
  - dependency-name: charset-normalizer
    dependency-version: 3.4.9
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump tqdm in the python-packages group. [dependabot[bot]]

  Bumps the python-packages group with 1 update: [tqdm](https://github.com/tqdm/tqdm).


  Updates `tqdm` from 4.68.3 to 4.68.4
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.68.3...v4.68.4)

  ---
  updated-dependencies:
  - dependency-name: tqdm
    dependency-version: 4.68.4
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump setuptools in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [setuptools](https://github.com/pypa/setuptools).


  Updates `setuptools` from 82.0.1 to 83.0.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v82.0.1...v83.0.0)

  ---
  updated-dependencies:
  - dependency-name: setuptools
    dependency-version: 83.0.0
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump click from 8.4.1 to 8.4.2 in the python-packages
  group. [dependabot[bot]]

  Bumps the python-packages group with 1 update: [click](https://github.com/pallets/click).


  Updates `click` from 8.4.1 to 8.4.2
  - [Release notes](https://github.com/pallets/click/releases)
  - [Changelog](https://github.com/pallets/click/blob/main/CHANGES.md)
  - [Commits](https://github.com/pallets/click/compare/8.4.1...8.4.2)

  ---
  updated-dependencies:
  - dependency-name: click
    dependency-version: 8.4.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [certifi](https://github.com/certifi/python-certifi) and [tqdm](https://github.com/tqdm/tqdm).


  Updates `certifi` from 2026.5.20 to 2026.6.17
  - [Commits](https://github.com/certifi/python-certifi/compare/2026.05.20...2026.06.17)

  Updates `tqdm` from 4.68.2 to 4.68.3
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.68.2...v4.68.3)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2026.6.17
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: tqdm
    dependency-version: 4.68.3
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [readme-renderer](https://github.com/pypa/readme_renderer) and [tqdm](https://github.com/tqdm/tqdm).


  Updates `readme-renderer` from 44.0 to 45.0
  - [Release notes](https://github.com/pypa/readme_renderer/releases)
  - [Changelog](https://github.com/pypa/readme_renderer/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pypa/readme_renderer/compare/44.0...45.0)

  Updates `tqdm` from 4.68.1 to 4.68.2
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.68.1...v4.68.2)

  ---
  updated-dependencies:
  - dependency-name: readme-renderer
    dependency-version: '45.0'
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: tqdm
    dependency-version: 4.68.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump tqdm in the python-packages group. [dependabot[bot]]

  Bumps the python-packages group with 1 update: [tqdm](https://github.com/tqdm/tqdm).


  Updates `tqdm` from 4.67.3 to 4.68.1
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.67.3...v4.68.1)

  ---
  updated-dependencies:
  - dependency-name: tqdm
    dependency-version: 4.68.1
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump bleach in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [bleach](https://github.com/mozilla/bleach).


  Updates `bleach` from 6.3.0 to 6.4.0
  - [Changelog](https://github.com/mozilla/bleach/blob/main/CHANGES)
  - [Commits](https://github.com/mozilla/bleach/compare/v6.3.0...v6.4.0)

  ---
  updated-dependencies:
  - dependency-name: bleach
    dependency-version: 6.4.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump idna from 3.17 to 3.18 in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [idna](https://github.com/kjd/idna).


  Updates `idna` from 3.17 to 3.18
  - [Release notes](https://github.com/kjd/idna/releases)
  - [Changelog](https://github.com/kjd/idna/blob/master/HISTORY.md)
  - [Commits](https://github.com/kjd/idna/compare/v3.17...v3.18)

  ---
  updated-dependencies:
  - dependency-name: idna
    dependency-version: '3.18'
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 3 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 3 updates: [docutils](https://github.com/rtfd/recommonmark), [idna](https://github.com/kjd/idna) and [platformdirs](https://github.com/tox-dev/platformdirs).


  Updates `docutils` from 0.22.4 to 0.23
  - [Changelog](https://github.com/readthedocs/recommonmark/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/rtfd/recommonmark/commits)

  Updates `idna` from 3.16 to 3.17
  - [Release notes](https://github.com/kjd/idna/releases)
  - [Changelog](https://github.com/kjd/idna/blob/v3.17/HISTORY.md)
  - [Commits](https://github.com/kjd/idna/compare/v3.16...v3.17)

  Updates `platformdirs` from 4.9.6 to 4.10.0
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/docs/changelog.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.9.6...4.10.0)

  ---
  updated-dependencies:
  - dependency-name: docutils
    dependency-version: '0.23'
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: idna
    dependency-version: '3.17'
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: platformdirs
    dependency-version: 4.10.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump more-itertools in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [more-itertools](https://github.com/more-itertools/more-itertools).


  Updates `more-itertools` from 11.0.2 to 11.1.0
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v11.0.2...v11.1.0)

  ---
  updated-dependencies:
  - dependency-name: more-itertools
    dependency-version: 11.1.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [click](https://github.com/pallets/click) and [idna](https://github.com/kjd/idna).


  Updates `click` from 8.4.0 to 8.4.1
  - [Release notes](https://github.com/pallets/click/releases)
  - [Changelog](https://github.com/pallets/click/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pallets/click/compare/8.4.0...8.4.1)

  Updates `idna` from 3.15 to 3.16
  - [Release notes](https://github.com/kjd/idna/releases)
  - [Changelog](https://github.com/kjd/idna/blob/master/HISTORY.md)
  - [Commits](https://github.com/kjd/idna/compare/v3.15...v3.16)

  ---
  updated-dependencies:
  - dependency-name: click
    dependency-version: 8.4.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: idna
    dependency-version: '3.16'
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 4
  updates. [dependabot[bot]]

  Bumps the python-packages group with 4 updates in the / directory: [black](https://github.com/psf/black), [certifi](https://github.com/certifi/python-certifi), [click](https://github.com/pallets/click) and [zipp](https://github.com/jaraco/zipp).


  Updates `black` from 26.3.1 to 26.5.1
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/26.3.1...26.5.1)

  Updates `certifi` from 2026.4.22 to 2026.5.20
  - [Commits](https://github.com/certifi/python-certifi/compare/2026.04.22...2026.05.20)

  Updates `click` from 8.3.3 to 8.4.0
  - [Release notes](https://github.com/pallets/click/releases)
  - [Changelog](https://github.com/pallets/click/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pallets/click/compare/8.3.3...8.4.0)

  Updates `zipp` from 3.23.1 to 4.1.0
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.23.1...v4.1.0)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-version: 26.5.1
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: certifi
    dependency-version: 2026.5.20
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: click
    dependency-version: 8.4.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: zipp
    dependency-version: 4.1.0
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump requests in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [requests](https://github.com/psf/requests).


  Updates `requests` from 2.34.1 to 2.34.2
  - [Release notes](https://github.com/psf/requests/releases)
  - [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md)
  - [Commits](https://github.com/psf/requests/compare/v2.34.1...v2.34.2)

  ---
  updated-dependencies:
  - dependency-name: requests
    dependency-version: 2.34.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump requests in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [requests](https://github.com/psf/requests).


  Updates `requests` from 2.34.0 to 2.34.1
  - [Release notes](https://github.com/psf/requests/releases)
  - [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md)
  - [Commits](https://github.com/psf/requests/compare/v2.34.0...v2.34.1)

  ---
  updated-dependencies:
  - dependency-name: requests
    dependency-version: 2.34.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump idna from 3.14 to 3.15 in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [idna](https://github.com/kjd/idna).


  Updates `idna` from 3.14 to 3.15
  - [Release notes](https://github.com/kjd/idna/releases)
  - [Changelog](https://github.com/kjd/idna/blob/master/HISTORY.md)
  - [Commits](https://github.com/kjd/idna/compare/v3.14...v3.15)

  ---
  updated-dependencies:
  - dependency-name: idna
    dependency-version: '3.15'
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [idna](https://github.com/kjd/idna) and [requests](https://github.com/psf/requests).


  Updates `idna` from 3.13 to 3.14
  - [Release notes](https://github.com/kjd/idna/releases)
  - [Changelog](https://github.com/kjd/idna/blob/master/HISTORY.rst)
  - [Commits](https://github.com/kjd/idna/compare/v3.13...v3.14)

  Updates `requests` from 2.33.1 to 2.34.0
  - [Release notes](https://github.com/psf/requests/releases)
  - [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md)
  - [Commits](https://github.com/psf/requests/compare/v2.33.1...v2.34.0)

  ---
  updated-dependencies:
  - dependency-name: idna
    dependency-version: '3.14'
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: requests
    dependency-version: 2.34.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump urllib3 in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [urllib3](https://github.com/urllib3/urllib3).


  Updates `urllib3` from 2.6.3 to 2.7.0
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.6.3...2.7.0)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-version: 2.7.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump markdown-it-py in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [markdown-it-py](https://github.com/executablebooks/markdown-it-py).


  Updates `markdown-it-py` from 4.0.0 to 4.2.0
  - [Release notes](https://github.com/executablebooks/markdown-it-py/releases)
  - [Changelog](https://github.com/executablebooks/markdown-it-py/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/executablebooks/markdown-it-py/compare/v4.0.0...v4.2.0)

  ---
  updated-dependencies:
  - dependency-name: markdown-it-py
    dependency-version: 4.2.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [packaging](https://github.com/pypa/packaging) and [pathspec](https://github.com/cpburnz/python-pathspec).


  Updates `packaging` from 26.1 to 26.2
  - [Release notes](https://github.com/pypa/packaging/releases)
  - [Changelog](https://github.com/pypa/packaging/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pypa/packaging/compare/26.1...26.2)

  Updates `pathspec` from 1.1.0 to 1.1.1
  - [Release notes](https://github.com/cpburnz/python-pathspec/releases)
  - [Changelog](https://github.com/cpburnz/python-pathspec/blob/master/CHANGES.rst)
  - [Commits](https://github.com/cpburnz/python-pathspec/compare/v1.1.0...v1.1.1)

  ---
  updated-dependencies:
  - dependency-name: packaging
    dependency-version: '26.2'
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pathspec
    dependency-version: 1.1.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 3 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 3 updates: [click](https://github.com/pallets/click), [idna](https://github.com/kjd/idna) and [pathspec](https://github.com/cpburnz/python-pathspec).


  Updates `click` from 8.3.2 to 8.3.3
  - [Release notes](https://github.com/pallets/click/releases)
  - [Changelog](https://github.com/pallets/click/blob/8.3.3/CHANGES.rst)
  - [Commits](https://github.com/pallets/click/compare/8.3.2...8.3.3)

  Updates `idna` from 3.12 to 3.13
  - [Release notes](https://github.com/kjd/idna/releases)
  - [Changelog](https://github.com/kjd/idna/blob/master/HISTORY.rst)
  - [Commits](https://github.com/kjd/idna/compare/v3.12...v3.13)

  Updates `pathspec` from 1.0.4 to 1.1.0
  - [Release notes](https://github.com/cpburnz/python-pathspec/releases)
  - [Changelog](https://github.com/cpburnz/python-pathspec/blob/master/CHANGES.rst)
  - [Commits](https://github.com/cpburnz/python-pathspec/compare/v1.0.4...v1.1.0)

  ---
  updated-dependencies:
  - dependency-name: click
    dependency-version: 8.3.3
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: idna
    dependency-version: '3.13'
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pathspec
    dependency-version: 1.1.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [certifi](https://github.com/certifi/python-certifi) and [idna](https://github.com/kjd/idna).


  Updates `certifi` from 2026.2.25 to 2026.4.22
  - [Commits](https://github.com/certifi/python-certifi/compare/2026.02.25...2026.04.22)

  Updates `idna` from 3.11 to 3.12
  - [Release notes](https://github.com/kjd/idna/releases)
  - [Changelog](https://github.com/kjd/idna/blob/master/HISTORY.rst)
  - [Commits](https://github.com/kjd/idna/compare/v3.11...v3.12)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2026.4.22
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: idna
    dependency-version: '3.12'
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump packaging in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [packaging](https://github.com/pypa/packaging).


  Updates `packaging` from 26.0 to 26.1
  - [Release notes](https://github.com/pypa/packaging/releases)
  - [Changelog](https://github.com/pypa/packaging/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pypa/packaging/compare/26.0...26.1)

  ---
  updated-dependencies:
  - dependency-name: packaging
    dependency-version: '26.1'
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump zipp in the python-packages group. [dependabot[bot]]

  Bumps the python-packages group with 1 update: [zipp](https://github.com/jaraco/zipp).


  Updates `zipp` from 3.23.0 to 3.23.1
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.23.0...v3.23.1)

  ---
  updated-dependencies:
  - dependency-name: zipp
    dependency-version: 3.23.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump rich in the python-packages group. [dependabot[bot]]

  Bumps the python-packages group with 1 update: [rich](https://github.com/Textualize/rich).


  Updates `rich` from 14.3.3 to 15.0.0
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v14.3.3...v15.0.0)

  ---
  updated-dependencies:
  - dependency-name: rich
    dependency-version: 15.0.0
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump more-itertools in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [more-itertools](https://github.com/more-itertools/more-itertools).


  Updates `more-itertools` from 11.0.1 to 11.0.2
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v11.0.1...v11.0.2)

  ---
  updated-dependencies:
  - dependency-name: more-itertools
    dependency-version: 11.0.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump platformdirs in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [platformdirs](https://github.com/tox-dev/platformdirs).


  Updates `platformdirs` from 4.9.4 to 4.9.6
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/docs/changelog.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.9.4...4.9.6)

  ---
  updated-dependencies:
  - dependency-name: platformdirs
    dependency-version: 4.9.6
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump click from 8.3.1 to 8.3.2 in the python-packages
  group. [dependabot[bot]]

  Bumps the python-packages group with 1 update: [click](https://github.com/pallets/click).


  Updates `click` from 8.3.1 to 8.3.2
  - [Release notes](https://github.com/pallets/click/releases)
  - [Changelog](https://github.com/pallets/click/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pallets/click/compare/8.3.1...8.3.2)

  ---
  updated-dependencies:
  - dependency-name: click
    dependency-version: 8.3.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump more-itertools in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [more-itertools](https://github.com/more-itertools/more-itertools).


  Updates `more-itertools` from 10.8.0 to 11.0.1
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v10.8.0...v11.0.1)

  ---
  updated-dependencies:
  - dependency-name: more-itertools
    dependency-version: 11.0.1
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump charset-normalizer in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [charset-normalizer](https://github.com/jawah/charset_normalizer).


  Updates `charset-normalizer` from 3.4.6 to 3.4.7
  - [Release notes](https://github.com/jawah/charset_normalizer/releases)
  - [Changelog](https://github.com/jawah/charset_normalizer/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/jawah/charset_normalizer/compare/3.4.6...3.4.7)

  ---
  updated-dependencies:
  - dependency-name: charset-normalizer
    dependency-version: 3.4.7
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump requests in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [requests](https://github.com/psf/requests).


  Updates `requests` from 2.33.0 to 2.33.1
  - [Release notes](https://github.com/psf/requests/releases)
  - [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md)
  - [Commits](https://github.com/psf/requests/compare/v2.33.0...v2.33.1)

  ---
  updated-dependencies:
  - dependency-name: requests
    dependency-version: 2.33.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump pygments in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [pygments](https://github.com/pygments/pygments).


  Updates `pygments` from 2.19.2 to 2.20.0
  - [Release notes](https://github.com/pygments/pygments/releases)
  - [Changelog](https://github.com/pygments/pygments/blob/master/CHANGES)
  - [Commits](https://github.com/pygments/pygments/compare/2.19.2...2.20.0)

  ---
  updated-dependencies:
  - dependency-name: pygments
    dependency-version: 2.20.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump requests in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [requests](https://github.com/psf/requests).


  Updates `requests` from 2.32.5 to 2.33.0
  - [Release notes](https://github.com/psf/requests/releases)
  - [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md)
  - [Commits](https://github.com/psf/requests/compare/v2.32.5...v2.33.0)

  ---
  updated-dependencies:
  - dependency-name: requests
    dependency-version: 2.33.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump importlib-metadata in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [importlib-metadata](https://github.com/python/importlib_metadata).


  Updates `importlib-metadata` from 8.7.1 to 9.0.0
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v8.7.1...v9.0.0)

  ---
  updated-dependencies:
  - dependency-name: importlib-metadata
    dependency-version: 9.0.0
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 2
  updates. [dependabot[bot]]

  Bumps the python-packages group with 2 updates in the / directory: [black](https://github.com/psf/black) and [charset-normalizer](https://github.com/jawah/charset_normalizer).


  Updates `black` from 26.3.0 to 26.3.1
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/26.3.0...26.3.1)

  Updates `charset-normalizer` from 3.4.5 to 3.4.6
  - [Release notes](https://github.com/jawah/charset_normalizer/releases)
  - [Changelog](https://github.com/jawah/charset_normalizer/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/jawah/charset_normalizer/compare/3.4.5...3.4.6)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-version: 26.3.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: charset-normalizer
    dependency-version: 3.4.6
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [black](https://github.com/psf/black) and [setuptools](https://github.com/pypa/setuptools).


  Updates `black` from 26.1.0 to 26.3.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/26.1.0...26.3.0)

  Updates `setuptools` from 82.0.0 to 82.0.1
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v82.0.0...v82.0.1)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-version: 26.3.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-version: 82.0.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [charset-normalizer](https://github.com/jawah/charset_normalizer) and [platformdirs](https://github.com/tox-dev/platformdirs).


  Updates `charset-normalizer` from 3.4.4 to 3.4.5
  - [Release notes](https://github.com/jawah/charset_normalizer/releases)
  - [Changelog](https://github.com/jawah/charset_normalizer/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/jawah/charset_normalizer/compare/3.4.4...3.4.5)

  Updates `platformdirs` from 4.9.2 to 4.9.4
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/docs/changelog.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.9.2...4.9.4)

  ---
  updated-dependencies:
  - dependency-name: charset-normalizer
    dependency-version: 3.4.5
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: platformdirs
    dependency-version: 4.9.4
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump certifi in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [certifi](https://github.com/certifi/python-certifi).


  Updates `certifi` from 2026.1.4 to 2026.2.25
  - [Commits](https://github.com/certifi/python-certifi/compare/2026.01.04...2026.02.25)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2026.2.25
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump rich in the python-packages group. [dependabot[bot]]

  Bumps the python-packages group with 1 update: [rich](https://github.com/Textualize/rich).


  Updates `rich` from 14.3.2 to 14.3.3
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v14.3.2...v14.3.3)

  ---
  updated-dependencies:
  - dependency-name: rich
    dependency-version: 14.3.3
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump platformdirs in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [platformdirs](https://github.com/tox-dev/platformdirs).


  Updates `platformdirs` from 4.7.0 to 4.9.2
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/docs/changelog.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.7.0...4.9.2)

  ---
  updated-dependencies:
  - dependency-name: platformdirs
    dependency-version: 4.9.2
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 2
  updates. [dependabot[bot]]

  Bumps the python-packages group with 2 updates in the / directory: [platformdirs](https://github.com/tox-dev/platformdirs) and [setuptools](https://github.com/pypa/setuptools).


  Updates `platformdirs` from 4.5.1 to 4.7.0
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/docs/changelog.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.5.1...4.7.0)

  Updates `setuptools` from 80.10.2 to 82.0.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v80.10.2...v82.0.0)

  ---
  updated-dependencies:
  - dependency-name: platformdirs
    dependency-version: 4.7.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-version: 82.0.0
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump tqdm in the python-packages group. [dependabot[bot]]

  Bumps the python-packages group with 1 update: [tqdm](https://github.com/tqdm/tqdm).


  Updates `tqdm` from 4.67.2 to 4.67.3
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.67.2...v4.67.3)

  ---
  updated-dependencies:
  - dependency-name: tqdm
    dependency-version: 4.67.3
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [rich](https://github.com/Textualize/rich) and [tqdm](https://github.com/tqdm/tqdm).


  Updates `rich` from 14.3.1 to 14.3.2
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v14.3.1...v14.3.2)

  Updates `tqdm` from 4.67.1 to 4.67.2
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.67.1...v4.67.2)

  ---
  updated-dependencies:
  - dependency-name: rich
    dependency-version: 14.3.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: tqdm
    dependency-version: 4.67.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump pathspec in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [pathspec](https://github.com/cpburnz/python-pathspec).


  Updates `pathspec` from 1.0.3 to 1.0.4
  - [Release notes](https://github.com/cpburnz/python-pathspec/releases)
  - [Changelog](https://github.com/cpburnz/python-pathspec/blob/master/CHANGES.rst)
  - [Commits](https://github.com/cpburnz/python-pathspec/compare/v1.0.3...v1.0.4)

  ---
  updated-dependencies:
  - dependency-name: pathspec
    dependency-version: 1.0.4
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [rich](https://github.com/Textualize/rich) and [setuptools](https://github.com/pypa/setuptools).


  Updates `rich` from 14.2.0 to 14.3.1
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v14.2.0...v14.3.1)

  Updates `setuptools` from 80.10.1 to 80.10.2
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v80.10.1...v80.10.2)

  ---
  updated-dependencies:
  - dependency-name: rich
    dependency-version: 14.3.1
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-version: 80.10.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 2
  updates. [dependabot[bot]]

  Bumps the python-packages group with 2 updates in the / directory: [packaging](https://github.com/pypa/packaging) and [setuptools](https://github.com/pypa/setuptools).


  Updates `packaging` from 25.0 to 26.0
  - [Release notes](https://github.com/pypa/packaging/releases)
  - [Changelog](https://github.com/pypa/packaging/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pypa/packaging/compare/25.0...26.0)

  Updates `setuptools` from 80.9.0 to 80.10.1
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v80.9.0...v80.10.1)

  ---
  updated-dependencies:
  - dependency-name: packaging
    dependency-version: '26.0'
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-version: 80.10.1
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 2
  updates. [dependabot[bot]]

  Bumps the python-packages group with 2 updates in the / directory: [black](https://github.com/psf/black) and [pathspec](https://github.com/cpburnz/python-pathspec).


  Updates `black` from 25.12.0 to 26.1.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/25.12.0...26.1.0)

  Updates `pathspec` from 1.0.2 to 1.0.3
  - [Release notes](https://github.com/cpburnz/python-pathspec/releases)
  - [Changelog](https://github.com/cpburnz/python-pathspec/blob/master/CHANGES.rst)
  - [Commits](https://github.com/cpburnz/python-pathspec/compare/v1.0.2...v1.0.3)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-version: 26.1.0
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: pathspec
    dependency-version: 1.0.3
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump urllib3 from 2.6.2 to 2.6.3. [dependabot[bot]]

  Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.6.2 to 2.6.3.
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.6.2...2.6.3)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-version: 2.6.3
    dependency-type: direct:production
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [pathspec](https://github.com/cpburnz/python-pathspec) and [urllib3](https://github.com/urllib3/urllib3).


  Updates `pathspec` from 1.0.1 to 1.0.2
  - [Release notes](https://github.com/cpburnz/python-pathspec/releases)
  - [Changelog](https://github.com/cpburnz/python-pathspec/blob/master/CHANGES.rst)
  - [Commits](https://github.com/cpburnz/python-pathspec/compare/v1.0.1...v1.0.2)

  Updates `urllib3` from 2.6.2 to 2.6.3
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.6.2...2.6.3)

  ---
  updated-dependencies:
  - dependency-name: pathspec
    dependency-version: 1.0.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: urllib3
    dependency-version: 2.6.3
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump pathspec in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [pathspec](https://github.com/cpburnz/python-pathspec).


  Updates `pathspec` from 0.12.1 to 1.0.1
  - [Release notes](https://github.com/cpburnz/python-pathspec/releases)
  - [Changelog](https://github.com/cpburnz/python-pathspec/blob/master/CHANGES.rst)
  - [Commits](https://github.com/cpburnz/python-pathspec/compare/v0.12.1...v1.0.1)

  ---
  updated-dependencies:
  - dependency-name: pathspec
    dependency-version: 1.0.1
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump certifi in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [certifi](https://github.com/certifi/python-certifi).


  Updates `certifi` from 2025.11.12 to 2026.1.4
  - [Commits](https://github.com/certifi/python-certifi/compare/2025.11.12...2026.01.04)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2026.1.4
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump importlib-metadata in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [importlib-metadata](https://github.com/python/importlib_metadata).


  Updates `importlib-metadata` from 8.7.0 to 8.7.1
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v8.7.0...v8.7.1)

  ---
  updated-dependencies:
  - dependency-name: importlib-metadata
    dependency-version: 8.7.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump docutils in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [docutils](https://github.com/rtfd/recommonmark).


  Updates `docutils` from 0.22.3 to 0.22.4
  - [Changelog](https://github.com/readthedocs/recommonmark/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/rtfd/recommonmark/commits)

  ---
  updated-dependencies:
  - dependency-name: docutils
    dependency-version: 0.22.4
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump urllib3 in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [urllib3](https://github.com/urllib3/urllib3).


  Updates `urllib3` from 2.6.1 to 2.6.2
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.6.1...2.6.2)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-version: 2.6.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump urllib3 in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [urllib3](https://github.com/urllib3/urllib3).


  Updates `urllib3` from 2.6.0 to 2.6.1
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.6.0...2.6.1)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-version: 2.6.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [black](https://github.com/psf/black) and [platformdirs](https://github.com/tox-dev/platformdirs).


  Updates `black` from 25.11.0 to 25.12.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/25.11.0...25.12.0)

  Updates `platformdirs` from 4.5.0 to 4.5.1
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/CHANGES.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.5.0...4.5.1)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-version: 25.12.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: platformdirs
    dependency-version: 4.5.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump urllib3 from 2.5.0 to 2.6.0. [dependabot[bot]]

  Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.5.0 to 2.6.0.
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.5.0...2.6.0)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-version: 2.6.0
    dependency-type: direct:production
  ...
- Chore(deps): bump restructuredtext-lint in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [restructuredtext-lint](https://github.com/twolfson/restructuredtext-lint).


  Updates `restructuredtext-lint` from 1.4.0 to 2.0.2
  - [Changelog](https://github.com/twolfson/restructuredtext-lint/blob/master/CHANGELOG.rst)
  - [Commits](https://github.com/twolfson/restructuredtext-lint/compare/1.4.0...2.0.2)

  ---
  updated-dependencies:
  - dependency-name: restructuredtext-lint
    dependency-version: 2.0.2
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [click](https://github.com/pallets/click) and [keyring](https://github.com/jaraco/keyring).


  Updates `click` from 8.3.0 to 8.3.1
  - [Release notes](https://github.com/pallets/click/releases)
  - [Changelog](https://github.com/pallets/click/blob/8.3.1/CHANGES.rst)
  - [Commits](https://github.com/pallets/click/compare/8.3.0...8.3.1)

  Updates `keyring` from 25.6.0 to 25.7.0
  - [Release notes](https://github.com/jaraco/keyring/releases)
  - [Changelog](https://github.com/jaraco/keyring/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/keyring/compare/v25.6.0...v25.7.0)

  ---
  updated-dependencies:
  - dependency-name: click
    dependency-version: 8.3.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: keyring
    dependency-version: 25.7.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump certifi in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [certifi](https://github.com/certifi/python-certifi).


  Updates `certifi` from 2025.10.5 to 2025.11.12
  - [Commits](https://github.com/certifi/python-certifi/compare/2025.10.05...2025.11.12)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2025.11.12
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump black in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [black](https://github.com/psf/black).


  Updates `black` from 25.9.0 to 25.11.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/25.9.0...25.11.0)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-version: 25.11.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump docutils in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [docutils](https://github.com/rtfd/recommonmark).


  Updates `docutils` from 0.22.2 to 0.22.3
  - [Changelog](https://github.com/readthedocs/recommonmark/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/rtfd/recommonmark/commits)

  ---
  updated-dependencies:
  - dependency-name: docutils
    dependency-version: 0.22.3
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump bleach in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [bleach](https://github.com/mozilla/bleach).


  Updates `bleach` from 6.2.0 to 6.3.0
  - [Changelog](https://github.com/mozilla/bleach/blob/main/CHANGES)
  - [Commits](https://github.com/mozilla/bleach/compare/v6.2.0...v6.3.0)

  ---
  updated-dependencies:
  - dependency-name: bleach
    dependency-version: 6.3.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump charset-normalizer in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [charset-normalizer](https://github.com/jawah/charset_normalizer).


  Updates `charset-normalizer` from 3.4.3 to 3.4.4
  - [Release notes](https://github.com/jawah/charset_normalizer/releases)
  - [Changelog](https://github.com/jawah/charset_normalizer/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/jawah/charset_normalizer/compare/3.4.3...3.4.4)

  ---
  updated-dependencies:
  - dependency-name: charset-normalizer
    dependency-version: 3.4.4
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump idna from 3.10 to 3.11 in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [idna](https://github.com/kjd/idna).


  Updates `idna` from 3.10 to 3.11
  - [Release notes](https://github.com/kjd/idna/releases)
  - [Changelog](https://github.com/kjd/idna/blob/master/HISTORY.rst)
  - [Commits](https://github.com/kjd/idna/compare/v3.10...v3.11)

  ---
  updated-dependencies:
  - dependency-name: idna
    dependency-version: '3.11'
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 2
  updates. [dependabot[bot]]

  Bumps the python-packages group with 2 updates in the / directory: [platformdirs](https://github.com/tox-dev/platformdirs) and [rich](https://github.com/Textualize/rich).


  Updates `platformdirs` from 4.4.0 to 4.5.0
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/CHANGES.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.4.0...4.5.0)

  Updates `rich` from 14.1.0 to 14.2.0
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v14.1.0...v14.2.0)

  ---
  updated-dependencies:
  - dependency-name: platformdirs
    dependency-version: 4.5.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: rich
    dependency-version: 14.2.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 3 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 3 updates: [certifi](https://github.com/certifi/python-certifi), [click](https://github.com/pallets/click) and [markdown-it-py](https://github.com/executablebooks/markdown-it-py).


  Updates `certifi` from 2025.8.3 to 2025.10.5
  - [Commits](https://github.com/certifi/python-certifi/compare/2025.08.03...2025.10.05)

  Updates `click` from 8.1.8 to 8.3.0
  - [Release notes](https://github.com/pallets/click/releases)
  - [Changelog](https://github.com/pallets/click/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pallets/click/compare/8.1.8...8.3.0)

  Updates `markdown-it-py` from 3.0.0 to 4.0.0
  - [Release notes](https://github.com/executablebooks/markdown-it-py/releases)
  - [Changelog](https://github.com/executablebooks/markdown-it-py/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/executablebooks/markdown-it-py/compare/v3.0.0...v4.0.0)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2025.10.5
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: click
    dependency-version: 8.3.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: markdown-it-py
    dependency-version: 4.0.0
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump docutils in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [docutils](https://github.com/rtfd/recommonmark).


  Updates `docutils` from 0.22.1 to 0.22.2
  - [Changelog](https://github.com/readthedocs/recommonmark/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/rtfd/recommonmark/commits)

  ---
  updated-dependencies:
  - dependency-name: docutils
    dependency-version: 0.22.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 2
  updates. [dependabot[bot]]

  Bumps the python-packages group with 2 updates in the / directory: [black](https://github.com/psf/black) and [docutils](https://github.com/rtfd/recommonmark).


  Updates `black` from 25.1.0 to 25.9.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/25.1.0...25.9.0)

  Updates `docutils` from 0.22 to 0.22.1
  - [Changelog](https://github.com/readthedocs/recommonmark/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/rtfd/recommonmark/commits)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-version: 25.9.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: docutils
    dependency-version: 0.22.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump twine from 6.1.0 to 6.2.0 in the python-packages
  group. [dependabot[bot]]

  Bumps the python-packages group with 1 update: [twine](https://github.com/pypa/twine).


  Updates `twine` from 6.1.0 to 6.2.0
  - [Release notes](https://github.com/pypa/twine/releases)
  - [Changelog](https://github.com/pypa/twine/blob/main/docs/changelog.rst)
  - [Commits](https://github.com/pypa/twine/compare/6.1.0...6.2.0)

  ---
  updated-dependencies:
  - dependency-name: twine
    dependency-version: 6.2.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump more-itertools in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [more-itertools](https://github.com/more-itertools/more-itertools).


  Updates `more-itertools` from 10.7.0 to 10.8.0
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v10.7.0...v10.8.0)

  ---
  updated-dependencies:
  - dependency-name: more-itertools
    dependency-version: 10.8.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump platformdirs in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [platformdirs](https://github.com/tox-dev/platformdirs).


  Updates `platformdirs` from 4.3.8 to 4.4.0
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/CHANGES.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.3.8...4.4.0)

  ---
  updated-dependencies:
  - dependency-name: platformdirs
    dependency-version: 4.4.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump requests in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [requests](https://github.com/psf/requests).


  Updates `requests` from 2.32.4 to 2.32.5
  - [Release notes](https://github.com/psf/requests/releases)
  - [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md)
  - [Commits](https://github.com/psf/requests/compare/v2.32.4...v2.32.5)

  ---
  updated-dependencies:
  - dependency-name: requests
    dependency-version: 2.32.5
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Feat: add Dockerfile for building and running gitlab-backup
  application. [Mateusz Hajder]
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [certifi](https://github.com/certifi/python-certifi) and [charset-normalizer](https://github.com/jawah/charset_normalizer).


  Updates `certifi` from 2025.7.14 to 2025.8.3
  - [Commits](https://github.com/certifi/python-certifi/compare/2025.07.14...2025.08.03)

  Updates `charset-normalizer` from 3.4.2 to 3.4.3
  - [Release notes](https://github.com/jawah/charset_normalizer/releases)
  - [Changelog](https://github.com/jawah/charset_normalizer/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/jawah/charset_normalizer/compare/3.4.2...3.4.3)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2025.8.3
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: charset-normalizer
    dependency-version: 3.4.3
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 3
  updates. [dependabot[bot]]

  Bumps the python-packages group with 3 updates in the / directory: [certifi](https://github.com/certifi/python-certifi), [docutils](https://github.com/rtfd/recommonmark) and [rich](https://github.com/Textualize/rich).


  Updates `certifi` from 2025.7.9 to 2025.7.14
  - [Commits](https://github.com/certifi/python-certifi/compare/2025.07.09...2025.07.14)

  Updates `docutils` from 0.21.2 to 0.22
  - [Changelog](https://github.com/readthedocs/recommonmark/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/rtfd/recommonmark/commits)

  Updates `rich` from 14.0.0 to 14.1.0
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v14.0.0...v14.1.0)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2025.7.14
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: docutils
    dependency-version: '0.22'
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: rich
    dependency-version: 14.1.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump certifi in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [certifi](https://github.com/certifi/python-certifi).


  Updates `certifi` from 2025.6.15 to 2025.7.9
  - [Commits](https://github.com/certifi/python-certifi/compare/2025.06.15...2025.07.09)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2025.7.9
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump urllib3 from 2.4.0 to 2.5.0. [dependabot[bot]]

  Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.4.0 to 2.5.0.
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.4.0...2.5.0)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-version: 2.5.0
    dependency-type: direct:production
  ...
- Chore(deps): bump the python-packages group with 5 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 5 updates:

  | Package | From | To |
  | --- | --- | --- |
  | [flake8](https://github.com/pycqa/flake8) | `7.2.0` | `7.3.0` |
  | [pycodestyle](https://github.com/PyCQA/pycodestyle) | `2.13.0` | `2.14.0` |
  | [pyflakes](https://github.com/PyCQA/pyflakes) | `3.3.2` | `3.4.0` |
  | [pygments](https://github.com/pygments/pygments) | `2.19.1` | `2.19.2` |
  | [urllib3](https://github.com/urllib3/urllib3) | `2.4.0` | `2.5.0` |


  Updates `flake8` from 7.2.0 to 7.3.0
  - [Commits](https://github.com/pycqa/flake8/compare/7.2.0...7.3.0)

  Updates `pycodestyle` from 2.13.0 to 2.14.0
  - [Release notes](https://github.com/PyCQA/pycodestyle/releases)
  - [Changelog](https://github.com/PyCQA/pycodestyle/blob/main/CHANGES.txt)
  - [Commits](https://github.com/PyCQA/pycodestyle/compare/2.13.0...2.14.0)

  Updates `pyflakes` from 3.3.2 to 3.4.0
  - [Changelog](https://github.com/PyCQA/pyflakes/blob/main/NEWS.rst)
  - [Commits](https://github.com/PyCQA/pyflakes/compare/3.3.2...3.4.0)

  Updates `pygments` from 2.19.1 to 2.19.2
  - [Release notes](https://github.com/pygments/pygments/releases)
  - [Changelog](https://github.com/pygments/pygments/blob/master/CHANGES)
  - [Commits](https://github.com/pygments/pygments/compare/2.19.1...2.19.2)

  Updates `urllib3` from 2.4.0 to 2.5.0
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.4.0...2.5.0)

  ---
  updated-dependencies:
  - dependency-name: flake8
    dependency-version: 7.3.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pycodestyle
    dependency-version: 2.14.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pyflakes
    dependency-version: 3.4.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pygments
    dependency-version: 2.19.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: urllib3
    dependency-version: 2.5.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump certifi in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [certifi](https://github.com/certifi/python-certifi).


  Updates `certifi` from 2025.4.26 to 2025.6.15
  - [Commits](https://github.com/certifi/python-certifi/compare/2025.04.26...2025.06.15)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2025.6.15
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 2
  updates. [dependabot[bot]]

  Bumps the python-packages group with 2 updates in the / directory: [requests](https://github.com/psf/requests) and [zipp](https://github.com/jaraco/zipp).


  Updates `requests` from 2.32.3 to 2.32.4
  - [Release notes](https://github.com/psf/requests/releases)
  - [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md)
  - [Commits](https://github.com/psf/requests/compare/v2.32.3...v2.32.4)

  Updates `zipp` from 3.22.0 to 3.23.0
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.22.0...v3.23.0)

  ---
  updated-dependencies:
  - dependency-name: requests
    dependency-version: 2.32.4
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: zipp
    dependency-version: 3.23.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump requests from 2.32.3 to 2.32.4. [dependabot[bot]]

  Bumps [requests](https://github.com/psf/requests) from 2.32.3 to 2.32.4.
  - [Release notes](https://github.com/psf/requests/releases)
  - [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md)
  - [Commits](https://github.com/psf/requests/compare/v2.32.3...v2.32.4)

  ---
  updated-dependencies:
  - dependency-name: requests
    dependency-version: 2.32.4
    dependency-type: direct:production
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [setuptools](https://github.com/pypa/setuptools) and [zipp](https://github.com/jaraco/zipp).


  Updates `setuptools` from 80.8.0 to 80.9.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v80.8.0...v80.9.0)

  Updates `zipp` from 3.21.0 to 3.22.0
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.21.0...v3.22.0)

  ---
  updated-dependencies:
  - dependency-name: setuptools
    dependency-version: 80.9.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: zipp
    dependency-version: 3.22.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump setuptools in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [setuptools](https://github.com/pypa/setuptools).


  Updates `setuptools` from 80.4.0 to 80.8.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v80.4.0...v80.8.0)

  ---
  updated-dependencies:
  - dependency-name: setuptools
    dependency-version: 80.8.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump setuptools in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [setuptools](https://github.com/pypa/setuptools).


  Updates `setuptools` from 80.3.1 to 80.4.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v80.3.1...v80.4.0)

  ---
  updated-dependencies:
  - dependency-name: setuptools
    dependency-version: 80.4.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 3
  updates. [dependabot[bot]]

  Bumps the python-packages group with 3 updates in the / directory: [charset-normalizer](https://github.com/jawah/charset_normalizer), [platformdirs](https://github.com/tox-dev/platformdirs) and [setuptools](https://github.com/pypa/setuptools).


  Updates `charset-normalizer` from 3.4.1 to 3.4.2
  - [Release notes](https://github.com/jawah/charset_normalizer/releases)
  - [Changelog](https://github.com/jawah/charset_normalizer/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/jawah/charset_normalizer/compare/3.4.1...3.4.2)

  Updates `platformdirs` from 4.3.7 to 4.3.8
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/CHANGES.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.3.7...4.3.8)

  Updates `setuptools` from 80.0.0 to 80.3.1
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v80.0.0...v80.3.1)

  ---
  updated-dependencies:
  - dependency-name: charset-normalizer
    dependency-version: 3.4.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: platformdirs
    dependency-version: 4.3.8
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-version: 80.3.1
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 6
  updates. [dependabot[bot]]

  Bumps the python-packages group with 6 updates in the / directory:

  | Package | From | To |
  | --- | --- | --- |
  | [certifi](https://github.com/certifi/python-certifi) | `2025.1.31` | `2025.4.26` |
  | [importlib-metadata](https://github.com/python/importlib_metadata) | `8.6.1` | `8.7.0` |
  | [more-itertools](https://github.com/more-itertools/more-itertools) | `10.6.0` | `10.7.0` |
  | [mypy-extensions](https://github.com/python/mypy_extensions) | `1.0.0` | `1.1.0` |
  | [packaging](https://github.com/pypa/packaging) | `24.2` | `25.0` |
  | [setuptools](https://github.com/pypa/setuptools) | `78.1.0` | `80.0.0` |



  Updates `certifi` from 2025.1.31 to 2025.4.26
  - [Commits](https://github.com/certifi/python-certifi/compare/2025.01.31...2025.04.26)

  Updates `importlib-metadata` from 8.6.1 to 8.7.0
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v8.6.1...v8.7.0)

  Updates `more-itertools` from 10.6.0 to 10.7.0
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v10.6.0...v10.7.0)

  Updates `mypy-extensions` from 1.0.0 to 1.1.0
  - [Commits](https://github.com/python/mypy_extensions/compare/1.0.0...1.1.0)

  Updates `packaging` from 24.2 to 25.0
  - [Release notes](https://github.com/pypa/packaging/releases)
  - [Changelog](https://github.com/pypa/packaging/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pypa/packaging/compare/24.2...25.0)

  Updates `setuptools` from 78.1.0 to 80.0.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v78.1.0...v80.0.0)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-version: 2025.4.26
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: importlib-metadata
    dependency-version: 8.7.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: more-itertools
    dependency-version: 10.7.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: mypy-extensions
    dependency-version: 1.1.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: packaging
    dependency-version: '25.0'
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-version: 80.0.0
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore: bump runs-on image from ubuntu-20.04 to ubuntu-24.04. [Jose
  Diaz-Gonzalez]
- Chore: bump runs-on image from ubuntu-22.04 to ubuntu-24.04. [Jose
  Diaz-Gonzalez]
- Chore: bump runs-on image from ubuntu-20.04 to ubuntu-24.04. [Jose
  Diaz-Gonzalez]
- Chore(deps): bump urllib3 in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [urllib3](https://github.com/urllib3/urllib3).


  Updates `urllib3` from 2.3.0 to 2.4.0
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.3.0...2.4.0)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-version: 2.4.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 5 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 5 updates:

  | Package | From | To |
  | --- | --- | --- |
  | [flake8](https://github.com/pycqa/flake8) | `7.1.2` | `7.2.0` |
  | [pycodestyle](https://github.com/PyCQA/pycodestyle) | `2.12.1` | `2.13.0` |
  | [pyflakes](https://github.com/PyCQA/pyflakes) | `3.2.0` | `3.3.2` |
  | [rich](https://github.com/Textualize/rich) | `13.9.4` | `14.0.0` |
  | [setuptools](https://github.com/pypa/setuptools) | `78.0.1` | `78.1.0` |


  Updates `flake8` from 7.1.2 to 7.2.0
  - [Commits](https://github.com/pycqa/flake8/compare/7.1.2...7.2.0)

  Updates `pycodestyle` from 2.12.1 to 2.13.0
  - [Release notes](https://github.com/PyCQA/pycodestyle/releases)
  - [Changelog](https://github.com/PyCQA/pycodestyle/blob/main/CHANGES.txt)
  - [Commits](https://github.com/PyCQA/pycodestyle/compare/2.12.1...2.13.0)

  Updates `pyflakes` from 3.2.0 to 3.3.2
  - [Changelog](https://github.com/PyCQA/pyflakes/blob/main/NEWS.rst)
  - [Commits](https://github.com/PyCQA/pyflakes/compare/3.2.0...3.3.2)

  Updates `rich` from 13.9.4 to 14.0.0
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v13.9.4...v14.0.0)

  Updates `setuptools` from 78.0.1 to 78.1.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v78.0.1...v78.1.0)

  ---
  updated-dependencies:
  - dependency-name: flake8
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pycodestyle
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pyflakes
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: rich
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump setuptools in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [setuptools](https://github.com/pypa/setuptools).


  Updates `setuptools` from 77.0.1 to 78.0.1
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v77.0.1...v78.0.1)

  ---
  updated-dependencies:
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 2
  updates. [dependabot[bot]]

  Bumps the python-packages group with 2 updates in the / directory: [platformdirs](https://github.com/tox-dev/platformdirs) and [setuptools](https://github.com/pypa/setuptools).


  Updates `platformdirs` from 4.3.6 to 4.3.7
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/CHANGES.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.3.6...4.3.7)

  Updates `setuptools` from 76.0.0 to 77.0.1
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v76.0.0...v77.0.1)

  ---
  updated-dependencies:
  - dependency-name: platformdirs
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump setuptools in the python-packages group.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [setuptools](https://github.com/pypa/setuptools).


  Updates `setuptools` from 75.8.2 to 76.0.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v75.8.2...v76.0.0)

  ---
  updated-dependencies:
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 24
  updates. [dependabot[bot]]

  Bumps the python-packages group with 24 updates in the / directory:

  | Package | From | To |
  | --- | --- | --- |
  | [autopep8](https://github.com/hhatto/autopep8) | `2.3.1` | `2.3.2` |
  | [black](https://github.com/psf/black) | `24.4.2` | `25.1.0` |
  | [bleach](https://github.com/mozilla/bleach) | `6.1.0` | `6.2.0` |
  | [certifi](https://github.com/certifi/python-certifi) | `2024.7.4` | `2025.1.31` |
  | [charset-normalizer](https://github.com/jawah/charset_normalizer) | `3.3.2` | `3.4.1` |
  | [click](https://github.com/pallets/click) | `8.1.7` | `8.1.8` |
  | [flake8](https://github.com/pycqa/flake8) | `7.1.0` | `7.1.2` |
  | [idna](https://github.com/kjd/idna) | `3.7` | `3.10` |
  | [importlib-metadata](https://github.com/python/importlib_metadata) | `7.2.1` | `8.6.1` |
  | [keyring](https://github.com/jaraco/keyring) | `25.2.1` | `25.6.0` |
  | [more-itertools](https://github.com/more-itertools/more-itertools) | `10.3.0` | `10.6.0` |
  | [packaging](https://github.com/pypa/packaging) | `24.1` | `24.2` |
  | [pkginfo](https://code.launchpad.net/~tseaver/pkginfo/trunk) | `1.11.1` | `1.12.1.2` |
  | [platformdirs](https://github.com/tox-dev/platformdirs) | `4.2.2` | `4.3.6` |
  | [pycodestyle](https://github.com/PyCQA/pycodestyle) | `2.12.0` | `2.12.1` |
  | [pygments](https://github.com/pygments/pygments) | `2.18.0` | `2.19.1` |
  | [readme-renderer](https://github.com/pypa/readme_renderer) | `43.0` | `44.0` |
  | [rich](https://github.com/Textualize/rich) | `13.7.1` | `13.9.4` |
  | [setuptools](https://github.com/pypa/setuptools) | `70.1.1` | `75.8.2` |
  | [six](https://github.com/benjaminp/six) | `1.16.0` | `1.17.0` |
  | [tqdm](https://github.com/tqdm/tqdm) | `4.66.4` | `4.67.1` |
  | [twine](https://github.com/pypa/twine) | `5.1.0` | `6.1.0` |
  | [urllib3](https://github.com/urllib3/urllib3) | `2.2.2` | `2.3.0` |
  | [zipp](https://github.com/jaraco/zipp) | `3.19.2` | `3.21.0` |



  Updates `autopep8` from 2.3.1 to 2.3.2
  - [Release notes](https://github.com/hhatto/autopep8/releases)
  - [Commits](https://github.com/hhatto/autopep8/compare/v2.3.1...v2.3.2)

  Updates `black` from 24.4.2 to 25.1.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/24.4.2...25.1.0)

  Updates `bleach` from 6.1.0 to 6.2.0
  - [Changelog](https://github.com/mozilla/bleach/blob/main/CHANGES)
  - [Commits](https://github.com/mozilla/bleach/compare/v6.1.0...v6.2.0)

  Updates `certifi` from 2024.7.4 to 2025.1.31
  - [Commits](https://github.com/certifi/python-certifi/compare/2024.07.04...2025.01.31)

  Updates `charset-normalizer` from 3.3.2 to 3.4.1
  - [Release notes](https://github.com/jawah/charset_normalizer/releases)
  - [Changelog](https://github.com/jawah/charset_normalizer/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/jawah/charset_normalizer/compare/3.3.2...3.4.1)

  Updates `click` from 8.1.7 to 8.1.8
  - [Release notes](https://github.com/pallets/click/releases)
  - [Changelog](https://github.com/pallets/click/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pallets/click/compare/8.1.7...8.1.8)

  Updates `flake8` from 7.1.0 to 7.1.2
  - [Commits](https://github.com/pycqa/flake8/compare/7.1.0...7.1.2)

  Updates `idna` from 3.7 to 3.10
  - [Release notes](https://github.com/kjd/idna/releases)
  - [Changelog](https://github.com/kjd/idna/blob/master/HISTORY.rst)
  - [Commits](https://github.com/kjd/idna/compare/v3.7...v3.10)

  Updates `importlib-metadata` from 7.2.1 to 8.6.1
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v7.2.1...v8.6.1)

  Updates `keyring` from 25.2.1 to 25.6.0
  - [Release notes](https://github.com/jaraco/keyring/releases)
  - [Changelog](https://github.com/jaraco/keyring/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/keyring/compare/v25.2.1...v25.6.0)

  Updates `more-itertools` from 10.3.0 to 10.6.0
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v10.3.0...v10.6.0)

  Updates `packaging` from 24.1 to 24.2
  - [Release notes](https://github.com/pypa/packaging/releases)
  - [Changelog](https://github.com/pypa/packaging/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pypa/packaging/compare/24.1...24.2)

  Updates `pkginfo` from 1.11.1 to 1.12.1.2

  Updates `platformdirs` from 4.2.2 to 4.3.6
  - [Release notes](https://github.com/tox-dev/platformdirs/releases)
  - [Changelog](https://github.com/tox-dev/platformdirs/blob/main/CHANGES.rst)
  - [Commits](https://github.com/tox-dev/platformdirs/compare/4.2.2...4.3.6)

  Updates `pycodestyle` from 2.12.0 to 2.12.1
  - [Release notes](https://github.com/PyCQA/pycodestyle/releases)
  - [Changelog](https://github.com/PyCQA/pycodestyle/blob/main/CHANGES.txt)
  - [Commits](https://github.com/PyCQA/pycodestyle/compare/2.12.0...2.12.1)

  Updates `pygments` from 2.18.0 to 2.19.1
  - [Release notes](https://github.com/pygments/pygments/releases)
  - [Changelog](https://github.com/pygments/pygments/blob/master/CHANGES)
  - [Commits](https://github.com/pygments/pygments/compare/2.18.0...2.19.1)

  Updates `readme-renderer` from 43.0 to 44.0
  - [Release notes](https://github.com/pypa/readme_renderer/releases)
  - [Changelog](https://github.com/pypa/readme_renderer/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pypa/readme_renderer/compare/43.0...44.0)

  Updates `rich` from 13.7.1 to 13.9.4
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v13.7.1...v13.9.4)

  Updates `setuptools` from 70.1.1 to 75.8.2
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v70.1.1...v75.8.2)

  Updates `six` from 1.16.0 to 1.17.0
  - [Changelog](https://github.com/benjaminp/six/blob/main/CHANGES)
  - [Commits](https://github.com/benjaminp/six/compare/1.16.0...1.17.0)

  Updates `tqdm` from 4.66.4 to 4.67.1
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.66.4...v4.67.1)

  Updates `twine` from 5.1.0 to 6.1.0
  - [Release notes](https://github.com/pypa/twine/releases)
  - [Changelog](https://github.com/pypa/twine/blob/main/docs/changelog.rst)
  - [Commits](https://github.com/pypa/twine/compare/5.1.0...6.1.0)

  Updates `urllib3` from 2.2.2 to 2.3.0
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.2.2...2.3.0)

  Updates `zipp` from 3.19.2 to 3.21.0
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.19.2...v3.21.0)

  ---
  updated-dependencies:
  - dependency-name: autopep8
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: black
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: bleach
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: certifi
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: charset-normalizer
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: click
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: flake8
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: idna
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: keyring
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: more-itertools
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: packaging
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pkginfo
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: platformdirs
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pycodestyle
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: pygments
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: readme-renderer
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: rich
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: six
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: tqdm
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: twine
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: urllib3
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: zipp
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump certifi from 2024.6.2 to 2024.7.4. [dependabot[bot]]

  Bumps [certifi](https://github.com/certifi/python-certifi) from 2024.6.2 to 2024.7.4.
  - [Commits](https://github.com/certifi/python-certifi/compare/2024.06.02...2024.07.04)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-type: direct:production
  ...
- Chore(deps): bump the python-packages group across 1 directory with 3
  updates. [dependabot[bot]]

  Bumps the python-packages group with 3 updates in the / directory: [autopep8](https://github.com/hhatto/autopep8), [importlib-metadata](https://github.com/python/importlib_metadata) and [setuptools](https://github.com/pypa/setuptools).


  Updates `autopep8` from 2.3.0 to 2.3.1
  - [Release notes](https://github.com/hhatto/autopep8/releases)
  - [Commits](https://github.com/hhatto/autopep8/compare/v2.3.0...v2.3.1)

  Updates `importlib-metadata` from 7.2.0 to 7.2.1
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v7.2.0...v7.2.1)

  Updates `setuptools` from 70.1.0 to 70.1.1
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v70.1.0...v70.1.1)

  ---
  updated-dependencies:
  - dependency-name: autopep8
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group across 1 directory with 2
  updates. [dependabot[bot]]

  Bumps the python-packages group with 2 updates in the / directory: [importlib-metadata](https://github.com/python/importlib_metadata) and [setuptools](https://github.com/pypa/setuptools).


  Updates `importlib-metadata` from 7.1.0 to 7.2.0
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v7.1.0...v7.2.0)

  Updates `setuptools` from 70.0.0 to 70.1.0
  - [Release notes](https://github.com/pypa/setuptools/releases)
  - [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst)
  - [Commits](https://github.com/pypa/setuptools/compare/v70.0.0...v70.1.0)

  ---
  updated-dependencies:
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: setuptools
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 3 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 3 updates: [autopep8](https://github.com/hhatto/autopep8), [flake8](https://github.com/pycqa/flake8) and [pycodestyle](https://github.com/PyCQA/pycodestyle).


  Updates `autopep8` from 2.2.0 to 2.3.0
  - [Release notes](https://github.com/hhatto/autopep8/releases)
  - [Commits](https://github.com/hhatto/autopep8/compare/v2.2.0...v2.3.0)

  Updates `flake8` from 7.0.0 to 7.1.0
  - [Commits](https://github.com/pycqa/flake8/compare/7.0.0...7.1.0)

  Updates `pycodestyle` from 2.11.1 to 2.12.0
  - [Release notes](https://github.com/PyCQA/pycodestyle/releases)
  - [Changelog](https://github.com/PyCQA/pycodestyle/blob/main/CHANGES.txt)
  - [Commits](https://github.com/PyCQA/pycodestyle/compare/2.11.1...2.12.0)

  ---
  updated-dependencies:
  - dependency-name: autopep8
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: flake8
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pycodestyle
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump urllib3 from 2.2.1 to 2.2.2. [dependabot[bot]]

  Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.2.1 to 2.2.2.
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.2.1...2.2.2)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-type: direct:production
  ...
- Chore(deps): bump the python-packages group across 1 directory with 7
  updates. [dependabot[bot]]

  Bumps the python-packages group with 7 updates in the / directory:

  | Package | From | To |
  | --- | --- | --- |
  | [autopep8](https://github.com/hhatto/autopep8) | `2.1.1` | `2.2.0` |
  | [certifi](https://github.com/certifi/python-certifi) | `2024.2.2` | `2024.6.2` |
  | [more-itertools](https://github.com/more-itertools/more-itertools) | `10.2.0` | `10.3.0` |
  | [packaging](https://github.com/pypa/packaging) | `24.0` | `24.1` |
  | [pkginfo](https://code.launchpad.net/~tseaver/pkginfo/trunk) | `1.10.0` | `1.11.1` |
  | [requests](https://github.com/psf/requests) | `2.32.2` | `2.32.3` |
  | [zipp](https://github.com/jaraco/zipp) | `3.18.2` | `3.19.2` |



  Updates `autopep8` from 2.1.1 to 2.2.0
  - [Release notes](https://github.com/hhatto/autopep8/releases)
  - [Commits](https://github.com/hhatto/autopep8/compare/v2.1.1...v2.2.0)

  Updates `certifi` from 2024.2.2 to 2024.6.2
  - [Commits](https://github.com/certifi/python-certifi/compare/2024.02.02...2024.06.02)

  Updates `more-itertools` from 10.2.0 to 10.3.0
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v10.2.0...v10.3.0)

  Updates `packaging` from 24.0 to 24.1
  - [Release notes](https://github.com/pypa/packaging/releases)
  - [Changelog](https://github.com/pypa/packaging/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pypa/packaging/compare/24.0...24.1)

  Updates `pkginfo` from 1.10.0 to 1.11.1

  Updates `requests` from 2.32.2 to 2.32.3
  - [Release notes](https://github.com/psf/requests/releases)
  - [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md)
  - [Commits](https://github.com/psf/requests/compare/v2.32.2...v2.32.3)

  Updates `zipp` from 3.18.2 to 3.19.2
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.18.2...v3.19.2)

  ---
  updated-dependencies:
  - dependency-name: autopep8
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: certifi
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: more-itertools
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: packaging
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pkginfo
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: requests
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: zipp
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore: update python version in lint workflow. [Jose Diaz-Gonzalez]
- Chore: update python version in lint workflow. [Jose Diaz-Gonzalez]
- --- updated-dependencies: - dependency-name: autopep8   dependency-
  type: direct:production   update-type: version-update:semver-patch
  dependency-group: python-packages - dependency-name: black
  dependency-type: direct:production   update-type: version-
  update:semver-minor   dependency-group: python-packages - dependency-
  name: docutils   dependency-type: direct:production   update-type:
  version-update:semver-minor   dependency-group: python-packages -
  dependency-name: keyring   dependency-type: direct:production
  update-type: version-update:semver-minor   dependency-group: python-
  packages - dependency-name: platformdirs   dependency-type:
  direct:production   update-type: version-update:semver-patch
  dependency-group: python-packages - dependency-name: pygments
  dependency-type: direct:production   update-type: version-
  update:semver-minor   dependency-group: python-packages - dependency-
  name: requests   dependency-type: direct:production   update-type:
  version-update:semver-minor   dependency-group: python-packages -
  dependency-name: tqdm   dependency-type: direct:production   update-
  type: version-update:semver-patch   dependency-group: python-packages
  - dependency-name: twine   dependency-type: direct:production
  update-type: version-update:semver-minor   dependency-group: python-
  packages - dependency-name: zipp   dependency-type: direct:production
  update-type: version-update:semver-patch   dependency-group: python-
  packages ... [dependabot[bot]]
- Chore: update supported python versions. [Jose Diaz-Gonzalez]
- --- updated-dependencies: - dependency-name: requests   dependency-
  type: direct:production ... [dependabot[bot]]
- Chore(deps): bump tqdm from 4.66.2 to 4.66.3. [dependabot[bot]]

  Bumps [tqdm](https://github.com/tqdm/tqdm) from 4.66.2 to 4.66.3.
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.66.2...v4.66.3)

  ---
  updated-dependencies:
  - dependency-name: tqdm
    dependency-type: direct:production
  ...
- Chore(deps): bump idna from 3.6 to 3.7. [dependabot[bot]]

  Bumps [idna](https://github.com/kjd/idna) from 3.6 to 3.7.
  - [Release notes](https://github.com/kjd/idna/releases)
  - [Changelog](https://github.com/kjd/idna/blob/master/HISTORY.rst)
  - [Commits](https://github.com/kjd/idna/compare/v3.6...v3.7)

  ---
  updated-dependencies:
  - dependency-name: idna
    dependency-type: direct:production
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [keyring](https://github.com/jaraco/keyring).


  Updates `keyring` from 25.0.0 to 25.1.0
  - [Release notes](https://github.com/jaraco/keyring/releases)
  - [Changelog](https://github.com/jaraco/keyring/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/keyring/compare/v25.0.0...v25.1.0)

  ---
  updated-dependencies:
  - dependency-name: keyring
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [jaraco-classes](https://github.com/jaraco/jaraco.classes).


  Updates `jaraco-classes` from 3.3.1 to 3.4.0
  - [Release notes](https://github.com/jaraco/jaraco.classes/releases)
  - [Changelog](https://github.com/jaraco/jaraco.classes/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/jaraco.classes/compare/v3.3.1...v3.4.0)

  ---
  updated-dependencies:
  - dependency-name: jaraco-classes
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [keyring](https://github.com/jaraco/keyring).


  Updates `keyring` from 24.3.1 to 25.0.0
  - [Release notes](https://github.com/jaraco/keyring/releases)
  - [Changelog](https://github.com/jaraco/keyring/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/keyring/compare/v24.3.1...v25.0.0)

  ---
  updated-dependencies:
  - dependency-name: keyring
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [importlib-metadata](https://github.com/python/importlib_metadata).


  Updates `importlib-metadata` from 7.0.2 to 7.1.0
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v7.0.2...v7.1.0)

  ---
  updated-dependencies:
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [autopep8](https://github.com/hhatto/autopep8) and [black](https://github.com/psf/black).


  Updates `autopep8` from 2.0.4 to 2.1.0
  - [Release notes](https://github.com/hhatto/autopep8/releases)
  - [Commits](https://github.com/hhatto/autopep8/compare/v2.0.4...v2.1.0)

  Updates `black` from 24.2.0 to 24.3.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/24.2.0...24.3.0)

  ---
  updated-dependencies:
  - dependency-name: autopep8
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: black
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [zipp](https://github.com/jaraco/zipp).


  Updates `zipp` from 3.18.0 to 3.18.1
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.18.0...v3.18.1)

  ---
  updated-dependencies:
  - dependency-name: zipp
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [zipp](https://github.com/jaraco/zipp).


  Updates `zipp` from 3.17.0 to 3.18.0
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.17.0...v3.18.0)

  ---
  updated-dependencies:
  - dependency-name: zipp
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [importlib-metadata](https://github.com/python/importlib_metadata) and [packaging](https://github.com/pypa/packaging).


  Updates `importlib-metadata` from 7.0.1 to 7.0.2
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v7.0.1...v7.0.2)

  Updates `packaging` from 23.2 to 24.0
  - [Release notes](https://github.com/pypa/packaging/releases)
  - [Changelog](https://github.com/pypa/packaging/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pypa/packaging/compare/23.2...24.0)

  ---
  updated-dependencies:
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: packaging
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [pkginfo](https://code.launchpad.net/~tseaver/pkginfo/trunk) and [rich](https://github.com/Textualize/rich).


  Updates `pkginfo` from 1.9.6 to 1.10.0

  Updates `rich` from 13.7.0 to 13.7.1
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v13.7.0...v13.7.1)

  ---
  updated-dependencies:
  - dependency-name: pkginfo
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: rich
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [keyring](https://github.com/jaraco/keyring).


  Updates `keyring` from 24.3.0 to 24.3.1
  - [Release notes](https://github.com/jaraco/keyring/releases)
  - [Changelog](https://github.com/jaraco/keyring/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/keyring/compare/v24.3.0...v24.3.1)

  ---
  updated-dependencies:
  - dependency-name: keyring
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [readme-renderer](https://github.com/pypa/readme_renderer).


  Updates `readme-renderer` from 42.0 to 43.0
  - [Release notes](https://github.com/pypa/readme_renderer/releases)
  - [Changelog](https://github.com/pypa/readme_renderer/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pypa/readme_renderer/compare/42.0...43.0)

  ---
  updated-dependencies:
  - dependency-name: readme-renderer
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [urllib3](https://github.com/urllib3/urllib3).


  Updates `urllib3` from 2.2.0 to 2.2.1
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.2.0...2.2.1)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [black](https://github.com/psf/black).


  Updates `black` from 24.1.1 to 24.2.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/24.1.1...24.2.0)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [tqdm](https://github.com/tqdm/tqdm) and [twine](https://github.com/pypa/twine).


  Updates `tqdm` from 4.66.1 to 4.66.2
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.66.1...v4.66.2)

  Updates `twine` from 4.0.2 to 5.0.0
  - [Release notes](https://github.com/pypa/twine/releases)
  - [Changelog](https://github.com/pypa/twine/blob/main/docs/changelog.rst)
  - [Commits](https://github.com/pypa/twine/compare/4.0.2...5.0.0)

  ---
  updated-dependencies:
  - dependency-name: tqdm
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: twine
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [jaraco-classes](https://github.com/jaraco/jaraco.classes).


  Updates `jaraco-classes` from 3.3.0 to 3.3.1
  - [Release notes](https://github.com/jaraco/jaraco.classes/releases)
  - [Changelog](https://github.com/jaraco/jaraco.classes/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/jaraco.classes/compare/v3.3.0...v3.3.1)

  ---
  updated-dependencies:
  - dependency-name: jaraco-classes
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [certifi](https://github.com/certifi/python-certifi).


  Updates `certifi` from 2023.11.17 to 2024.2.2
  - [Commits](https://github.com/certifi/python-certifi/compare/2023.11.17...2024.02.02)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [platformdirs](https://github.com/platformdirs/platformdirs) and [urllib3](https://github.com/urllib3/urllib3).


  Updates `platformdirs` from 4.1.0 to 4.2.0
  - [Release notes](https://github.com/platformdirs/platformdirs/releases)
  - [Changelog](https://github.com/platformdirs/platformdirs/blob/main/CHANGES.rst)
  - [Commits](https://github.com/platformdirs/platformdirs/compare/4.1.0...4.2.0)

  Updates `urllib3` from 2.1.0 to 2.2.0
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.1.0...2.2.0)

  ---
  updated-dependencies:
  - dependency-name: platformdirs
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: urllib3
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [black](https://github.com/psf/black).


  Updates `black` from 24.1.0 to 24.1.1
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/24.1.0...24.1.1)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 6 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 6 updates:

  | Package | From | To |
  | --- | --- | --- |
  | [black](https://github.com/psf/black) | `23.11.0` | `24.1.0` |
  | [flake8](https://github.com/pycqa/flake8) | `6.1.0` | `7.0.0` |
  | [importlib-metadata](https://github.com/python/importlib_metadata) | `7.0.0` | `7.0.1` |
  | [more-itertools](https://github.com/more-itertools/more-itertools) | `10.1.0` | `10.2.0` |
  | [pathspec](https://github.com/cpburnz/python-pathspec) | `0.11.2` | `0.12.1` |
  | [pyflakes](https://github.com/PyCQA/pyflakes) | `3.1.0` | `3.2.0` |


  Updates `black` from 23.11.0 to 24.1.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/23.11.0...24.1.0)

  Updates `flake8` from 6.1.0 to 7.0.0
  - [Commits](https://github.com/pycqa/flake8/compare/6.1.0...7.0.0)

  Updates `importlib-metadata` from 7.0.0 to 7.0.1
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v7.0.0...v7.0.1)

  Updates `more-itertools` from 10.1.0 to 10.2.0
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v10.1.0...v10.2.0)

  Updates `pathspec` from 0.11.2 to 0.12.1
  - [Release notes](https://github.com/cpburnz/python-pathspec/releases)
  - [Changelog](https://github.com/cpburnz/python-pathspec/blob/master/CHANGES.rst)
  - [Commits](https://github.com/cpburnz/python-pathspec/compare/v0.11.2...v0.12.1)

  Updates `pyflakes` from 3.1.0 to 3.2.0
  - [Changelog](https://github.com/PyCQA/pyflakes/blob/main/NEWS.rst)
  - [Commits](https://github.com/PyCQA/pyflakes/compare/3.1.0...3.2.0)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: flake8
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: more-itertools
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pathspec
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pyflakes
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...


0.5.1 (2023-12-09)
------------------

Fix
~~~
- Ensure wheel is installed. [Jose Diaz-Gonzalez]

Other
~~~~~
- Chore(deps): bump the python-packages group with 15 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 15 updates:

  | Package | From | To |
  | --- | --- | --- |
  | [bleach](https://github.com/mozilla/bleach) | `6.0.0` | `6.1.0` |
  | [certifi](https://github.com/certifi/python-certifi) | `2023.7.22` | `2023.11.17` |
  | [charset-normalizer](https://github.com/Ousret/charset_normalizer) | `3.1.0` | `3.3.2` |
  | [idna](https://github.com/kjd/idna) | `3.4` | `3.6` |
  | [importlib-metadata](https://github.com/python/importlib_metadata) | `6.6.0` | `7.0.0` |
  | [jaraco-classes](https://github.com/jaraco/jaraco.classes) | `3.2.3` | `3.3.0` |
  | [keyring](https://github.com/jaraco/keyring) | `23.13.1` | `24.3.0` |
  | [markdown-it-py](https://github.com/executablebooks/markdown-it-py) | `2.2.0` | `3.0.0` |
  | [more-itertools](https://github.com/more-itertools/more-itertools) | `9.1.0` | `10.1.0` |
  | [pygments](https://github.com/pygments/pygments) | `2.15.1` | `2.17.2` |
  | [readme-renderer](https://github.com/pypa/readme_renderer) | `37.3` | `42.0` |
  | [rich](https://github.com/Textualize/rich) | `13.3.5` | `13.7.0` |
  | [tqdm](https://github.com/tqdm/tqdm) | `4.65.0` | `4.66.1` |
  | [urllib3](https://github.com/urllib3/urllib3) | `2.0.7` | `2.1.0` |
  | [zipp](https://github.com/jaraco/zipp) | `3.15.0` | `3.17.0` |


  Updates `bleach` from 6.0.0 to 6.1.0
  - [Changelog](https://github.com/mozilla/bleach/blob/main/CHANGES)
  - [Commits](https://github.com/mozilla/bleach/compare/v6.0.0...v6.1.0)

  Updates `certifi` from 2023.7.22 to 2023.11.17
  - [Commits](https://github.com/certifi/python-certifi/compare/2023.07.22...2023.11.17)

  Updates `charset-normalizer` from 3.1.0 to 3.3.2
  - [Release notes](https://github.com/Ousret/charset_normalizer/releases)
  - [Changelog](https://github.com/Ousret/charset_normalizer/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Ousret/charset_normalizer/compare/3.1.0...3.3.2)

  Updates `idna` from 3.4 to 3.6
  - [Changelog](https://github.com/kjd/idna/blob/master/HISTORY.rst)
  - [Commits](https://github.com/kjd/idna/compare/v3.4...v3.6)

  Updates `importlib-metadata` from 6.6.0 to 7.0.0
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v6.6.0...v7.0.0)

  Updates `jaraco-classes` from 3.2.3 to 3.3.0
  - [Release notes](https://github.com/jaraco/jaraco.classes/releases)
  - [Changelog](https://github.com/jaraco/jaraco.classes/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/jaraco.classes/compare/v3.2.3...v3.3.0)

  Updates `keyring` from 23.13.1 to 24.3.0
  - [Release notes](https://github.com/jaraco/keyring/releases)
  - [Changelog](https://github.com/jaraco/keyring/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/keyring/compare/v23.13.1...v24.3.0)

  Updates `markdown-it-py` from 2.2.0 to 3.0.0
  - [Release notes](https://github.com/executablebooks/markdown-it-py/releases)
  - [Changelog](https://github.com/executablebooks/markdown-it-py/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/executablebooks/markdown-it-py/compare/v2.2.0...v3.0.0)

  Updates `more-itertools` from 9.1.0 to 10.1.0
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v9.1.0...v10.1.0)

  Updates `pygments` from 2.15.1 to 2.17.2
  - [Release notes](https://github.com/pygments/pygments/releases)
  - [Changelog](https://github.com/pygments/pygments/blob/master/CHANGES)
  - [Commits](https://github.com/pygments/pygments/compare/2.15.1...2.17.2)

  Updates `readme-renderer` from 37.3 to 42.0
  - [Release notes](https://github.com/pypa/readme_renderer/releases)
  - [Changelog](https://github.com/pypa/readme_renderer/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pypa/readme_renderer/compare/37.3...42.0)

  Updates `rich` from 13.3.5 to 13.7.0
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v13.3.5...v13.7.0)

  Updates `tqdm` from 4.65.0 to 4.66.1
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.65.0...v4.66.1)

  Updates `urllib3` from 2.0.7 to 2.1.0
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.0.7...2.1.0)

  Updates `zipp` from 3.15.0 to 3.17.0
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.15.0...v3.17.0)

  ---
  updated-dependencies:
  - dependency-name: bleach
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: certifi
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: charset-normalizer
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: idna
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: jaraco-classes
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: keyring
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: markdown-it-py
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: more-itertools
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: pygments
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: readme-renderer
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: rich
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: tqdm
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: urllib3
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: zipp
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Tests: lint potential code releases. [Jose Diaz-Gonzalez]


0.5.0 (2023-12-09)
------------------
- Feat: add dependabot configuration to repository. [Jose Diaz-Gonzalez]
- Chore: sort out automated releases and cleanup codebase. [Jose Diaz-
  Gonzalez]


0.4.0 (2022-11-28)
------------------
- Feat(*) - add private_key parameter & update readme. [Cyril Heraudet]
- Feat(.gitignore) - comment & add virtual env. [Cyril Heraudet]
- Chore(.gitignore) - ignore id_rsa & id_rsa.pub files. [Cyril Heraudet]


0.3.2 (2020-12-02)
------------------
- Refactor: use twine for releases. [Jose Diaz-Gonzalez]


0.3.1 (2020-12-02)
------------------

Fix
~~~
- Correct flag. [Jose Diaz-Gonzalez]

Other
~~~~~
- Chore: update release script. [Jose Diaz-Gonzalez]
- Create PULL_REQUEST.md. [Jose Diaz-Gonzalez]
- Create ISSUE_TEMPLATE.md. [Jose Diaz-Gonzalez]


0.3.0 (2019-05-06)
------------------
- Add --with-membership option. [Konstantin Sorokin]

  Specifying this option will allow backup projects the user or key is member of.
  This also include projects filtered by --owned-only option.


0.2.0 (2019-01-31)
------------------
- Added space before the owned boolean check. [Matthew Sheats]
- Added a flag to allow processing only the projects owned by the user
  or key. [Matthew Sheats]


0.1.1 (2018-03-24)
------------------
- Chore: drop Python 2.6. [Jose Diaz-Gonzalez]


0.1.0 (2018-03-24)
------------------
- Initial commit. [Jose Diaz-Gonzalez]


