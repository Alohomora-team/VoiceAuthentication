import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="speaker_verification_tools",
    version="0.0.1",
    author="Victor Silva",
    author_email="victor.eng.unb@gmail.com",
    description="A package designed to compose speaker verification systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VictorJorgeFGA/speaker-verification-tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
