r'''Squall installation script
    Usage: python setup.py install
    
    This script relies on setuptools and/or distribute.
'''#"""#'''

# Copyright 2012 Eric Wald
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

try:
    readme = open('README.txt').read()
except:
    # Todo: Attempt to find the README file.
    readme = None

setup(
    # Provided items
    name = "Squall",
    version = "0.1a",
    packages = ["squall"],
    entry_points = {
        "console_scripts": [
        ],
        "gui_scripts": [
            "squall = squall.main:main",
        ],
    },
    
    # Project metadata
    author = "Eric Wald",
    author_email = "eswald@gmail.com",
    description = "Visual database query interface",
    long_description = readme,
    license = "Apache License, Version 2.0",
    keywords = "database sql mysql gui",
    url = "https://github.com/eswald/squall",
    platforms = "Any",
    classifiers = [
        "Development Status :: 1 - Planning",
        "Environment :: X11 Applications",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Topic :: Database :: Front-Ends",
    ],
    
    # Installation options
    zip_safe = True,
    install_requires = ["distribute"],
)
