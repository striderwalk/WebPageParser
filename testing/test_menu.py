import builtins
from unittest import mock

import pytest

import cli


def test_normal():
    options = [cli.MenuOption("normal", "normal")]
    menu = cli.Menu(options)

    with mock.patch.object(builtins, "input", lambda _: "1"):
        assert menu.get_choice() == "normal"


def test_no_response():
    options = [cli.MenuOption("normal", "normal")]
    menu = cli.Menu(options, raise_if_invalid_choice=True)

    with mock.patch.object(builtins, "input", lambda _: ""):
        with pytest.raises(ValueError, match="Selected choice was not a number."):
            menu.get_choice()


def test_str_response():
    options = [cli.MenuOption("normal", "normal")]
    menu = cli.Menu(options, raise_if_invalid_choice=True)

    with mock.patch.object(builtins, "input", lambda _: "word"):
        with pytest.raises(ValueError, match="Selected choice was not a number."):
            menu.get_choice()


def test_float_response():
    options = [cli.MenuOption("normal", "normal")]
    menu = cli.Menu(options, raise_if_invalid_choice=True)

    with mock.patch.object(builtins, "input", lambda _: "3.1415"):
        with pytest.raises(ValueError, match="Selected choice was not a number."):
            menu.get_choice()


def test_out_of_range_response():
    options = [cli.MenuOption("normal", "normal")]
    menu = cli.Menu(options, raise_if_invalid_choice=True)

    with mock.patch.object(builtins, "input", lambda _: "3"):
        with pytest.raises(
            ValueError, match="Selected choice was not one of the options."
        ):
            menu.get_choice()
