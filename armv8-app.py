# This python file contains three sections:
# 1. A pretty printer for floating point registers
# 2. An event hook for register change by the user
# 3. Custom gdb commands info general/single/double to display the various register groups
# 4. info fpscr to decode some of the bits in the control register.
# 5. A Tui Window to display user selected registers using the regwin command

# gdb -x armv8-app.py <exe>
#
# Developed and tested with gdb 10.1.90.20210103-git on armv8-a
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

GREEN = "\x1b[38;5;47m"
BLUE = "\x1b[38;5;14m"
WHITE = "\x1b[38;5;15m"
RESET = "\x1b[0m"
NL = "\n\n"

class FloatRegPrinter(object):

    def __init__(self, val):
        self.val = val

    def to_string(self):
        return "%f" % self.val['f64']

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

reg_dict = {0:"r0", 1:"r1", 2:"r2", 3:"r3", 4:"r4", 5:"r5", 6:"r6", 7:"r7", 8:"r8", 9:"r9"
, 10:"r10", 11:"r11", 12:"r12", 13:"sp", 14:"lr", 15:"pc"
, 25:"cpsr", 58:"d0", 59:"d1"
, 60:"d2", 61:"d3", 62:"d4", 63:"d5", 64:"d6", 65:"d7", 66:"d8", 67:"d9", 68:"d10", 69:"d11"
, 70:"d12", 71:"d13", 72:"d14", 73:"d15", 74:"d16", 75:"d17", 76:"d18", 77:"d19", 78:"d20", 79:"d21"
, 80:"d22", 81:"d23", 82:"d24", 83:"d25", 84:"d26", 85:"d27", 86:"d28", 87:"d29", 88:"d30", 89:"d31"
, 90:"fpscr", 91:"s0", 92:"s1", 93:"s2", 94:"s3", 95:"s4", 96:"s5", 97:"s6", 98:"s7", 99:"s8"
, 100:"s9", 101:"s10", 102:"s11", 103:"s12", 104:"s13", 105:"s14", 106:"s15", 107:"s16", 108:"s17", 109:"s18"
, 110:"s19", 111:"s20", 112:"s21", 113:"s22", 114:"s23", 115:"s24", 116:"s25", 117:"s26", 118:"s27", 119:"s28"
, 120:"s29", 121:"s30", 122:"s31", 123:"q0", 124:"q1", 125:"q2", 126:"q3", 127:"q4", 128:"q5", 129:"q6"
, 130:"q7", 131:"q8", 132:"q9", 133:"q10", 134:"q11", 135:"q12", 136:"q13", 137:"q14", 138:"q15"}

# new dictionary with keys and values swapped
reg_name = {value: key for key, value in reg_dict.items()} 

def GetRegister(i):
   frame = gdb.selected_frame()
   name = reg_dict[i]
   reg = frame.read_register(name)
   return name, reg

def reg_changed(event):
    name = reg_dict[event.regnum]
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

# used to print floats in hex by casting the value to a pointer. We could use any pointer type really.
type_ptr_double = gdb.Value(0.0).type.pointer()

def DumpSingleFloatRegs(start, length):
    frame = gdb.selected_frame()
    for i in range(start,start + length):
        name = reg_dict[i]
        reg = frame.read_register(name)
        h = reg.cast(type_ptr_double).format_string(format="z")
        print(f'{GREEN}{name}{RESET}\t{h}\t{reg}')

def DumpDoubleFloatRegs(start, length):
    frame = gdb.selected_frame()
    for i in range(start,start + length):
        name = reg_dict[i]
        reg = frame.read_register(name)
        print(f'{GREEN}{name}{RESET}\t{reg["u64"].format_string(format="z")}\t{reg["f64"]}')

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
           name = reg_dict[i]
           reg = frame.read_register(name)
           print(f'{GREEN}{name}{RESET}\t{reg.format_string(format="x")}\t{reg}')

InfoGeneral()

# --------------------

RM_MASK = 0xc00000 # 23-22
RN_FLAG = 0x000000 # Round to nearest tie zero
RP_FLAG = 0x400000 # Round towards + infinity (ceil)
RM_FLAG = 0x800000 # Round towards - infinity (floor)
RZ_FLAG = 0xc00000 # Round towards zero (truncate)

