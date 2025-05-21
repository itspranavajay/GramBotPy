import os
from setuptools import setup, find_packages

# Get the version from __init__.py
with open(os.path.join('GramBotPy', '__init__.py'), 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('"\'')
            break

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='GramBotPy',
    version=version,
    description='Telegram Bot Framework',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='GramBotPy Team',
    author_email='info@GramBotPy.example.com',
    url='https://github.com/GramBotPy/GramBotPy',
    packages=find_packages(),
    keywords=['telegram', 'bot', 'api', 'GramBotPy', 'framework'],
    python_requires='>=3.7',
    install_requires=[
        'aiohttp>=3.8.1',
        'async-timeout>=4.0.2',
        'cryptography>=37.0.4',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: AsyncIO',
    ],
    project_urls={
        'Documentation': 'https://GramBotPy.readthedocs.io',
        'Source': 'https://github.com/GramBotPy/GramBotPy',
        'Tracker': 'https://github.com/GramBotPy/GramBotPy/issues',
    },
) 