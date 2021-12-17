# This python file contains three sections:
# 1. A pretty printer for floating point registers
# 2. An event hook for register change by the user
# 3. A custom gdb command info single and info double to display floating point registers
#
# gdb -x aarch64pp.py <exe>
#
# potential use case of info single/double
# (gdb) define hook-stop
# > info single 10 3
# > end
#
# gdb will now display the 3 floating point registers after every n/s command.
#
#
# These functions were written in order to learn about and explore the GDB Python API while learning about ARM assembler.
# Developed and tested with gdb 8.2.1 on aarch64
# armv8-a version coming soon.
#
# Future aim is to create custom tui windows for floating point registers
# since in aarch64 they are too verbose and not as compact as the armv8-a versions
#
# --------------------

#
# Override the pretty printing of the floating point registers $dnn and $snn
# to make the tui reg float window less cluttered if you are only interested in
# floating point values.
#

# tui reg float

# (gdb) p $d1
# $2 = {f = 23.454499999999999}
# (gdb) p $s1
# $6 = {f = 1.13841227e-21}

# use the /r to get the original formatting back
# (gdb) p /r $d1
# $4 = {f = 23.454499999999999, u = 4627295072523388977, s = 4627295072523388977}
# (gdb) p /r $s1
# $8 = {f = 1.13841227e-21, u = 481036337, s = 481036337}

import gdb

class FloatRegPrinter(object):

    def __init__(self, val):
        self.val = val

    def to_string(self):
        pass

# Use children method else the tui reg float window won't display the values in hex and float
# The view was better in armv8-a since Snn were float but now they are a builtin union

    def children(self):
        yield "f", self.val['f']
        # yield "s", self.val['s']
        # yield "u", self.val['u']
 
    def display_hint(self):
        return None

import gdb.printing

# create a collection of regex
pp = gdb.printing.RegexpCollectionPrettyPrinter('AsmLibrary')

# add a type regex to the collection
pp.add_printer('double_float_registers', "^__gdb_builtin_type_vnd$", FloatRegPrinter)
pp.add_printer('single_float_registers', "^__gdb_builtin_type_vns$", FloatRegPrinter)

# register the collection
gdb.printing.register_pretty_printer(gdb.current_objfile(), pp, replace=True)


# (gdb) info pretty-printer
# (gdb) g/D 

# --------------------

#
# Just for fun, register a function for the register_changed event
#
 
# (gdb) set $d1 = 12.34
# f = 12.34

# frame.read_regiger() needs the name of the register but only the number is avaliable
# from the frame from the event
 
# regs list generated from reg.awk

regs = ["x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9"
, "x10", "x11", "x12", "x13", "x14", "x15", "x16", "x17", "x18", "x19"
, "x20", "x21", "x22", "x23", "x24", "x25", "x26", "x27", "x28", "x29"
, "x30", "sp", "pc", "cpsr", "v0", "v1", "v2", "v3", "v4", "v5"
, "v6", "v7", "v8", "v9", "v10", "v11", "v12", "v13", "v14", "v15"
, "v16", "v17", "v18", "v19", "v20", "v21", "v22", "v23", "v24", "v25"
, "v26", "v27", "v28", "v29", "v30", "v31", "fpsr", "fpcr", "q0", "q1"
, "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11"
, "q12", "q13", "q14", "q15", "q16", "q17", "q18", "q19", "q20", "q21"
, "q22", "q23", "q24", "q25", "q26", "q27", "q28", "q29", "q30", "q31"
, "d0", "d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9"
, "d10", "d11", "d12", "d13", "d14", "d15", "d16", "d17", "d18", "d19"
, "d20", "d21", "d22", "d23", "d24", "d25", "d26", "d27", "d28", "d29"
, "d30", "d31", "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7"
, "s8", "s9", "s10", "s11", "s12", "s13", "s14", "s15", "s16", "s17"
, "s18", "s19", "s20", "s21", "s22", "s23", "s24", "s25", "s26", "s27"
, "s28", "s29", "s30", "s31", "h0", "h1", "h2", "h3", "h4", "h5"
, "h6", "h7", "h8", "h9", "h10", "h11", "h12", "h13", "h14", "h15"
, "h16", "h17", "h18", "h19", "h20", "h21", "h22", "h23", "h24", "h25"
, "h26", "h27", "h28", "h29", "h30", "h31", "b0", "b1", "b2", "b3"
, "b4", "b5", "b6", "b7", "b8", "b9", "b10", "b11", "b12", "b13"
, "b14", "b15", "b16", "b17", "b18", "b19", "b20", "b21", "b22", "b23"
, "b24", "b25", "b26", "b27", "b28", "b29", "b30", "b31"]

