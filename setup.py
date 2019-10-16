# Copyright 2019 Twilio, Inc.
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
# limitations under the License

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
   long_description = fh.read()

setup(
   name="socless-sumologic",
   version="1.0.0",
   author="Saxon Hunt",
   long_description=long_description,
   long_description_content_type="text/markdown",
   packages=find_packages(),
   python_requires='>=3.7'
)