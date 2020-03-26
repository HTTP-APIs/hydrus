"""Test for checking Cli"""
from click.testing import CliRunner

from cli import startserver


def test_startserver():
    runner = CliRunner()
    # Starting server with valid parameters
    result = runner.invoke(startserver,
                           ["--adduser", "--api", "--no-auth", "--dburl",
                            "--hydradoc", "--port", "--no-token", "--serverurl",
                            "serve"])
    result.exit_code != 0

    # Starting server with invalid parameters
    result = runner.invoke(startserver,
                           ["--adduser", "sqlite://not-valid", "http://localhost",
                            "--port", "serve"])
    assert result.exit_code == 2
