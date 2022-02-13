# This python file contains several sections:
# 1. A pretty printer for floating point registers
# 2. An event hook for register change by the user
# 3. Custom gdb commands info general/single/double to display the various registor groups
# 4. info fpsr and info fpcr to decode some of the bits in these registers. Work in progress
# 5. A Tui Window to display user selected registers using the regwin command
#
# gdb -x aarch64pp.py <exe>
#
# Developed and tested with gdb 10.1.90.20210103-git on aarch64
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

# by retuning a float we can get the display of the register without the f = 
    def to_string(self):
        return(float(self.val['f']))

# Use children method else the tui reg float window won't display the values in hex and float
# The view was better in armv8-a since Snn were float but now they are a builtin union
    # def children(self):
        # yield "f", float(self.val['f'])
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
# info general/single/double
#
# Potential use case of info general/single/double
# (gdb) define hook-stop
# > info single 10 3
# > end
#
# gdb will now display the 3 floating point registers after every n/s command.
#
# Also tui reg float is quite cluttered so the info commands should improve
# inspecting the floating point registers
#

general_abi = {'type': 'general', 'MAX_REGISTERS': 31, 'ARGS_LENGTH': 9, 'CALLEE_SAVED_START': 19, 'CALLEE_SAVED_LENGTH': 11,
           'TEMPORARY_START': 9, 'TEMPORARY_LENGTH': 10, 'REG_START': 0}

single_abi = {'type': 'single', 'MAX_REGISTERS': 32, 'ARGS_LENGTH': 8, 'CALLEE_SAVED_START': 8, 'CALLEE_SAVED_LENGTH': 8,
           'TEMPORARY_START': 16, 'TEMPORARY_LENGTH': 16, 'REG_START': 132}

double_abi = {'type': 'double', 'MAX_REGISTERS': 32, 'ARGS_LENGTH': 8, 'CALLEE_SAVED_START': 8, 'CALLEE_SAVED_LENGTH': 8,
           'TEMPORARY_START': 16, 'TEMPORARY_LENGTH': 16, 'REG_START': 100}

# would be nice to have this function in a common source file with armv8-app.py but not found a conveniant way to do this yet

def ParseInfoArgs(abi, arguments):
    MAX_REGISTERS = abi['MAX_REGISTERS']
    ARGS_LENGTH = abi['ARGS_LENGTH']
    CALLEE_SAVED_START = abi['CALLEE_SAVED_START']
    CALLEE_SAVED_LENGTH = abi['CALLEE_SAVED_LENGTH']
    TEMPORARY_START = abi['TEMPORARY_START']
    TEMPORARY_LENGTH = abi['TEMPORARY_LENGTH']

    length = MAX_REGISTERS
    start = abi['REG_START']
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
        print(name + "\t" + f'{int(reg["u"]):<#18x}' + "\t" + str(reg['f'])) 

class InfoSingle(gdb.Command):
   """List the single precision floating point registers and values
info single [[start [length]] | [args|callee|temp]] 
        start: start register (0-31)
       length: number of registers:
         args: arguments 0-7
       callee: callee saved 8-15
    temporary: 16-31
default: info single 0 32"""

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
info double [[start [length]] | [args|callee|temp]] 
        start: start register (0-31)
       length: number of registers:
         args: arguments 0-7
       callee: callee saved 8-15
    temporary: 16-31
default: info double 0 32"""

   def __init__(self):
       super(InfoDouble, self).__init__("info double", gdb.COMMAND_DATA)

   def invoke(self, arguments, from_tty):
       start, length = ParseInfoArgs(double_abi, arguments)
       if start == -1: # error
           return

       DumpFloatRegs(start, length)

InfoDouble()

class InfoGeneral(gdb.Command):
   """List general registers and values
info general [[start [length]] | [args|callee|temp]] 
        start: start register (0-30)
       length: number of registers:
         args: arguments 0-8 (XR: 8)
    temporary: 9-18 (IP0: 16, IP1: 17, Platform specific: 18)
       callee: callee saved 19-29 (FP: 29)
     link reg: 30
default: info general 0 31"""

   def __init__(self):
       super(InfoGeneral, self).__init__("info general", gdb.COMMAND_DATA)

   def invoke(self, arguments, from_tty):
       start, length = ParseInfoArgs(general_abi, arguments)
       if start == -1: # error
           return

       frame = gdb.selected_frame()
       for i in range(start,start + length):
           name = regs[i]
           reg = frame.read_register(name)
           print(name + "\t" + f'{int(reg):<#18x}' + "\t" + str(reg)) 

InfoGeneral()

# --------------------

# info cpsr

class InfoCpsr(gdb.Command):
   """Display the status of the pstate/cpsr register and condition codes
EQ	Equal to
NE	Not equal to
	Unsigned
HS	Greater than, equal to
HI	Greater than
LS	Less than, equal to
LO	Less than
	Signed
GE	Greater than, equal to (signed)
GT	Greater than (signed)
LE	Less than, equal to
LT	Less than
	Misc