DZE_FLAG = 0x200 # Divide by Zero Enabled

def decode_fpscr(reg):
     flags = ""
     n = (reg & N_FLAG) == N_FLAG
     z = (reg & Z_FLAG) == Z_FLAG
     c = (reg & C_FLAG) == C_FLAG
     v = (reg & V_FLAG) == V_FLAG
     if n: flags +="N "
     if z: flags +="Z "
     if c: flags +="C "
     if v: flags +="V"

     if z: str = "EQ"
     else: str = "NE"

     mode = RM_MASK & reg
     if mode == RN_FLAG: str += " RN"
     elif mode == RP_FLAG: str += "RP"
     elif mode == RM_FLAG: str += "RM"
     else: str += "RZ"

     if (reg & DZE_FLAG) == DZE_FLAG: str += " DZE"

     return flags, str


# cpsr flags
N_FLAG = 0x80000000  # Negative
Z_FLAG = 0x40000000  # Zero
C_FLAG = 0x20000000  # Carry
V_FLAG = 0x10000000  # Overflow

def decode_cpsr(reg, extra):
     flags = ""
     n = (reg & N_FLAG) == N_FLAG
     z = (reg & Z_FLAG) == Z_FLAG
     c = (reg & C_FLAG) == C_FLAG
     v = (reg & V_FLAG) == V_FLAG
     if n: flags +="N "
     if z: flags +="Z "
     if c: flags +="C "
     if v: flags +="V"

     if z: str = "EQ"
     else: str = "NE"

     # signed
     if (not z) and n == v: str += " GT"
     if n == v: str += " GE"
     if not n == v: str += " LT"
     if z or (not n == v): str += " LE"
  
     if extra:
         # unsigned
         str += " -"
         if c and not z: str += " HI"  # greater than (Higher)
         if c: str += " HS"            # greater than, equal to
         else: str += " LO"            # less than (Lower)
         if (not c) or z: str += " LS" # less than, equal to

         #
         str += " -"
         if n: str += " MI"
         else: str += " PL"
         if v: str += " VS"
         else: str += " VC"

     return flags, str

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

       name, reg = GetRegister(FPSCR_REGISTER)
       flags, str = decode_cpsr(reg, True)
       print(GREEN + name + RESET + "  " + flags + " - " + str)

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

       name, reg = GetRegister(FPSCR_REGISTER)
       flags, str = decode_fpscr(reg)
       print(GREEN + name + RESET + "  " + flags + " - " + str)

InfoFpscr()

# --------------------
# Custom Tui Reg Window
#

class RegWinCmd(gdb.Command):
    """Add registers to the custom TUI Window arm32
List of registers space separated. Ranges can be specified with -. For example:
  regwin r0  r10 - r12 s0 s4 - s6 d5 - d9
Special registers: lr, pc, sp, cpsr, fpcsr
Toggle display of registers with hex format
  regwin hex [on|off]"""

    def __init__(self):
       super(RegWinCmd, self).__init__("regwin", gdb.COMMAND_DATA)

    def set_win(self, win):
        self.win = win

    def invoke(self, arguments, from_tty):
        args = gdb.string_to_argv(arguments)
        reg_list = []
        prev = None
        expand = False
        if args[0] == "hex":
            if args[1] == "on":
                self.win.set_hex(True)
            else:
                self.win.set_hex(False)
            return
            
        for reg in args:
            if reg == "-":
                expand = True
                continue
            elif not reg in reg_name:
                print("winreg: invalid register %s" % reg)
                return

            if expand:
                if prev == None:
                    print("winreg: no start to range")
                    return
                start = reg_name[prev] 
                finish = reg_name[reg]
                reg_list.extend([v for k, v in reg_dict.items() if k > start and k <= finish])
                expand = False
            else: 
                prev = reg
                reg_list.append(reg)

        self.win.set_list(reg_list)

regWinCmd = RegWinCmd()

def RegWinFactory(tui):
    win = RegWindow(tui)
    gdb.events.before_prompt.connect(win.render)
    regWinCmd.set_win(win)
    return win

