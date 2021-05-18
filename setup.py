import setuptools


def get_readme():
    with open('README.rst') as f:
        return f.read()


setuptools.setup(
    # the first three fields are a must according to the documentation
    name="pytubekit",
    version="0.0.19",
    packages=[
        'pytubekit',
    ],
    # from here all is optional
    description="Pytubekit will allow you to perform operations in your youtube account en masse",
    long_description=get_readme(),
    long_description_content_type="text/x-rst",
    author="Mark Veltzer",
    author_email="mark.veltzer@gmail.com",
    maintainer="Mark Veltzer",
    maintainer_email="mark.veltzer@gmail.com",
    keywords=[
        'google',
        'youtube',
        'playlist',
        'videos',
    ],
    url="https://veltzer.github.io/pytubekit",
    download_url="https://github.com/veltzer/pytubekit",
    license="MIT",
    platforms=[
        'python3',
    ],
    install_requires=[
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'pygooglehelper',
        'pytconf',
        'pylogconf',
        'pyvardump',
    ],
    extras_require={
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    data_files=[
    ],
    entry_points={"console_scripts": [
        'pytubekit=pytubekit.main:main',
    ]},
    python_requires=">=3.6",
)
