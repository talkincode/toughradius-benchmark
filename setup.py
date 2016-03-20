#!/usr/bin/python


from setuptools import setup, find_packages
import toughbt

version = toughbt.__version__

install_requires = [
    'six>=1.8.0',
    'Twisted>=15.0.0',
    'txradius',
    'txzmq',
]
install_requires_empty = []

package_data={
    'toughbt': [
        'dictionary',
    ]
}


setup(name='toughbt',
      version=version,
      author='toughmen',
      author_email='wjt.net@outlook.com',
      url='https://github.com/toughmen/toughradius-benchmark',
      license='GPL',
      description='RADIUS tools',
      long_description=open('README.md').read(),
      classifiers=[
       'Development Status :: 6 - Mature',
       'Intended Audience :: Developers',
       'Programming Language :: Python :: 2.6',
       'Programming Language :: Python :: 2.7',
       'Topic :: Software Development :: Libraries :: Python Modules',
       'Topic :: System :: Systems Administration :: Authentication/Directory',
       ],
      packages=find_packages(),
      package_data=package_data,
      keywords=['radius', 'AAA','authentication','accounting','authorization','toughradius','benchmark'],
      zip_safe=True,
      include_package_data=True,
      eager_resources=['toughbt'],
      scripts=["trbctl"],
      install_requires=install_requires,
)