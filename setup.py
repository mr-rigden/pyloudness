from setuptools import setup

setup(name='pyloudness',
      version='1.0',
      description='Find out how loud that file is',
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
