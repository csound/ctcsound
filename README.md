## ctcsound
Python bindings for Csound using ctypes. Can be used from python2.x and python3.x as well.  

The *ctcsound.py* file is in the [Csound sources repository](https://github.com/csound/csound/blob/develop/interfaces/ctcsound.py).
This means that each release of Csound has its own version of *ctcsound.py* tied with the API functions present in the version of the libcsound library generated for that release. You should always use the *ctcsound* module shipped with the release of Csound you're using to avoid binding errors with libcsound.

Copy the *ctcsound.py* file of your Csound release into the site-packages folder of your Python, or anywhere else it can be found. For example, if you use the anconda3 distribution on osx, copy the *ctcsound.py* in */Library/Frameworks/CsoundLib64.framework/Versions/6.0/Resources/Python/Current* to *anaconda3/lib/python3.X/site-packages*

A comprehensive documentation for *ctcsound* can be found [here](https://csound.com/docs/ctcsound/)

Dependency: numpy, Csound 6.07 or higher.
