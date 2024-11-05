# Right now no use bzoc their is no requirement.txt to install any library or package in this project as I am use default env i.e conda "base". 


from setuptools import find_packages, setup
# # find_packages: find the number of packages file in the folder 
# # setup: provide me the information  
from typing import List

def get_requirements() -> List[str]:
    with open('requirement.txt', 'r') as f:
        requirements_list = [line.strip() for line in f]
    return requirements_list

setup(
    name='sensor',
    version='0.0.1',
    author='aarsh',
    author_email='aarshmehtani01@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements() #["pymongo"],
)
