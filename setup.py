from setuptools import setup, find_packages

setup(
    name = "qed-seal",
    version = "0.1",
    description = "QED watermarking tool",
    url = "https://github.com/qed-software/seal",
    author = "Paweł Wegner",
    author_email = "pa0@qed.ai",
    license = "MIT",
    classifiers = [
        "Programming Language :: Python :: 3"
    ],
    keywords = "watermark seal qed",
    install_requires = ["Pillow", "wheel"],
    packages = find_packages(),
    python_requires = ">=3",
    package_data = {
        "seal": ["watermark/*.png"]
    },
    entry_points = {
        "console_scripts": [
            "seal = seal.watermark:main"
        ]
    }
)
