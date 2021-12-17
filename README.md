# gdb-python
Using the Python API for gdb to produce commands, etc to help improve debugging ARM assembler.
```
info single/double to list the float registers around a specific selection or by ABI classification.
pretty printer to filter only the floating point part of the unions used by gdb.
Event handler when a register is changed by a user. I'm not sure how useful this is but achieving it was
a step toward better understanding of the Python API and a precursor to the info commands
```
```
Future plans:
    info general along the same lines, with abi info
    info 'status-registers' will decode the various float status registers into a nicer format
    create new tui windows to give filtered view since tui reg float and tui reg vector display more info than you are interested in

```
    
