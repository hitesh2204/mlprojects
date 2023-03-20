from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT='-e .'
## Function for finding requirnments.txt file.
def get_requirnments(file_path:str)->List[str]:
    '''   
    This function is used to return the requirnment.
    ''' 
    requirnments=[]
    with open(file_path) as file_obj:
        requirnments=file_obj.readlines()
        requirnments=[req.replace('\n','')for req in requirnments]

        if HYPEN_E_DOT in requirnments:
            requirnments.remove(HYPEN_E_DOT)
    return requirnments

setup(
    name='mlproject',
    version='0.0.1',
    author='Hitesh',
    author_email='hitesh.yerekar@gmail.com',
    packages=find_packages(),
    install_requires=get_requirnments('requirnments.txt')
)