from setuptools import setup

setup(
    name='awesome-search',
    version='0.1',
    packages=['cli'],
    entry_points='''
        [console_scripts]
        srch=cli.awesome_search:main
    ''',
    install_requires=[]
)
