from setuptools import find_packages, setup

with open('README.md', encoding="UTF-8") as file:
    readme = file.read()

with open('LICENSE', encoding="UTF-8") as file:
    app_license = file.read()

setup(
    name='family-tree',
    version='0.1',
    description='Command-line tool for generating a family tree as a svg/pdf format graphic',
    long_description=readme,
    author='MaciejMagic',
    url='https://github.com/MaciejMagic/family-tree',
    license=app_license,
    packages=find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    py_modules=['graphviz', 'validator_collection'],
    keywords=['graph', 'digraph', 'graphviz', 'visualize', 'svg', 'pdf']
)
