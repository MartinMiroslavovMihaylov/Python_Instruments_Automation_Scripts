# Project Documentation (Sphinx) — `docu` branch

This branch contains only the **Sphinx sources**.  
Docs are built on every push to `main` and deployed to **GitHub Pages** via GitHub Actions.

## GitHub Pages (CI/CD)

The workflow lives on **`main`** (not here). Create `.github/workflows/docs.yml` on `main`.

Then in the repository: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

### Expected git layout

```
(main)  <repo root>/
  Instruments_Libraries/
  Examples/
  ...

(docu)  <this branch root>/
  conf.py
  index.rst (or .md)
  _rst/  _static/  _templates/
  Examples/*.rst
  requirements-docs.txt
```


## Build locally

> Prereqs: Python 3.11+, `pip` (ideally inside a virtualenv).

### About the layout
Sphinx needs to import your package to build API docs. This `docu` branch assumes you have a **sibling checkout** of your code at `../Python_Instruments_Automation_Scripts` relative to this folder, e.g.:

```
/parent-folder/
  ├─ Python_Instruments_Automation_Scripts/   # your code repo (branch: main)
  └─ Documentation/                           # this docs worktree/clone (branch: docu)
```

Create a git worktree. From the main branch run:
```
git fetch origin
git worktree add ../Documentation docu
git worktree list
```

To delete run:
```
git worktree remove ../Documentation
```

If your code is elsewhere, that’s fine—**set `CODE_DIR` to the absolute path** of the code repo root before building.

### 1) Install doc dependencies
- **bash/Powershell**
  ```bash
  python -m pip install --upgrade pip
  pip install -r requirements-docs.txt
  ```

### 2) Make the package importable for autodoc (set `CODE_DIR`)

- **Windows (PowerShell)**
  ```powershell
  # If your code is a sibling folder (recommended):
  $env:CODE_DIR = (Resolve-Path ..\Python_Instruments_Automation_Scripts).Path
  # Or point to any absolute path where your code repo lives:
  # $env:CODE_DIR = "C:\path\to\Python_Instruments_Automation_Scripts"
  ```
- **macOS/Linux (bash)**
  ```bash
  # If your code is a sibling folder (recommended):
  export CODE_DIR="$(cd ../Python_Instruments_Automation_Scripts && pwd)"
  # Or point to any absolute path where your code repo lives:
  # export CODE_DIR="/abs/path/to/Python_Instruments_Automation_Scripts"
  ```

### 3) Regenerate API stubs (optional, recommended when modules change)
- **Windows**
  ```powershell
  sphinx-apidoc -o _rst --separate --force --no-toc -t _templates\apidoc ..\Python_Instruments_Automation_Scripts\Instruments_Libraries
  ```
- **macOS/Linux**
  ```bash
  sphinx-apidoc -o _rst --separate --force --no-toc -t _templates/apidoc ../Python_Instruments_Automation_Scripts/Instruments_Libraries
  ```

### 4) Build HTML
- **Windows**
  ```powershell
  .\make.bat html
  ```
- **macOS/Linux**
  ```bash
  make html
  ```

Open `_build/html/index.html` in your browser.

---



