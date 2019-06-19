from setuptools import setup, find_packages

# exec (open('pdia/version.py').read())


def readme():
    with open('README.md') as f:
        return f.read()


__version__ = '0.71'


setup(name='pdia',
      version=__version__,
      use_2to3=False,
      author='Gary Feng',
      author_email='gfeng@ets.org',
      maintainer='Gary Feng',
      maintainer_email='gfeng@ets.org',
      url='https://github.com/naepdev/pdia/',
      description="Python library for NAEP process data",
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
      ],
      license='MIT',
      packages=find_packages(exclude=['examples', 'docs']),
      install_requires=['requests', 'pandas', 'numpy', 'dpath', 'lxml', 'plotly', 'colorlover',
                        'distributed', 'bs4', 'sklearn', 'dask', 'xlrd',
                        'pymssql', 'pyodbc', 'nltk', 'IPython'],
      zip_safe=False)
