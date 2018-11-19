.. _development_environment:

Development Environment
========================

Python Development environment for FDMS*

In this document we will describe the different tools, settings and strategy used for the development of FDMS transformation rules using Python 3.

Ths document is written based on the Anaconda Python distribution 5.3, Python versions 3.6 and/or 3.7, Pytest 3.8, PyCharm 2018.2.5 (Community Edition).

The different sections of the document are:

* Anaconda: Python Distribution.
* PyCharm: Integrated Development Environment (IDE).
* GitHub: Version Control.
* Pytest
* Python Debugger
* Python Debugging with Pytest


.. _anaconda:

Anaconda Installation
=====================================

This section will describe the installation and used components of Anaconda for the Python development in the FDMS project.

At the date the latest version of Python 3 available is Python 3.7.

https://www.anaconda.com/download/

.. image:: ../../img/anaconda1.JPG
.. image:: ../../img/anaconda2.JPG
.. image:: ../../img/anaconda3.JPG
.. image:: ../../img/anaconda4.JPG
.. image:: ../../img/anaconda5.JPG
.. image:: ../../img/anaconda6.JPG

Anaconda Prompt
----------------

.. image:: ../../img/anaconda7.JPG

By typing:  conda list in the (base) C:\> , it will be shown all the packages that have been installed with the Anaconda distribution.
In the appendix all the packages for the distribution of Anaconda 5.3 are listed.


.. _pycharm:

PyCharm: Integrated Development Environment (IDE)
=================================================

https://www.jetbrains.com/pycharm/download/#section=windows

The Pycharm version to download is the Community version.


.. image:: ../../img/pycharm1.JPG
.. image:: ../../img/pycharm2.JPG
.. image:: ../../img/pycharm3.JPG
.. image:: ../../img/pycharm4.JPG
.. image:: ../../img/pycharm5.JPG

Get the `anaconda` Prompt running in the PyCharm Terminal.
-----------------------------------------------------------

In PyCharm, File menu, Settings > Tools > Terminal, change the Shell path as following:

.. code-block:: console.

    cmd.exe "/K" "C:\python\anaconda\Scripts\activate.bat" "C:\python\anaconda"

Here we assume that the directory where `anaconda` is installed is C:\\python\\anaconda, otherwise replace accordingly.

.. image:: ../../img/pycharm6.JPG

Close the Terminal and reopen it, you will get the Anaconda Prompt.

.. image:: ../../img/pycharm7.JPG


.. _git:

GitHub: Version Control
=======================

At the heart of GitHub is an open source version control system (VCS) called Git. Git is responsible for everything GitHub-related that happens locally on your computer.
For Windows, in order to use Git on the command line, you'll need to download and  install, Git on your computer using this link:

https://git-scm.com/download/win

.. image:: ../../img/git1.JPG

Setting up GIT
--------------

.. image:: ../../img/git2.JPG
.. image:: ../../img/git3.JPG
.. image:: ../../img/git4.JPG
.. image:: ../../img/git5.JPG
.. image:: ../../img/git6.JPG
.. image:: ../../img/git7.JPG
.. image:: ../../img/git8.JPG
.. image:: ../../img/git9.JPG

Working with GitHub
--------------------

clone a GIT repository
#######################

.. image:: ../../img/git10.JPG
.. image:: ../../img/git11.JPG
.. image:: ../../img/git12.JPG
.. image:: ../../img/git13.JPG
