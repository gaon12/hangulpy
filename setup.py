# setup.py
# Maintained for backward compatibility
# New installations should use pyproject.toml

from setuptools import setup, find_packages

# Read version from pyproject.toml would be better, but for simplicity:
setup(
    name='hangulpy',
    version='1.3.0',
    description='A comprehensive Python library for Korean language processing, inspired by es-hangul',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/gaon12/hangulpy',
    author='Jeong Gaon',
    author_email='gokirito12@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'ruff>=0.1.0',
            'mypy>=1.5.0',
        ],
        'test': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
    ],
    python_requires='>=3.8',
    package_data={
        'hangulpy': ['py.typed'],
    },
)
