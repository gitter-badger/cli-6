# SPARKL CLI

[![Join the chat at https://gitter.im/sparkl/cli](https://badges.gitter.im/sparkl/cli.svg)](https://gitter.im/sparkl/cli?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
Console CLI interface for managing running SPARKL nodes.
## Build
Use `make` as follows:
1. `make deps` to set up dependencies.
2. `make rel` to create distribution in `dist` directory.
3. From the dist directory, `sudo -H pip install xxx.gz` to install.
## Run
Use `sparkl -h` to see help as follows:
```
usage: sparkl [-h] [-v] [-a ALIAS] [-s SESSION]
              {connect,close,session,login,logout,ls,get,put,rm,show,mkdir,undo,vars,call,listen}
              ...

SPARKL command line utility.

positional arguments:
  {connect,close,session,login,logout,ls,get,put,rm,show,mkdir,undo,vars,call,listen}
    connect             Create or show connections
    close               Close connection
    session             Show all session info
    login               Login user or show current login
    logout              Logout user
    ls                  List content of folder or service
    get                 Download XML or JSON source
    put                 Upload XML source or change file
    rm                  Remove object
    show                Show object
    mkdir               Create new folder
    undo                Undo last change
    vars                Set field variables
    call                Invoke transaction or operation
    listen              Listen on a provision='rest' service

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -a ALIAS, --alias ALIAS
                        optional alias for multiple connections
  -s SESSION, --session SESSION
                        optional session id, defaults to invoking pid

Use 'sparkl <cmd> -h' for subcommand help
```
