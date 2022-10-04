from setuptools import setup

packages = \
['liggghts']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['importlib_metadata>=4']}

setup_kwargs = {
    'name': 'liggghts',
    'version': '3.8.0',
    'description': 'Discrete Element Method Particle Simulation Software',
    'author': 'DCS Computing',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.cfdem.com',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
