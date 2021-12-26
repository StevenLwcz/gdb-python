# This python file contains three sections:
# 1. A pretty printer for floating point registers
# 2. An event hook for register change by the user
# 3. Custom gdb commands info general/single/double to display the various register groups
# 4. info fpscr to decode some of the bits in the control register.

# gdb -x armv8-app.py <exe>
#
# potential use case of info general/single/double
# (gdb) define hook-stop
# > info double 10 3
# > end
#
# gdb will now display the 3 floating point registers after every n/s command.
#
# Developed and tested with gdb 8.2.1 on armv8-a
#
# --------------------

#
# Override the pretty printing of the floating point registers $dnn
# to make the tui reg float window less cluttered if you are only interested in
# floating point values.
#

# tui reg float

# (gdb) p $d1
# $2 = {f = 23.454499999999999}

# use the /r to get the original formatting back
# (gdb) p /r $d1
# $5 = {u8 = {14, 190, 48, 153, 42, 232, 36, 64}, u16 = {48654, 39216, 59434, 16420}, u32 = {2570108430, 1076160554}, u64 = 46220743872453504, f32 = {-9.13736798e-24, 2.57667017}, f64 = 10.45345}`

import gdb

class FloatRegPrinter(object):

    def __init__(self, val):
        self.val = val

    def to_string(self):
        return "%f" %self.val['f64']

    # def children(self):
    #     pass
 
    def display_hint(self):
        return None

import gdb.printing

# create a collection of regex
pp = gdb.printing.RegexpCollectionPrettyPrinter('AsmLibrary')

# add a type regex to the collection
pp.add_printer('double_float_registers', "^neon_d$", FloatRegPrinter)

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

# single registers start at 91
# double registers start at 58

regs = ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8"
, "r9", "r10", "r11", "r12", "sp", "lr", "pc", "''", "''", "''"
, "''", "''", "''", "''", "''", "''", "cpsr", "''", "''", "''"
, "''", "''", "''", "''", "''", "''", "''", "''", "''", "''"
, "''", "''", "''", "''", "''", "''", "''", "''", "''", "''"
, "''", "''", "''", "''", "''", "''", "''", "''", "''", "d0"
, "d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "d10"
, "d11", "d12", "d13", "d14", "d15", "d16", "d17", "d18", "d19", "d20"
, "d21", "d22", "d23", "d24", "d25", "d26", "d27", "d28", "d29", "d30"
, "d31", "fpscr", "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7"
, "s8", "s9", "s10", "s11", "s12", "s13", "s14", "s15", "s16", "s17"
, "s18", "s19", "s20", "s21", "s22", "s23", "s24", "s25", "s26", "s27"
, "s28", "s29", "s30", "s31", "q0", "q1", "q2", "q3", "q4", "q5"
, "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "q14", "q15"]

def GetRegister(i):
   frame = gdb.selected_frame()
   name = regs[i]
   reg = frame.read_register(name)
   return name, reg

def reg_changed(event):
    name = regs[event.regnum]
    print("%s" % event.frame.read_register(name))

gdb.events.register_changed.connect(reg_changed)

# --------------------

#
# info general/single/double
#

general_abi = {'type': 'general', 'MAX_REGISTERS': 16, 'ARGS_LENGTH': 4, 'CALLEE_SAVED_START': 5, 'CALLEE_SAVED_LENGTH': 7,
           'TEMPORARY_START': 12, 'TEMPORARY_LENGTH': 1, 'REG_START': 0}

single_abi = {'type': 'single', 'MAX_REGISTERS': 32, 'ARGS_LENGTH': 16, 'CALLEE_SAVED_START': 16, 'CALLEE_SAVED_LENGTH': 16,
           'TEMPORARY_START': 0, 'TEMPORARY_LENGTH': 0, 'REG_START': 91}

