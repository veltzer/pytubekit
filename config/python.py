import config.project

package_name = config.project.project_name

console_scripts = [
    "pytubekit=pytubekit.main:main",
]

setup_requires = []

run_requires = [
    "google-api-python-client",
    "google-auth-httplib2",
    "google-auth-oauthlib",
    "pygooglehelper",
    "pytconf",
    "pylogconf",
    "pyvardump",
    "youtube-dl",
    "browsercookie",
]

test_requires = [
    "pytest",
    "pytest-cov",
    "pylint",
    "flake8",
    "pymakehelper",
]

dev_requires = [
    "pyclassifiers",
    "pypitools",
    "pydmt",
    "Sphinx",
    "black",
]

install_requires = list(setup_requires)
install_requires.extend(run_requires)

python_requires = ">=3.7"

extras_require = {
}
test_os = "[ubuntu-20.04]"
test_python = "[3.7, 3.8, 3.9]"
test_container = "[ubuntu:20.04]"
