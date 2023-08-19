from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='tusur',
    version='0.1.1',
    author='Tarodictrl',
    author_email='vudi600@gmail.com',
    description='A project that allows you to work with tusur.ru via python',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Weebp-Team/tusur',
    packages=find_packages(),
    install_requires=['requests>=2.31.0', 'beautifulsoup4>=4.12.2'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='python python3.7 tusur',
    python_requires='>=3.7'
)
