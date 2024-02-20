import sys
from setuptools import setup, find_packages

with open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='eday',
    version='1.0.2',
    description='A package for converting between dates and epoch days',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/mindey/eday',
    author='Your Name',
    author_email='mindey@mindey.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='epoch days date time datetime conversion utility',
    packages=find_packages(),
    install_requires=['python-dateutil'],
    zip_safe=False,
)
