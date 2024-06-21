from setuptools import setup, find_packages

setup(
    name='pymhw',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
    ],
    author='Andre Belem',
    author_email='andrebelem@id.uff.br',
    description='A package to calculate marine heatwaves',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/andrebelem/pymhw',  # 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
