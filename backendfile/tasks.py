
from invoke import task

@task
def test(c):
    c.run("pytest -q tests/test*.py")

@task
def start(c):
    c.run("gunicorn -w 5 appFile:app")