class RegWindow(object):

    reglist_save = []

    def __init__(self, tui):
        self.tui = tui
        tui.title = "Registers"
        self.reglist = RegWindow.reglist_save
        self.prev = {}
        self.hex = False

    def set_list(self, list):
        self.reglist = list

    def set_hex(self, hex):
        self.hex = hex

    def close(self):
        RegWindow.reglist_save = self.reglist
        gdb.events.before_prompt.disconnect(self.render)

    def render(self):
        self.tui.erase()
        frame = gdb.selected_frame()
        width = self.tui.width
        for name in self.reglist:
            reg = frame.read_register(name)
            if name in self.prev and self.prev[name] != reg:
                hint = BLUE
            else:
                hint = WHITE

            self.prev[name] = reg

            if self.hex:
                if reg.type.name == "uint32_t" or name == "lr":
                    self.tui.write(f'{GREEN}{name:<5}{hint}{reg.format_string(format="x"):<18} {reg.format_string():<24}{RESET}')
                elif name == "pc" or name == "sp":
                    self.tui.write(f'{GREEN}{name:<5}{hint}{reg.format_string():<43}{RESET}')
                elif name == "cpsr":
                    flags, cond = decode_cpsr(reg, False)
                    self.tui.write(GREEN + f'{GREEN}{name:<5}{hint}{reg.format_string(format="x"):<18} {flags:<24}{RESET}')
                elif name == "fpscr":
                    flags, st = decode_fpscr(reg)
                    self.tui.write(f'{GREEN}{name:<5}{hint}{reg.format_string(format="x"):<18} {flags:<24}{RESET}')
                elif reg.type.name == "neon_q":
                    r1 = reg["u64"][1].format_string(format="z")
                    r2 = reg["u64"][0].format_string(format="z")
                    self.tui.write(f'{GREEN}{name:<5}{hint}{r1:<18} {r2:<18}{RESET}         ') 
                elif reg.type.name == "float": # s
                    # get the raw value of the float by casting it to a pointer (double *) and then printing the pointer in hex
                    r1 = reg.cast(type_ptr_double).format_string(format="z")
                    self.tui.write(f'{GREEN}{name:<5}{hint}{r1:<18} {reg.format_string():<24}{RESET}') 
                else: # d
                    self.tui.write(f'{GREEN}{name:<5}{hint}{reg["u64"].format_string(format="z"):<18} {reg["f64"].format_string():<24}{RESET}') 
                width = width - 48
                if width < 48:
                    self.tui.write(NL)
                    width = self.tui.width
            else:
                if reg.type.name == "uint32_t" or name == "pc" or name == "sp":
                    self.tui.write(f'{GREEN}{name:<5}{hint}{reg.format_string():<24}{RESET}')
                elif name == "lr":
                    self.tui.write(f'{GREEN}{name:<5}{hint}{reg.format_string(format="x"):<24}{RESET}') 
                elif name == "cpsr":
                    flags, cond = decode_cpsr(reg, False)
                    self.tui.write(GREEN + f'{GREEN}{name:<5}{hint}{flags:<24}{RESET}')
                elif name == "fpscr":
                    flags, st = decode_fpscr(reg)
                    self.tui.write(f'{GREEN}{name:<5}{hint}{flags + st:<24}{RESET}')
                elif reg.type.name == "neon_q":
                    r1 = reg["u64"][1].format_string(format="z")
                    r2 = reg["u64"][0].format_string(format="z")
                    self.tui.write(f'{GREEN}{name:<5}{hint}{r1:<18} {r2:<18}{RESET}         ') 
                    width = width - 29
                elif reg.type.name == "float": # s
                    self.tui.write(f'{GREEN}{name:<5}{hint}{reg.format_string():<24}{RESET}') 
                else: # d
                    self.tui.write(f'{GREEN}{name:<5}{hint}{reg["f64"].format_string():<24}{RESET}') 
                width = width - 29
                if width < 29:
                    self.tui.write(NL)
                    width = self.tui.width

    def hscroll(self, num):
        pass

    def vscroll(self, num):
        pass

    def click(self, x, y, button):
        pass
 
gdb.register_window_type("arm32", RegWinFactory)
