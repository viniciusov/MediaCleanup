from setuptools import setup

setup(
    name = 'MediaCleanup',
    version = '1.1',
    description = 'Cleanup your Media files and folders',
    author = 'Vinícius Orsi Valente',
    author_email = 'viniciusov@hotmail.com',
    py_modules = ['mediacleanup'],
    install_requires = ['Send2Trash'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ]
)
