from setuptools import setup

setup(
    name='awesome-search',
    version='0.1.2',
    packages=['search_cli'],
    entry_points='''
        [console_scripts]
        awesome=search_cli.awesome_search:main
    ''',
    install_requires=[]
)
