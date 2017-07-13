## ctcsound cookbook  
Recipes for using the ctcsound Python interface to the Csound API. Each recipe  
is presented in a [Jupyter notebook](http://jupyter.org/).

The easiest way to get Jupyter working on Windows or OSX is to install
[Anaconda](https://www.continuum.io/downloads) with the latest  
Python 3.x version. Anaconda includes Python and a bunch of numerical computing  
modules like numpy, matplotlib, scipy, etc. Once Anaconda is installed on your  
system, you can add an environment for Python 2.7 with the following commands:

```
conda create -n py27 python=2 ipykernel anaconda  
source activate py27   # On Windows, remove the word 'source'  
python -m ipykernel install --user
```

You'll then have kernels for Python 2 and 3 in Jupyter.  

Linux users might prefer to install Jupyter using pip instead of Anaconda.
For example on Ubuntu 16.04 LTS, Python 2.7.12 and Python 3.5.2 are installed
by default. Python 2.7.12 is launched with the command ```python``` or with
the command ```python2```, while Python 3.5.2 is launched with the command
```python3```.  

One have to install pip for both versions of Python:

```
sudo apt-get install python-pip
sudo apt-get install python3-pip
```

Then upgrade pip:

```
sudo pip install --upgrade pip
sudo pip3 install --upgrade pip
```

Install Jupyter with the Python 3 kernel, and numpy and matplotlib for
both versions of Python:

```
sudo pip3 install jupyter
sudo pip install numpy
sudo pip install matplotlib
sudo pip2 install numpy
sudo pip2 install matplotlib
```

And finally install the Python 2 kernel for Jupyter:

```
sudo python -m pip install ipykernel
sudo python -m ipykernel install --user
```
