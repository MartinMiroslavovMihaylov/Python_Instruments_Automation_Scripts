# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os, sys, shutil, subprocess

CODE_DIR = os.environ.get("CODE_DIR")
if not (CODE_DIR and os.path.isdir(CODE_DIR)):
    CODE_DIR = os.path.abspath("../Python_Instruments_Automation_Scripts")
sys.path.insert(0, CODE_DIR)

# --- Expose code examples under 'examples-src' (avoid clashing with docs/Examples) ---
def _mount_examples():
    src = os.path.join(CODE_DIR, "Examples")
    dst = os.path.abspath(os.path.join(os.path.dirname(__file__), "examples-src"))
    if not os.path.isdir(src):
        print(f"[conf.py] No code examples at {src}; skipping.", file=sys.stderr)
        return

    # If already linked to the same place, done
    try:
        if os.path.exists(dst) and os.path.samefile(dst, src):
            return
    except Exception:
        pass

    # Remove old link/dir if it's a link or user forced replacement
    if os.path.exists(dst):
        if os.path.islink(dst):
            os.unlink(dst)
        elif os.environ.get("DOCS_FORCE_EXAMPLES_LINK") == "1":
            shutil.rmtree(dst)
        else:
            print(f"[conf.py] '{dst}' exists and is not a link. Set DOCS_FORCE_EXAMPLES_LINK=1 to replace it.", file=sys.stderr)
            return

    # Try symlink first
    try:
        os.symlink(src, dst, target_is_directory=True)
        print(f"[conf.py] Linked examples-src -> {src}")
        return
    except Exception:
        pass

    # Windows junction fallback
    if os.name == "nt":
        try:
            subprocess.run(["cmd", "/c", "mklink", "/J", dst, src], check=True, shell=True)
            print(f"[conf.py] Junction examples-src -> {src}")
            return
        except Exception:
            pass

    # Last resort: copy
    try:
        shutil.copytree(src, dst)
        print(f"[conf.py] Copied examples to '{dst}' (symlink/junction unavailable)")
    except Exception as e:
        print(f"[conf.py] Failed to expose examples: {e}", file=sys.stderr)

_mount_examples()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Instruments-Libraries"
copyright = "2025, Martin Mihaylov and Maxim Weizel"
author = "Martin Mihaylov and Maxim Weizel"
release = "01.01.2024"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    'sphinx.ext.autosummary',
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    'sphinx_rtd_theme',
]


templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
autodoc_typehints = "description"
# Mock heavy deps so autodoc can import your package without installing them
autodoc_mock_imports = [
    "pyvisa",
    "serial",
    "vxi11",
    "matlab",
    "RsInstrument",
    "ftd2xx",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
    "titles_only": False,
    "includehidden": True,
    "sticky_navigation": True
}
html_static_path = []

# Generate .rst files
# sphinx-apidoc -o _rst --separate --force --no-toc -t _templates\apidoc ..\Python_Instruments_Automation_Scripts\Instruments_Libraries