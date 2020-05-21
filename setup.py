from setuptools import setup, find_packages

__version__ = "0.0"
exec(open("./dinoskynet/version.py").read())

with open('README.md') as f:
    _LONG_DESCRIPTION = f.read()

setup(
    name='dino-skynet',
    packages=find_packages(),
    version=__version__,
    license='gpl-3.0',
    description='A simple implementation of an autonomous agent which exploits OpenCV to play the famous dino game',
    long_description=_LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Roberto Bochet',
    author_email='robertobochet@gmail.com',
    url='https://github.com/RobertoBochet/dino-skynet',
    keywords=['game', 'dino', 'pygame', 'opencv', 'computer vision', 'autonomous agent'],
    install_requires=[
        'dino-game~=0.2',
        'opencv-python~=4.2.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.6'
)
