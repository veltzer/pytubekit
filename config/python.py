""" python deps for this project """

scripts: dict[str, str] = {
    "pytubekit": "pytubekit.main:main",
}

config_requires: list[str] = [
    "pyclassifiers",
]
install_requires: list[str] = [
    "google-api-python-client",
    "pygooglehelper",
    "pytconf",
    "pylogconf",
    "pyvardump",
    "youtube-dl",
    "browsercookie",
]
build_requires: list[str] = [
    "pydmt",
    "pymakehelper",
]
test_requires: list[str] = [
    "pytest",
    "pylint",
    "mypy",
    "ruff",
]
requires = config_requires + install_requires + build_requires + test_requires
