import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pai_api_clients",
    version="0.0.3",
    author="pivotai",
    author_email="",
    description="It's pip with git. Helps with many methods to manage and use google speech to text services",
    long_description=long_description,
    url="https://github.com/PivotAI/pai-api-clients.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Django==3.2.5',
        'librosa==0.8.1',
        'SoundFile==0.10.3.post1',
        'google-cloud-speech==2.6.0',
        'pydub==0.25.1',
        'azure-ai-formrecognizer==3.1.1',
        'azure-storage-blob==12.8.1',
        'azure-identity==1.5.0',
        'azure-keyvault-secrets==4.2.0'
    ]
)
