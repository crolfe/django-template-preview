import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    README = f.read()


setup(
    name='django-template-preview',
    version='0.1.4',
    packages=find_packages(),
    include_package_data=True,
    description='A Django app to preview rendered templates in your browser.',
    long_description=README,
    url='https://github.com/crolfe/django-template-preview/',
    author='Colin Rolfe',
    license='Apache',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
