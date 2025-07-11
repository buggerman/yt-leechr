"""
Setup script for YT Leechr
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="yt-leechr",
    version="0.6.0",
    author="buggerman",
    author_email="buggerman@users.noreply.github.com",
    description="A feature-rich, cross-platform GUI for yt-dlp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/buggerman/yt-leechr",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "yt-leechr=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)