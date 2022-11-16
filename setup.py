from distutils.core import setup
from analysis._version import __version__  # noqa

setup(
    name='ConjPolAnalysis',
    version=__version__,
    description='Analysis Package for Molecular Dynamics on Conjugated Polymers',
    author='Nicholas Siemons',
    author_email='nicholas9182@gmail.com',
    packages=[
        'MDAnalysis',
        'pandas',
        'numpy'
    ]
)
