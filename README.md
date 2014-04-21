python-appassure
================

A Python wrapper for the [AppAssure 5](http://www.appassure.com/) [REST
API](http://docs.appassure.com/display/AA50D/AppAssure+5+API+Reference).

## Installation

    git clone https://github.com/george2/python-appassure.git
    cd python-appassure
    python setup.py install

## Usage

Here's a simple example using the
[ILocalMountManagement](http://docs.appassure.com/display/AA50D/ILocalMountManagement)
Core interface.

```python
# Import the interface(s) you want to work with, and the session
# manager.
from appassure.core.ILocalMountManagement import ILocalMountManagement
from appassure.session import AppAssureSession

# Set up a session. The same session can be used for multiple
# interfaces.
session = AppAssureSession('myappassure5coreserver', 8006, 'Username',
        'password')

# Pass the session to the interface(s) on creation.
mounts = ILocalMountManagement(session)

# Call methods from the interface. Response data can be accessed
# with object or dictionary syntax.
mounts.getMounts().mountInfo
mounts.getMounts()['mountInfo']
```

## Implementing New Interfaces
AppAssure has quite a few of what it calls
[interfaces](http://docs.appassure.com/display/AA50D/Core+API+Reference)
available, and I have not yet implemented all of them. If you want
to add an interface that is not already implemented, it is fairly simple
to do so. In the [tools](tools) folder, there is a bash
script that will pull from the AppAssure documentation and automate most
of the implementation process. You will, however, still need to enter
the wrapper XML tag for the XML request body, if that exists.

![xml tag](http://i.imgur.com/HNsxslV.png)

If there is no XML request body for a method, just press enter. You will
not be prompted for request bodies for methods that use the `GET` or
`DELETE` HTTP verbs.

If you wish to implement an interface manually, that is also possible.
Just take a look at some of the existing interfaces to get an idea of
how to do so.
