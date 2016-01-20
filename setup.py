from setuptools import setup, find_packages
from codecs import open
from os import path

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pyloudness',
      version='1.1.2',
      description='Find out how loud that file is',
      long_description=long_description,
      url='https://github.com/jrigden/pyloudness',
      author='Jason Rigden',
      author_email='jasonrigden@gmail.com',
      keywords='loudness audio ebu r128',
      license='MIT',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Topic :: Multimedia :: Sound/Audio :: Analysis',
          'License :: OSI Approved :: MIT License',
      ],
      packages=['pyloudness'],
      zip_safe=False)
