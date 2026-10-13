"""Sphinx config used by CI to build a release tag (see docs-release.yml).

A tag such as ``release-0.1`` was cut before ``_ext/git_ref.py`` existed, so
its own conf.py has no version switcher and no clone-ref rewriting. CI copies
this file to an empty directory as ``conf.py`` and runs
``sphinx-build -c <that dir> <tag>/doc ...``. It loads the tag's conf.py
unchanged, then adds the git_ref extension from the current branch.

Env:
  DOCS_SRC      the tag's doc/ directory
  DOCS_EXT_DIR  directory holding git_ref.py (this branch's doc/_ext)
  DOCS_GIT_REF  the tag name
"""

import os
import sys

_src = os.path.abspath(os.environ['DOCS_SRC'])
_conf = os.path.join(_src, 'conf.py')
sys.path.insert(0, os.path.abspath(os.environ['DOCS_EXT_DIR']))

# Run the tag's conf.py as if Sphinx had loaded it from its own directory.
_cwd = os.getcwd()
os.chdir(_src)
try:
    with open(_conf) as f:
        exec(compile(f.read(), _conf, 'exec'))
finally:
    os.chdir(_cwd)

# Paths in the tag's conf.py are relative to its doc/ directory, but Sphinx
# resolves them against the -c directory. Make them absolute.
for _name in ('templates_path', 'html_static_path', 'html_extra_path'):
    if _name in globals():
        globals()[_name] = [os.path.join(_src, p) for p in globals()[_name]]
for _name in ('html_logo', 'html_favicon'):
    _value = globals().get(_name)
    if _value and '://' not in _value:
        globals()[_name] = os.path.join(_src, _value)

if 'git_ref' not in extensions:
    extensions.append('git_ref')
