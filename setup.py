from setuptools import setup, find_packages
import os

# Import version from version.py
# from vit_captioner.version import VERSION



# Use PyPI-specific README if available, otherwise use the standard README
readme_path = "README_PYPI.md" if os.path.exists("README_PYPI.md") else "README.md"

setup(
    name="vit-captioner",  # Use hyphen instead of underscore for PyPI
    version="0.1.2",  # Use explicit versioning - increment this for each release
    author="Lachlan Chen",
    author_email="lach@lazyingoronlyideas.art",
    description="A package for extracting keyframes from videos and generating captions using ViT-GPT2 model",
    long_description=open(readme_path).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lachlanchen/VideoCaptionerWithVit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.6",
    install_requires=[
        "opencv-python",
        "numpy",
        "torch",
        "transformers",
        "Pillow",
        "matplotlib",
        "tqdm",
        "Katna",
    ],
    entry_points={
        "console_scripts": [
            "vit-captioner=vit_captioner.cli:main",
        ],
    },
    include_package_data=True,
    keywords="video, captioning, ai, machine learning, ViT, GPT2, transformers",
    # project_urls={
    #     "Bug Reports": "https://github.com/user/vit-captioner/issues",
    #     "Source": "https://github.com/user/vit-captioner",
    # },
    project_urls={
        "Bug Reports": "https://github.com/lachlanchen/VideoCaptionerWithVit/issues",
        "Source": "https://github.com/lachlanchen/VideoCaptionerWithVit",
    },   
)