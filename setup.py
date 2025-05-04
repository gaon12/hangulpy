from setuptools import setup, find_packages

setup(
	name='hangulpy',
	version='1.2.1',
	description='A Python library for processing Hangul, inspired by es-hangul.',
	long_description=open('README.md', encoding='utf-8').read(),
	long_description_content_type='text/markdown',
	url='https://github.com/gaon12/hangulpy',
	author='Jeong Gaon',
	author_email='gokirito12@gmail.com',
	license='MIT',
	packages=find_packages(),
	install_requires=[],
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
	python_requires='>=3.8',
)
