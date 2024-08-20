from setuptools import setup, find_packages

setup(
    name='CompareJsonCustom',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='Henrique Cardamone',
    author_email='henrique.cardamonetec@gmail.com',
    description='A package for comparing JSON objects with custom attributes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hcardamone/comparejsoncustom.git',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
