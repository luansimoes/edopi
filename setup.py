from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='edopi',
    version='1.0.0',
    url='https://github.com/luansimoes/edopi',
    license='MIT License',
    author='Flavia Elias e Luan Simões',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='luansimoes@id.uff.br',
    keywords='microtonal edo music group-theoretic',
    description='Python package to deal with Group-Theoretic microtonal music structures',
    packages=find_packages(include=['edopi', 'edopi.*']),
    install_requires=['numpy','matplotlib'],)
