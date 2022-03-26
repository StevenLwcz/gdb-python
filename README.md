# gdb-python
Using the Python API for GDB to produce commands and TUI windows, to improve debugging ARM assembler. See the wiki for more information.

These functions were written in order to learn about and explore the GDB Python API while learning ARM 32 and 64 bit assembler.

The latest addition is vector.py to display vector registers in a much more friendly way than GDB allows.

Armv8-app.py and aarch64pp.py which implement each a Tui general register window both contain a lot of duplicate code. Also the create_win() method is overly complex. General.py will be a simpler implementation and will work with armv8-a and aarch64. The idea is to give each register type its own class which will sort out the specific needs for the gdb.Value object and individual formatting needs.
