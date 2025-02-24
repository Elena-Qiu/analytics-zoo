#!/usr/bin/env python

#
# Copyright 2018 Analytics Zoo Authors.
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
#

import os
import sys
from shutil import copyfile, copytree, rmtree
import fnmatch
from setuptools import setup

long_description = '''
[**Analytics Zoo**](https://github.com/intel-analytics/analytics-zoo/)
is an open source _**Big Data AI**_ platform, and includes the following
features for scaling end-to-end AI to distributed Big Data:

- [Orca](https://github.com/intel-analytics/analytics-zoo#getting-started-with-orca):
seamlessly scale out TensorFlow and PyTorch for Big Data (using Spark & Ray)

- [RayOnSpark](https://github.com/intel-analytics/analytics-zoo#getting-started-with-rayonspark):
run Ray programs directly on Big Data clusters

- [BigDL
Extensions](https://github.com/intel-analytics/analytics-zoo#getting-started-with-bigdl-extensions):
high-level Spark ML pipeline and Keras-like APIs for BigDL

- [Chronos](https://github.com/intel-analytics/analytics-zoo#getting-started-with-chronos):
scalable time series analysis using AutoML

- [PPML](https://github.com/intel-analytics/analytics-zoo#ppml-privacy-preserving-machine-learning):
privacy preserving big data analysis and machine learning (*experimental*)

For more information, you may [read the docs](https://analytics-zoo.readthedocs.io/).
'''


TEMP_PATH = "zoo/share"
analytics_zoo_home = os.path.abspath(__file__ + "/../../")
SCRIPTS_TARGET = os.path.join(TEMP_PATH, "bin/cluster-serving")

exclude_patterns = ["*__pycache__*", "*ipynb_checkpoints*", "*chronos.use-case*"]


def get_analytics_zoo_packages():
    analytics_zoo_python_home = analytics_zoo_home + "/pyzoo/zoo"
    analytics_zoo_packages = ['zoo.share']
    for dirpath, dirs, files in os.walk(analytics_zoo_python_home):
        package = dirpath.split(analytics_zoo_home +
                                "/pyzoo/")[1].replace('/', '.')
        if any(fnmatch.fnmatchcase(package, pat=pattern)
                for pattern in exclude_patterns):
            print("excluding", package)
        else:
            analytics_zoo_packages.append(package)
            print("including", package)
    return analytics_zoo_packages


packages = get_analytics_zoo_packages()

try:
    with open('zoo/__init__.py', 'r') as f:
        for line in f.readlines():
            if '__version__' in line:
                VERSION = line.strip().replace("\"", "").split(" ")[2]
except IOError:
    print("Failed to load Analytics Zoo version file for packaging. \
      You must be in Analytics Zoo's pyzoo dir.")
    sys.exit(-1)

building_error_msg = """
If you are packing python API from zoo source, you must build Analytics Zoo first
and run sdist.
    To build Analytics Zoo with maven you can run:
      cd $ANALYTICS_ZOO_HOME
      ./make-dist.sh
    Building the source dist is done in the Python directory:
      cd $ANALYTICS_ZOO_HOME/pyzoo
      python setup.py sdist
      pip install dist/*.tar.gz"""


def build_from_source():
    code_path = analytics_zoo_home + "/pyzoo/zoo/common/nncontext.py"
    print("Checking: %s to see if build from source" % code_path)
    if os.path.exists(code_path):
        return True
    return False


def init_env():
    if build_from_source():
        print("Start to build distributed package")
        print("HOME OF ANALYTICS ZOO: " + analytics_zoo_home)
        dist_source = analytics_zoo_home + "/dist"
        if not os.path.exists(dist_source):
            print(building_error_msg)
            sys.exit(-1)
        if os.path.exists(TEMP_PATH):
            rmtree(TEMP_PATH)
        copytree(dist_source, TEMP_PATH)
        copyfile(
            analytics_zoo_home +
            "/pyzoo/zoo/models/__init__.py",
            TEMP_PATH +
            "/__init__.py")
    else:
        print("Do nothing for release installation")


def setup_package():
    script_names = os.listdir(SCRIPTS_TARGET)
    scripts = list(map(lambda script: os.path.join(
        SCRIPTS_TARGET, script), script_names))

    metadata = dict(
        name='analytics-zoo',
        version=VERSION,
        description='A unified Data Analytics and AI platform for distributed TensorFlow, Keras, '
                    'PyTorch, Apache Spark/Flink and Ray',
        long_description=long_description,
        long_description_content_type="text/markdown",
        author='Analytics Zoo Authors',
        author_email='bigdl-user-group@googlegroups.com',
        license='Apache License, Version 2.0',
        url='https://github.com/intel-analytics/analytics-zoo',
        packages=packages,
        install_requires=['pyspark==2.4.6', 'bigdl==0.13.0', 'conda-pack==0.3.1'],
        extras_require={'ray': ['ray==1.2.0', 'psutil', 'aiohttp==3.7.0', 'aioredis==1.1.0',
                                'setproctitle', 'hiredis==1.1.0', 'async-timeout==3.0.1'],
                        'automl': ['tensorflow>=1.15.0,<2.0.0', 'h5py==2.10.0', 'hiredis==1.1.0',
                                   'ray[tune]==1.2.0', 'psutil', 'aiohttp', 'setproctitle',
                                   'pandas', 'scikit-learn>=0.20.0,<=0.22.0', 'requests',
                                   'tsfresh', 'scipy==1.5', 'aioredis==1.3.1']},
        dependency_links=['https://d3kbcqa49mib13.cloudfront.net/spark-2.0.0-bin-hadoop2.7.tgz'],
        include_package_data=True,
        package_data={"zoo.share": ['lib/analytics-zoo*with-dependencies.jar', 'conf/*', 'bin/*',
                                    'bin/standalone/*', 'bin/standalone/sbin/*',
                                    'extra-resources/*']},
        scripts=scripts,
        classifiers=[
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: Implementation :: CPython'],
        platforms=['mac', 'linux']
    )

    setup(**metadata)


if __name__ == '__main__':
    try:
        init_env()
        setup_package()
    except Exception as e:
        raise e
    finally:
        if build_from_source() and os.path.exists(TEMP_PATH):
            rmtree(TEMP_PATH)
