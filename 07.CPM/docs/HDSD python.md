1. chọn dòng hiện tại: Ctrl+L
2. comment/uncomment: Ctrl+/

Cài python 3.10

Python 3.11 is not yet released as of May 2023. However, you can install the latest available version of Python 3 on CentOS 7 by following these steps:

    First, make sure your system is up to date by running the following command as root:

    sql

yum update

Install the required dependencies for building Python by running the following command:

yum install gcc openssl-devel bzip2-devel libffi-devel

Download the source code of the latest Python 3 release from the official website:



cd /usr/src
wget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz

Extract the source code and navigate to the extracted directory:



tar xzf Python-3.9.7.tgz
cd Python-3.9.7

Configure the build process and enable optimizations:



./configure --enable-optimizations

Build and install Python:

go

make altinstall

Note that we used altinstall instead of install to avoid overwriting the default system version of Python.

Verify that Python 3.9 is installed by running the following command:

css

python3.9 --version

This should output the version number of Python 3.9.

You can also create a virtual environment with Python 3.9 to isolate your projects from the system Python by installing virtualenv and creating a new environment:



pip install virtualenv
virtualenv -p python3.9 myenv
source myenv/bin/activate
python --version

This should output the version number of Python 3.9, indicating that you are now using the virtual environment.