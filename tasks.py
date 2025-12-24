import re

from invoke import Context, task


@task(optional=["gui"])  # type: ignore[misc]
def app(c: Context, gui: bool = False) -> None:
    c.run("python gui.py" if gui else "python main.py")


@task  # type: ignore[misc]
def freeze(c: Context) -> None:
    c.run("uv pip freeze > requirements.txt")


@task(optional=["gui"])  # type: ignore[misc]
def build(c: Context, gui: bool = False) -> None:
    """Build standalone exe with versioned name from pyproject.toml. Pass --gui=True to build gui.py."""
    # Read name and version from pyproject.toml
    with open("pyproject.toml") as f:
        content = f.read()
    name_match = re.search(r'name\s*=\s*"([^"]+)"', content)
    version_match = re.search(r'version\s*=\s*"([^"]+)"', content)
    name = name_match.group(1) if name_match else "app"
    version = version_match.group(1) if version_match else "0.0.0"
    if str(gui).lower() == "true":
        script = "gui.py"
        app_name = f"{name}-gui-{version}"
    else:
        script = "main.py"
        app_name = f"{name}-{version}"
    result = c.run(f"pyinstaller --onefile {script} --name {app_name}")
    if result.ok:
        print(f"Built exe: dist/{app_name}.exe")
    else:
        print("Build failed! See output below:")
        print(result.stderr or result.stdout)


@task  # type: ignore[misc]
def tests(c: Context) -> None:
    c.run("pytest tests/  --html=build/reports/report.html --self-contained-html")


@task  # type: ignore[misc]
def ci(c: Context) -> None:
    """Check if uv sync is up to date (dry run)."""
    result = c.run("uv sync")
    if result.ok and not result.stdout.strip():
        print("Environment is up to date.")
    else:
        print("there was an error:")
        print(result.stdout or result.stderr)
