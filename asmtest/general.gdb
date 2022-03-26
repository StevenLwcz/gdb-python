set style enabled off
b _start
r
so ../general.py
tui new-layout debug1 register 1 src 1 status 0 cmd 1
layout debug1

register cpsr fpsr fpcr
# register hex on cpsr fpsr fpcr

register x0 x1 q2 q3 v1 v4 v5
