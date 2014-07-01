Rypace
======

Module of Parental Controll for Ryu Openflow Controller

What's Rypace
==========
Rypace is a component-based software defined networking framework, with parental control support and Openflow Controller Based Ryu.

All of the code is freely available under the Apache 2.0 license. Ryu
is fully written in Python.


Quick Start
===========
If you prefer to install Rypace from the source code::

```sh
$ git clone https://github.com/rafaelsilvag/Rypace.git
$ cd Rypace; export PYTHONPATH=. ; ryu-manager app/simple_switch_12 
```

Ryu Install::

```sh
$ sudo pip install ryu
```
Requirements to work Rypace::

```sh
$ sudo pip install -r requirements.txt
```
If you want to write your Ryu application, have a look at
`Writing ryu application <http://ryu.readthedocs.org/en/latest/writing_ryu_app.html>`_ document.
After writing your application, just type::

```sh
   $ cd /usr/local/rypace/
   $ export PYTHONPATH=.
   $ ryu-manager app/rypace_switch_v01.py
```
Developers:
	- Rafael S. Guimarães <rafaelg@ifes.edu.br>
	- Willen Borges Coelho <willen@ifes.edu.br>
	- Everson Scherrer Borges <everson@ifes.edu.br>