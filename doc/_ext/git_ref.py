"""Point every MOVENSYS clone command and source link at one git ref.

The site is published once per version (``main``, ``release-0.1``,
``release-0.2``). Each build sets ``DOCS_GIT_REF`` to the ref it documents, and
this extension rewrites the page sources before they are parsed:

    git clone https://github.com/movensys/wmx-r2.git
 -> git clone -b release-0.1 https://github.com/movensys/wmx-r2.git

    https://github.com/movensys/wmx-r2/blob/main/doc/launch_manipulator.md
 -> https://github.com/movensys/wmx-r2/blob/release-0.1/doc/launch_manipulator.md

Pages are written with the plain commands above; never hard-code a ref.
Clones that already pass ``-b``/``--branch`` and non-MOVENSYS repos are left
alone. ``|git_ref|`` is also available as a substitution in reST prose.

It also adds the version switcher under the sidebar Table of Contents
(templates/sidebar-version-switcher.html). The list of versions is
``/switcher.json`` at the site root, fetched by the browser at runtime. CI
writes it from the published release-* tags (.github/scripts/make_switcher.py),
so a new tag shows up in every version's switcher without a rebuild.
"""

import os
import re

SITE_URL = "https://movensys.github.io/wmx-r2-doc/"
SWITCHER_JSON_URL = SITE_URL + "switcher.json"

_TEMPLATES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
_SWITCHER_TEMPLATE = "sidebar-version-switcher.html"

_REPO = r"(?:https://github\.com/|git@github\.com:)movensys/[\w.-]+"
_CLONE_RE = re.compile(r"\bgit clone(?![^\n]*\s(?:-b|--branch)\s)(?=\s+" + _REPO + ")")
_LINK_RE = re.compile(r"(github\.com/movensys/[\w.-]+/(?:blob|tree)/)main/")


def _rewrite(app, text):
    ref = app.config.git_ref
    text = _CLONE_RE.sub(f"git clone -b {ref}", text)
    return _LINK_RE.sub(rf"\g<1>{ref}/", text)


def _on_source_read(app, docname, source):
    source[0] = _rewrite(app, source[0])


def _on_include_read(app, relative_path, parent_docname, content):
    content[0] = _rewrite(app, content[0])


def _on_config_inited(app, config):
    ref = config.git_ref
    config.rst_epilog = (config.rst_epilog or "") + f"\n.. |git_ref| replace:: ``{ref}``\n"

    options = config.html_theme_options
    options["switcher"] = {"json_url": SWITCHER_JSON_URL, "version_match": ref}
    # The JSON only exists on the deployed site; a build-time fetch
    # would fail the strict (-W) build locally and in PR checks.
    options["check_switcher"] = False

    # Put the switcher under the sidebar Table of Contents on every page.
    config.templates_path = list(config.templates_path) + [_TEMPLATES]
    sidebars = config.html_sidebars or {"**": ["sidebar-nav-bs"]}
    config.html_sidebars = {
        pattern: items if _SWITCHER_TEMPLATE in items else [*items, _SWITCHER_TEMPLATE]
        for pattern, items in sidebars.items()
    }


def setup(app):
    app.add_config_value("git_ref", os.environ.get("DOCS_GIT_REF", "main"), "env")
    app.connect("config-inited", _on_config_inited)
    app.connect("source-read", _on_source_read)
    app.connect("include-read", _on_include_read)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
