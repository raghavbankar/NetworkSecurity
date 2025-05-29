"""
    Defines Configurations of project
    For packaging and distribution of python projects

"""

from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:

    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            #Read lines
            Lines= file.readlines()
            #process the lines
            for lines in Lines:
                requirements = lines.strip()
                if requirements and requirements!='-e .':
                    requirement_lst.append(requirements)
    except FileNotFoundError:
        print("File not found")
    return requirement_lst

setup(
    name="Network Security",
    version="0.0.0.1",
    author="Raghvendra",
    author_email="raghavbankar.2023@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)