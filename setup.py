from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='edopi',
    version='0.0.3',
    url='https://github.com/luansimoes/edopi',
    license='MIT License',
    author='Flavia Elias e Luan Simões',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='luansimoes@id.uff.br',
    keywords='Pacote',
    description='Pacote PyPI para musica microtonal',
    packages=find_packages(include=['edopi', 'edopi.*']),
    install_requires=['numpy','matplotlib'],)
