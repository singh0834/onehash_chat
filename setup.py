from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in onehash_chat/__init__.py
from onehash_chat import __version__ as version

setup(
	name="onehash_chat",
	version=version,
	description="Integration with OneHash Chat",
	author="Abhishek Chougule",
	author_email="abhishek.c@onehash.ai",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
