from setuptools import setup, find_packages

setup(
    name="livestream_cat_detector",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "ultralytics",
        "twilio"
    ],
    entry_points={
        'console_scripts': [
            'cat-detector=livestream_cat_detector.detector:main',
        ],
    },
    author="Scott Brooks",
    author_email="s.brooks.2@warwick.ac.uk",
    description="A tool that detects cats in a YouTube livestream and sends SMS alerts.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/scott-vision/livestream_cat_detector",  # update with your repo URL if applicable
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