double_abi = {'type': 'double', 'MAX_REGISTERS': 16, 'ARGS_LENGTH': 8, 'CALLEE_SAVED_START': 8, 'CALLEE_SAVED_LENGTH': 8,
           'TEMPORARY_START': 16, 'TEMPORARY_LENGTH': 16, 'REG_START': 58}

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
def DumpSingleFloatRegs(start, length):
    frame = gdb.selected_frame()
    for i in range(start,start + length):
        name = regs[i]
        reg = frame.read_register(name)
        print(name + "\t" +  str(reg) + "\t" + float(reg).hex())

def DumpDoubleFloatRegs(start, length):
    frame = gdb.selected_frame()
    for i in range(start,start + length):
        name = regs[i]
        reg = frame.read_register(name)
        print(name + "\t" +  str(reg['f64']) + "\t" + hex(reg['u64']))

class InfoSingle(gdb.Command):
   """List the single precision floating point registers and values
info single  [[start [length]] | [args|callee|temp]]
        start: start register (0-31)
       length: number of registers:
         args: arguments 0-15
       callee: callee saved 16-31
    temporary: N/A
default: info single 0, 32"""

   def __init__(self):
       super(InfoSingle, self).__init__("info single", gdb.COMMAND_DATA)

   def invoke(self, arguments, from_tty):
       start, length = ParseInfoArgs(single_abi, arguments)
       if start == -1: # error
           return

       DumpSingleFloatRegs(start, length)

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

       DumpDoubleFloatRegs(start, length)

InfoDouble()

class InfoGeneral(gdb.Command):
   """List general registers and values
info general [[start [length]] | [args|callee|temp]] 
        start: start register (0-15)
       length: number of registers:
         args: arguments 0-3
       callee: callee saved 4-11 (Platform specific: 9, FP: 11)
    temporary: 12 (IP: 12)
           SP: 13
           LR: 14
           PC: 15
default: info general 0 15"""

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
           print(name + "\t" +  str(reg) + "\t" + hex(reg))

InfoGeneral()


# --------------------

def UnpackConditionCodes(reg):
    N_FLAG = 0x80000000  # Negative
    Z_FLAG = 0x40000000  # Zero
    C_FLAG = 0x20000000  # Carry
    V_FLAG = 0x10000000  # Overflow
    n = (reg & N_FLAG) == N_FLAG
    z = (reg & Z_FLAG) == Z_FLAG
    c = (reg & C_FLAG) == C_FLAG
    v = (reg & V_FLAG) == V_FLAG
    return n, z, c, v

# info cpsr armv8-a

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
       CPSR_REGISTER = 25

       str, reg = GetRegister(CPSR_REGISTER)
       str += ":"

       n, z, c, v = UnpackConditionCodes(reg)
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

# info fpscr  floating point status and control register

class InfoFpscr(gdb.Command):
   """Display the status of the floating point status and control register (fpcr) register
Shows status of condition flags (CNZV).
Shows the Rounding Mode. 
RN	Round to nearest (tie zero)
RP	Round towards plus infinity (ceil)
RM	Round towards minus infinity (floor)
RZ	Round towards zero (truncate)"""
      
   def __init__(self):
       super(InfoFpscr, self).__init__("info fpscr", gdb.COMMAND_DATA)

   def invoke(self, arguments, from_tty):
       FPSCR_REGISTER = 90

       RM_MASK = 0xc00000 # 23-22
       RN_FLAG = 0x000000 # Round to nearest tie zero
       RP_FLAG = 0x400000 # Round towards + infinity (ceil)
       RM_FLAG = 0x800000 # Round towards - infinity (floor)
       RZ_FLAG = 0xc00000 # Round towards zero (truncate)

       str, reg = GetRegister(FPSCR_REGISTER)
       str += ":"

       n, z, c, v = UnpackConditionCodes(reg)
       if n: str +=" N"
       if z: str +=" Z"
       if c: str +=" C"
       if v: str +=" V"

       mode = RM_MASK & reg
       if mode == RN_FLAG: str += " RN"
       elif mode == RP_FLAG: str += "RP"
       elif mode == RM_FLAG: str += "RM"
       else: str += "RZ"

       print(str)

InfoFpscr()

print("aarmv8-app.py loaded")
