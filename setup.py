from setuptools import find_packages,setup
from typing import List


HYPHEN_E_DOT="-e ."
def get_requirements(file_path)->List[str]:
    '''This function is responsible for read all the libraries'''
    requirement=[]
    with open(file_path) as file_obj:
        requirement=file_obj.readlines()
        requirement=[req.replace('/n','') for req in requirement]
        if HYPHEN_E_DOT in requirement:
            requirement.remove(HYPHEN_E_DOT)

            return requirement
        

setup(
    name="Student-Academic Perfomrace",
    version="0.0.1",
    author="Sharmi anyum",
    author_email="anyumsharmila@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')    
)

        