MI	Minus
PL	Positive
VC	No overflow 
VS	overflow 
"""

   def __init__(self):
       super(InfoCpsr, self).__init__("info cpsr", gdb.COMMAND_DATA)

   def invoke(self, arguments, from_tty):
       CPSR_REGISTER = 33
       N_FLAG = 0x80000000  # Negative
       Z_FLAG = 0x40000000  # Zero
       C_FLAG = 0x20000000  # Carry
       V_FLAG = 0x10000000  # Overflow

       frame = gdb.selected_frame()
       name = regs[CPSR_REGISTER]
       reg = frame.read_register(name)
       n = (reg & N_FLAG) == N_FLAG
       z = (reg & Z_FLAG) == Z_FLAG
       c = (reg & C_FLAG) == C_FLAG
       v = (reg & V_FLAG) == V_FLAG
       str = name + ":"
       if n: str +=" N"
       if z: str +=" Z"
       if c: str +=" C"
       if v: str +=" V"

       str += " -"
       if z: str += " EQ"
       else: str += " NE"

       # unsigned
       str += " -"
       if c and not z: str += " HI"  # greater than (Higher)
       if c: str += " HS"            # greater than, equal to
       else: str += " LO"            # less than (Lower)
       if (not c) or z: str += " LS" # less than, equal to

       # signed
       str += " -"
       if (not z) and n == v: str += " GT"
       if n == v: str += " GE"
       if not n == v: str += " LT"
       if z or (not n == v): str += " LE"

       #
       str += " -"
       if n: str += " MI"
       else: str += " PL"
       if v: str += " VS"
       else: str += " VC"

       print(str)

InfoCpsr()

# info fpcr

class InfoFpcr(gdb.Command):
   """Display the status of the floating point control register (fpcr) register
RN	Round to nearest (tie zero)
RP	Round towards plus infinity (ceil)
RM	Round towards minus infinity (floor)
RZ	Round towards zero (truncate)
DZE	Divide by Zero Enabled """
      
   def __init__(self):
       super(InfoFpcr, self).__init__("info fpcr", gdb.COMMAND_DATA)

   def invoke(self, arguments, from_tty):
       FPCR_REGISTER = 67

       RM_MASK = 0xc00000 # 23-22
       RN_FLAG = 0x000000 # Round to nearest tie zero
       RP_FLAG = 0x400000 # Round towards + infinity (ceil)
       RM_FLAG = 0x800000 # Round towards - infinity (floor)
       RZ_FLAG = 0xc00000 # Round towards zero (truncate)
       
       DZE_FLAG = 0x200 # Divide by Zero Enabled

       frame = gdb.selected_frame()
       name = regs[FPCR_REGISTER]
       reg = frame.read_register(name)
       str = name + ": "

       mode = RM_MASK & reg
       if mode == RN_FLAG:
           str += "RN"
       elif mode == RP_FLAG:
           str += "RP"
       elif mode == RM_FLAG:
           str += "RM"
       else:
           str += "RZ"

       d = (reg & DZE_FLAG) == DZE_FLAG
       if d: str += " DZE"

       print(str)

InfoFpcr()

# fpsr

class InfoFpsr(gdb.Command):
   """Display the status of the floating point status register (fpsr) register
QC	Saturation
DZC	Divide by Zero """

   def __init__(self):
       super(InfoFpsr, self).__init__("info fpsr", gdb.COMMAND_DATA)

   def invoke(self, arguments, from_tty):
       FPSR_REGISTER = 66

       Q_FLAG = 0x08000000  # QC  Saturation
       D_FLAG = 0x00000002  # DZC Divide by zero

       frame = gdb.selected_frame()
       name = regs[FPSR_REGISTER]
       reg = frame.read_register(name)
       str = name + ":"

       q = (reg & Q_FLAG) == Q_FLAG
       if q: str += " QC"

       d = (reg & D_FLAG) == D_FLAG
       if d: str += " DZC"

       print(str)

InfoFpsr()

# --------------------
# Custom Tui Reg Window
#

# TODO
# 1. validate registers passed to regwin
# 2. highlight registers changed from previous render (make toggable perhaps)
# 3. allow mix of general and float registers 
# 4. lots more I'm sure

class RegWinCmd(gdb.Command):

    def __init__(self):
       super(RegWinCmd, self).__init__("regwin", gdb.COMMAND_DATA)

    def set_win(self, win):
        self.win = win

    def invoke(self, arguments, from_tty):
        args = gdb.string_to_argv(arguments)
        self.win.set_list(args) 

regWinCmd = RegWinCmd()

def RegWinFactory(tui):
    win = RegWindow(tui)
    gdb.events.before_prompt.connect(win.render)
    regWinCmd.set_win(win)
    return win


GREEN = "\x1b[38;5;47m"
# GREEN = "\x1b[32;1m"
RESET = "\x1b[0m"
NL = "\n\n"

class RegWindow(object):

    def __init__(self, tui):
        self.tui = tui
        tui.title = "Registers"
        self.count = 0
        self.reglist = ['d0', 's1']

    def set_list(self, list):
        self.reglist = list

    def close(self):
        pass

    def render(self):
        if self.tui.is_valid():
            self.tui.erase()
            frame = gdb.selected_frame()
            width = self.tui.width
            for name in self.reglist:
                reg = frame.read_register(name)
                self.tui.write(GREEN + f'{name:<5}' + RESET + f'{int(reg["u"]):<#18x}' + "  " + f'{float(reg["f"]):<20} ')
                width = width - 46
                if width < 46:
                    self.tui.write(NL)
                    width = self.tui.width

    def hscroll(self, num):
        pass

    def vscroll(self, num):
        pass

    def click(self, x, y, button):
        pass
 
gdb.register_window_type("rega64", RegWinFactory)


