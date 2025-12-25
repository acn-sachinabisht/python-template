import tomllib

from invoke import Context, task
from pydantic import BaseModel, ValidationError


class ProjectMeta(BaseModel):  # type: ignore[misc]
    name: str
    version: str
    gui_support: bool = False


def projectDetail() -> tuple[str, str, bool]:
    """
    Read project details from pyproject.toml and validate with Pydantic.
    Returns:
        name (str): Project name
        version (str): Project version
        gui_support (bool): True if GUI support is enabled, else False
    """
    with open("pyproject.toml", "rb") as f:
        content = tomllib.load(f)
    project = content.get("project", {})
    data = {
        "name": project.get("name", "app"),
        "version": project.get("version", "0.0.0"),
        "gui_support": project.get("gui-support", False),
    }
    try:
        meta = ProjectMeta(**data)
    except ValidationError as e:
        print("Project metadata validation error:", e)
        raise
    return meta.name, meta.version, meta.gui_support


@task(optional=["gui"])  # type: ignore[misc]
def app(c: Context, gui: bool = False) -> None:
    """
    Run the application.
    If --gui is passed and GUI support is enabled, runs the GUI version.
    Otherwise, runs the CLI version.
    """
    _, _, guiSupport = projectDetail()
    gui = str(gui).lower() == "true"
    if gui and not guiSupport:
        print("GUI support is not enabled for this project.")
        return
    c.run("python src/core/gui.py" if gui else "python src/core/main.py")


@task  # type: ignore[misc]
def freeze(c: Context) -> None:
    """
    Freeze current environment packages to requirements.txt using uv.
    """
    c.run("uv pip freeze > requirements.txt")


@task(optional=["gui"])  # type: ignore[misc]
def build(c: Context, gui: bool = False) -> None:
    """
    Build a standalone executable with a versioned name from pyproject.toml.
    Pass --gui=True to build src/core/gui.py (if GUI support is enabled).
    Otherwise, builds src/core/main.py.
    """
    name, version, gui_support = projectDetail()
    gui = str(gui).lower() == "true"
    if gui and not gui_support:
        print("GUI support is not enabled for this application.")
        return
    script = "src/core/gui.py" if gui else "src/core/main.py"
    app_name = f"{name}-gui-{version}" if gui else f"{name}-{version}"
    result = c.run(f"pyinstaller --onefile {script} --name {app_name}")
    if result.ok:
        print(f"Built exe: dist/{app_name}.exe")
    else:
        print("Build failed! See output below:")
        print(result.stderr or result.stdout)


@task  # type: ignore[misc]
def tests(c: Context) -> None:
    """
    Run all pytest unit tests and generate an HTML report.
    """
    c.run("pytest tests/  --html=build/reports/report.html --self-contained-html")


@task  # type: ignore[misc]
def ci(c: Context) -> None:
    """
    Sync the environment with pyproject.toml using uv and report status.
    """
    result = c.run("uv sync")
    if result.ok and not result.stdout.strip():
        print("Environment is up to date.")
    else:
        print("there was an error:")
        print(result.stdout or result.stderr)
