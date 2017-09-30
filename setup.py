import re

from os import path
from codecs import open
from setuptools import setup, find_packages

__version__ = '1.0.0'

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('-e ', '') for x in all_reqs if x.startswith('-e git+')]

for pkg in dependency_links:
    install_requires.append(re.findall(r'.*/(.*?)\.git', pkg)[0])


setup(
    name='snowman_teste',
    version=__version__,
    description='Teste para Snowman',
    long_description=long_description,
    url='https://github.com/paraizofelipe/snowman_teste',
    download_url='https://github.com/paraizofelipe/snowman_teste/tarball/' + __version__,
    license='BSD',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Felipe Paraizo',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='felipeparaizo@gmail.com.br'
)
