##ctcsound cookbook
Recipes for using the ctcsound Python interface to the Csound API. Each recipe  
is presented in a [Jupyter notebook](http://jupyter.org/).

The easiest way to get Jupyter working is to install [Anaconda](https://www.continuum.io/downloads) for the latest  
Python version. Once Anaconda is installed or your system, can add an environment  
for Python2.7 with the following commands:

>conda create -n ipykernel_py2 python=2 ipykernel  
>source activate ipykernel_py2    # On Windows, remove the word 'source'  
>python -m ipykernel install --user

You'll then have kernels for Python 2 and 3 in Jupyter.

Jupyter works well with Google Chrome. The command to launch Jupyter with  
Google Chrome is:  

>jupyter notebook --browser=google-chrome  
