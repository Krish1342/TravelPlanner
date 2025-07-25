from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """
    This function will return list of requiremnents
    """
    requirement_list:List[str] = []
    
    try:
        #Open and read the requirements.txt file
        with open('requirements.txt', 'r') as file:
            #Read lines from the file
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found. Returning an empty list.")
    
    return requirement_list
print(get_requirements())

setup(
    name="AI_TRAVEL_PLANNER",
    version="0.0.1",
    author="Krish Lodha",
    authon_email="lodhakrish216@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
    description="A travel planner that uses AI to suggest itineraries based on user preferences.",
)