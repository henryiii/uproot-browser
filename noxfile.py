from __future__ import annotations

import nox

nox.needs_version = ">=2024.3.2"
nox.options.default_venv_backend = "uv|virtualenv"
nox.options.sessions = ["lint", "pylint", "tests"]


@nox.session(reuse_venv=True)
def lint(session: nox.Session) -> None:
    """
    Run the linter.
    """
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session
def tests(session: nox.Session) -> None:
    """
    Run the unit and regular tests.
    """
    session.install("-e.[test]")
    session.run("pytest", *session.posargs)


@nox.session(reuse_venv=True)
def minimums(session: nox.Session) -> None:
    """
    Run the unit and regular tests.
    """
    session.install("-e.[test]", "-ctests/constraints.txt")
    session.run("pytest", *session.posargs)


@nox.session()
def run(session: nox.Session) -> None:
    """
    Install and run.
    """
    session.install("-e.", "--compile")
    session.run("uproot-browser", *session.posargs)


@nox.session
def pylint(session: nox.Session) -> None:
    """
    Run pylint.
    """

    session.install("-e.", "pylint", "matplotlib")
    session.run("pylint", "src", *session.posargs)


@nox.session(reuse_venv=True)
def build(session: nox.Session) -> None:
    """
    Build an SDist and wheel.
    """

    session.install("build")
    session.run("python", "-m", "build")


@nox.session
def make_logo(session: nox.Session) -> None:
    """
    Rerender the logo.
    """

    session.install("pillow")
    session.run("python", "docs/make_logo.py")
