from setuptools import setup

setup(
    name='family-tree',
    version='1.0',
    author='MaciejMagic',
    description='Command-line tool for generating a family tree as a svg/pdf format graphic',
    url='https://github.com/MaciejMagic/family-tree',
    keywords='graph, visualize, svg',
    python_requires='>=3.10, <4',
    install_requires=[
        'graphviz>=0.20.1',
        'pytest>=7.2.2',
        'validator-collection>=1.5.0'
    ],
    package_data={
        'tree': ['tree.db'],
    },
    entry_points={
        'runners': [
            'main=app:main',
        ]
    }
)
