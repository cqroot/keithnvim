#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from comm.color import Color
from comm.utils import run_command, parse_version


class Executable(object):
    def __init__(self, name, version_cmd):
        self.__name = name
        self.__version = "unknown"
        self.__is_exist = False
        self.__error = ""

        try:
            ret, out = run_command(version_cmd)
            out = out.splitlines()[0].rstrip("\n")

            if ret != 0:
                self.__error = out
                return

            self.__is_exist = True
            self.__version = parse_version(out)
        except FileNotFoundError:
            self.__is_exist = False

    def name(self):
        return self.__name

    def is_exist(self):
        return self.__is_exist

    def version(self):
        return self.__version

    def error(self):
        return self.__error


def check_executable_version(executable):
    if executable.error():
        print(
            "- %s [%s]: %s"
            % (
                Color.fg_red("ERROR"),
                Color.fg_yellow(executable.name()),
                executable.error(),
            )
        )
        return

    if not executable.is_exist():
        print(
            "- %s [%s]: not ready"
            % (Color.fg_red("ERROR"), Color.fg_yellow(executable.name()))
        )
        return

    print(
        "- %s [%s]: %s"
        % (
            Color.fg_green("OK"),
            Color.fg_yellow(executable.name()),
            parse_version(executable.version()),
        )
    )


def check_executable(title, executables):
    print(Color.fg_blue(title))
    print(Color.fg_blue("=" * len(title)))

    for executable in executables:
        check_executable_version(executable)

    print()


def check_dependencies():
    title = "Check dependencies:"
    dependencies = [
        Executable("python", "python --version"),
        Executable("git", "git --version"),
        Executable("ripgrep", "rg --version"),
    ]
    check_executable(title, dependencies)


def check_lsps():
    title = "Check LSPs:"
    lsps = [
        Executable("bashls", "bash-language-server --version"),
        Executable("clangd", "clangd --version"),
        Executable("gopls", "gopls version"),
        Executable("lua_ls", "lua-language-server --version"),
        Executable("neocmake", "neocmake --version"),
        Executable("pyright", "pyright --version"),
    ]
    check_executable(title, lsps)


def check_formatters():
    title = "Check formatters:"
    formatters = [
        Executable("shfmt", "shfmt --version"),
        Executable("clang-format", "clang-format --version"),
        Executable("cmake_format", "cmake_format --version"),
        Executable("gofumpt", "gofumpt --version"),
        Executable("stylua", "stylua --version"),
        Executable("prettier", "prettier --version"),
        Executable("black", "black --version"),
        Executable("taplo", "taplo --version"),
    ]
    check_executable(title, formatters)


def main():
    check_dependencies()
    check_lsps()
    check_formatters()


if __name__ == "__main__":
    main()