def reg_changed(event):
    name = regs[event.regnum]
    print("%s" % event.frame.read_register(name))

gdb.events.register_changed.connect(reg_changed)

# --------------------

#
# info single/double
#

single_abi = {'type': 'single', 'MAX_REGISTERS': 32, 'ARGS_LENGTH': 8, 'CALLEE_SAVED_START': 8, 'CALLEE_SAVED_LENGTH': 8,
           'TEMPORARY_START': 16, 'TEMPORARY_LENGTH': 16, 'FLOAT_START': 132}

double_abi = {'type': 'double', 'MAX_REGISTERS': 32, 'ARGS_LENGTH': 8, 'CALLEE_SAVED_START': 8, 'CALLEE_SAVED_LENGTH': 8,
           'TEMPORARY_START': 16, 'TEMPORARY_LENGTH': 16, 'FLOAT_START': 100}

# would be nice to have this function in a common source file with armv8-app.py but not found a conveniant way to do this yet

def ParseInfoArgs(abi, arguments):
    MAX_REGISTERS = abi['MAX_REGISTERS']
    ARGS_LENGTH = abi['ARGS_LENGTH']
    CALLEE_SAVED_START = abi['CALLEE_SAVED_START']
    CALLEE_SAVED_LENGTH = abi['CALLEE_SAVED_LENGTH']
    TEMPORARY_START = abi['TEMPORARY_START']
    TEMPORARY_LENGTH = abi['TEMPORARY_LENGTH']

    length = MAX_REGISTERS
    start = abi['FLOAT_START']
    type = abi['type']

    args = gdb.string_to_argv(arguments)
    argc = len(args)

    if argc == 0:
        return (start, length)

    if args[0].isdigit():
        i = int(args[0])
        if i > 32:
            print("info %s: start too large (max 32): %d" % (type, i))
            return (-1, 0)

        start += i

        if argc == 2:
            if args[1].isdigit():
                length = int(args[1]) 
                if i + length > MAX_REGISTERS:
                    print("info %s: length too large: %d" % (type, length))
                    return (-1, 0)
            else:
                print("info %s: length not an integer: %s" % (type, args[1]))
        else:
            length = MAX_REGISTERS - i
    else:
        if args[0] == "args":
            length = ARGS_LENGTH
        elif args[0] == "callee":
            start += CALLEE_SAVED_START
            length = CALLEE_SAVED_LENGTH
        elif args[0] == "temp":
            start += TEMPORARY_START
            length = TEMPORARY_LENGTH
        else:
            print("info %s: [args|callee|temp]]" % type)
            return (-1, 0)

    return (start, length)

def DumpFloatRegs(start, length):
    frame = gdb.selected_frame()
    for i in range(start,start + length):
        name = regs[i]
        reg = frame.read_register(name)
        print(name + "\t" +  str(reg['f']) + "\t" + hex(reg['u']))

class InfoSingle(gdb.Command):
   """List the single precision floating point registers and values
info single  [[start [length]] | [args|callee|temp]] 
        start: start register (0-31)
       length: number of registers:
         args: arguments 0-7
       callee: callee saved 8-15
    temporary: 16-31
default: info single 0, 32"""

   def __init__(self):
       super(InfoSingle, self).__init__("info single", gdb.COMMAND_DATA)

   def invoke(self, arguments, from_tty):
       start, length = ParseInfoArgs(single_abi, arguments)
       if start == -1: # error
           return

       DumpFloatRegs(start, length)

InfoSingle()

class InfoDouble(gdb.Command):
   """List double precision floating point registers and values
info double  [[start [length]] | [args|callee|temp]] 
        start: start register (0-31)
       length: number of registers:
         args: arguments 0-7
       callee: callee saved 8-15
    temporary: 16-31
default: info double 0, 32"""

   def __init__(self):
       super(InfoDouble, self).__init__("info double", gdb.COMMAND_DATA)

   def invoke(self, arguments, from_tty):
       start, length = ParseInfoArgs(double_abi, arguments)
       if start == -1: # error
           return

       DumpFloatRegs(start, length)

InfoDouble()

print("aarch64pp.py loaded")
