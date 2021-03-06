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

GREEN = "\x1b[38;5;47m"
BLUE = "\x1b[38;5;14m"
WHITE = "\x1b[38;5;15m"
RESET = "\x1b[0m"
NL = "\n\n"

class FloatRegPrinter(object):

    def __init__(self, val):
        self.val = val

# by retuning a float we can get the display of the register without the f = when using print $dn or $sn
# tui reg float improved slightly but the hex part does not work properly
    def to_string(self):
        return(self.val['f'])

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
 
# reg_dict list generated from reg.awk

reg_dict = {0:"x0", 1:"x1", 2:"x2", 3:"x3", 4:"x4", 5:"x5", 6:"x6", 7:"x7", 8:"x8", 9:"x9"
, 10:"x10", 11:"x11", 12:"x12", 13:"x13", 14:"x14", 15:"x15", 16:"x16", 17:"x17", 18:"x18", 19:"x19"
, 20:"x20", 21:"x21", 22:"x22", 23:"x23", 24:"x24", 25:"x25", 26:"x26", 27:"x27", 28:"x28", 29:"x29"
, 30:"x30", 31:"sp", 32:"pc", 33:"cpsr", 34:"v0", 35:"v1", 36:"v2", 37:"v3", 38:"v4", 39:"v5"
, 40:"v6", 41:"v7", 42:"v8", 43:"v9", 44:"v10", 45:"v11", 46:"v12", 47:"v13", 48:"v14", 49:"v15"
, 50:"v16", 51:"v17", 52:"v18", 53:"v19", 54:"v20", 55:"v21", 56:"v22", 57:"v23", 58:"v24", 59:"v25"
, 60:"v26", 61:"v27", 62:"v28", 63:"v29", 64:"v30", 65:"v31", 66:"fpsr", 67:"fpcr", 68:"q0", 69:"q1"
, 70:"q2", 71:"q3", 72:"q4", 73:"q5", 74:"q6", 75:"q7", 76:"q8", 77:"q9", 78:"q10", 79:"q11"
, 80:"q12", 81:"q13", 82:"q14", 83:"q15", 84:"q16", 85:"q17", 86:"q18", 87:"q19", 88:"q20", 89:"q21"
, 90:"q22", 91:"q23", 92:"q24", 93:"q25", 94:"q26", 95:"q27", 96:"q28", 97:"q29", 98:"q30", 99:"q31"
, 100:"d0", 101:"d1", 102:"d2", 103:"d3", 104:"d4", 105:"d5", 106:"d6", 107:"d7", 108:"d8", 109:"d9"
, 110:"d10", 111:"d11", 112:"d12", 113:"d13", 114:"d14", 115:"d15", 116:"d16", 117:"d17", 118:"d18", 119:"d19"
, 120:"d20", 121:"d21", 122:"d22", 123:"d23", 124:"d24", 125:"d25", 126:"d26", 127:"d27", 128:"d28", 129:"d29"
, 130:"d30", 131:"d31", 132:"s0", 133:"s1", 134:"s2", 135:"s3", 136:"s4", 137:"s5", 138:"s6", 139:"s7"
, 140:"s8", 141:"s9", 142:"s10", 143:"s11", 144:"s12", 145:"s13", 146:"s14", 147:"s15", 148:"s16", 149:"s17"
, 150:"s18", 151:"s19", 152:"s20", 153:"s21", 154:"s22", 155:"s23", 156:"s24", 157:"s25", 158:"s26", 159:"s27"
, 160:"s28", 161:"s29", 162:"s30", 163:"s31", 164:"h0", 165:"h1", 166:"h2", 167:"h3", 168:"h4", 169:"h5"
, 170:"h6", 171:"h7", 172:"h8", 173:"h9", 174:"h10", 175:"h11", 176:"h12", 177:"h13", 178:"h14", 179:"h15"
, 180:"h16", 181:"h17", 182:"h18", 183:"h19", 184:"h20", 185:"h21", 186:"h22", 187:"h23", 188:"h24", 189:"h25"
, 190:"h26", 191:"h27", 192:"h28", 193:"h29", 194:"h30", 195:"h31", 196:"b0", 197:"b1", 198:"b2", 199:"b3"
, 200:"b4", 201:"b5", 202:"b6", 203:"b7", 204:"b8", 205:"b9", 206:"b10", 207:"b11", 208:"b12", 209:"b13"
, 210:"b14", 211:"b15", 212:"b16", 213:"b17", 214:"b18", 215:"b19", 216:"b20", 217:"b21", 218:"b22", 219:"b23"
, 220:"b24", 221:"b25", 222:"b26", 223:"b27", 224:"b28", 225:"b29", 226:"b30", 227:"b31"}

# new dictionary with keys and values swapped
reg_name = {value: key for key, value in reg_dict.items()}


def reg_changed(event):
    name = reg_dict[event.regnum]
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
        name = reg_dict[i]
        reg = frame.read_register(name)
        print(f'{GREEN}{name:<5}{RESET}{reg["u"].format_string(format="z"):18}  {reg["f"]}') 

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
           name = reg_dict[i]
           reg = frame.read_register(name)
           print(f'{GREEN}{name:<5}{RESET}{reg.format_string(format="x"):<18}  {reg}') 

InfoGeneral()

# --------------------

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

# fpcr flags
RM_MASK = 0xc00000 # 23-22
RN_FLAG = 0x000000 # Round to nearest tie zero
RP_FLAG = 0x400000 # Round towards + infinity (ceil)
RM_FLAG = 0x800000 # Round towards - infinity (floor)
RZ_FLAG = 0xc00000 # Round towards zero (truncate)
       
DZE_FLAG = 0x200 # Divide by Zero Enabled

def decode_fpcr(reg):
    mode = RM_MASK & reg
    if mode == RN_FLAG:
       str = "RN"
    elif mode == RP_FLAG:
       str = "RP"
    elif mode == RM_FLAG:
       str = "RM"
    else:
        str = "RZ"

    if (reg & DZE_FLAG) == DZE_FLAG: str += " DZE"

    return str

# fpsr flags
Q_FLAG = 0x08000000  # QC  Saturation
D_FLAG = 0x00000002  # DZC Divide by zero

def decode_fpsr(reg):
    str = ""
    if (reg & Q_FLAG) == Q_FLAG: str += "QC "
    if (reg & D_FLAG) == D_FLAG: str += "DZC"

    return str

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

       frame = gdb.selected_frame()
       name = reg_dict[CPSR_REGISTER]
       reg = frame.read_register(name)
       flags, str = decode_cpsr(reg, True)
       print(GREEN + name + RESET + "  " + flags + " - " + str)

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

       frame = gdb.selected_frame()
       name = reg_dict[FPCR_REGISTER]
       reg = frame.read_register(name)

       print(GREEN + name + RESET + ": " + decode_fpcr(reg))

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

       frame = gdb.selected_frame()
       name = reg_dict[FPSR_REGISTER]
       reg = frame.read_register(name)
       print(GREEN + name + RESET + ": " + decode_fpsr(reg))

InfoFpsr()

# --------------------
# Custom Tui Reg Window
#

# TODO
# 1. regwin add/remove registers maybe  add/remove groups

class RegWinCmd(gdb.Command):
    """Add registers to the custom TUI Window arm64
List of registers space separated. Ranges can be specified with -. For example:
  regwin x0 x10 - x15 s0 s4 - s6 d5 - d9
Special registers: pc, sp, cpsr, fpsr, fpcr
Toggle display of registers with hex format
  regwin hex [on|off]
Add more registers to existing list
  regwin add x17  s5 - s9 d12 - d13"""

    def __init__(self):
       super(RegWinCmd, self).__init__("regwin", gdb.COMMAND_DATA)

    def set_win(self, win):
        self.win = win

    def invoke(self, arguments, from_tty):
        reg_list = []
        args = gdb.string_to_argv(arguments)
        prev = None
        expand = False
        add = False
        if args[0] == "hex":
            if args[1] == "on":
                self.win.set_hex(True)
            else:
                self.win.set_hex(False)
            return

        if args[0] == "add":
            add = True
            del args[0]
            
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

        if add:
            self.win.add_list(reg_list)
        else:
            self.win.set_list(reg_list)

regWinCmd = RegWinCmd()

def RegWinFactory(tui):
    win = RegWindow(tui)
    gdb.events.before_prompt.connect(win.create_reg)
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
        self.start = 0
        self.list = []

    def set_list(self, list):
        self.reglist = list

    def add_list(self, list):
        self.reglist.extend(list)

    def set_hex(self, hex):
        self.hex = hex

    def close(self):
        RegWindow.reglist_save = self.reglist
        gdb.events.before_prompt.disconnect(self.create_reg)

    def render(self):
        if not self.tui.is_valid():
            return

        self.tui.erase()

        for l in self.list[self.start:]:
            self.tui.write(l)

    def create_reg(self):
        self.list = []

        if not self.tui.is_valid():
            return
        
        try:
            frame = gdb.selected_frame()
        except gdb.error:
            self.start = 0
            self.title = "No Frame"
            self.list.append("No frame currently selected" + NL)
            self.render()
            return
        
        width = self.tui.width
        line = ""

        for name in self.reglist:
            reg = frame.read_register(name)
            hint = BLUE if name in self.prev and self.prev[name] != reg else WHITE

            self.prev[name] = reg

            if self.hex:
                if reg.type.name == "long":
                    hexstr = reg.format_string(format="x")
                    line += f'{GREEN}{name:<5}{hint}{hexstr:<18} {reg.format_string():<24}{RESET}'
                elif name == "pc" or name == "sp":
                    line += f'{GREEN}{name:<5}{hint}{reg.format_string():<43}{RESET}'
                elif name == "cpsr":
                    hexstr = reg.format_string(format="x")
                    flags, cond = decode_cpsr(reg, False)
                    line += f'{GREEN}{name:<5}{hint}{hexstr:<18} {flags:<24}{RESET}'
                elif name == "fpcr":
                    hexstr = reg.format_string(format="x")
                    st = decode_fpcr(reg)
                    line += f'{GREEN}{name:<5}{hint}{hexstr:<18} {st:<24}{RESET}'
                elif name == "fpsr":
                    hexstr = reg.format_string(format="x")
                    st = decode_fpsr(reg)
                    line += f'{GREEN}{name:<5}{hint}{hexstr:<18} {st:<24}{RESET}'
                elif reg.type.name == "__gdb_builtin_type_vnq":
                    st = reg["u"].format_string(format="z")
                    line += f'{GREEN}{name:<5}{hint}{st:<43}{RESET}'
                elif reg.type.name == "__gdb_builtin_type_vnb":
                    st = reg["u"].format_string(format="x")
                    line += f'{GREEN}{name:<5}{hint}{st:<18} {reg["s"].format_string():<24}{RESET}'
                elif reg.type.name == "aarch64v":
                    st = reg["q"]["u"][0].format_string(format="z")
                    line += f'{GREEN}{name:<5}{hint}{st:<34}{RESET}         '
                else: # s & d
                    st = reg["u"].format_string(format="x")
                    f = reg["f"].format_string()
                    line += f'{GREEN}{name:<5}{hint}{st:<18} {f:<24}{RESET}'
                width = width - 48
                if width < 48:
                    line += NL
                    self.list.append(line)
                    line = ""
                    width = self.tui.width
            else:
                if reg.type.name == "long" or name == "pc" or name == "sp":
                    line += f'{GREEN}{name:<5}{hint}{reg.format_string():<24}{RESET}'
                elif name == "cpsr":
                    flags, cond = decode_cpsr(reg, False)
                    line += f'{GREEN}{name:<5}{hint}{flags:<24}{RESET}'
                elif name == "fpcr":
                    st = decode_fpcr(reg)
                    line += f'{GREEN}{name:<5}{hint}{st:<24}{RESET}'
                elif name == "fpsr":
                    st = decode_fpsr(reg)
                    line += f'{GREEN}{name:<5}{hint}{st:<24}{RESET}'
                elif reg.type.name == "__gdb_builtin_type_vnq":
                    st = reg["u"].format_string(format="z")
                    line += f'{GREEN}{name:<5}{hint}{st:<53}{RESET}'
                    width = width - 29
                elif reg.type.name == "__gdb_builtin_type_vnb":
                    line += f'{GREEN}{name:<5}{hint}{reg["s"].format_string():<24}{RESET}'
                elif reg.type.name == "aarch64v":
                    st = reg["q"]["u"][0].format_string(format="z")
                    line += f'{GREEN}{name:<5}{hint}{st:<53}{RESET}'
                    width = width - 29
                else:  # d or s
                    f = reg["f"].format_string()
                    line += f'{GREEN}{name:<5}{hint}{f:<24}{RESET}'
                width = width - 29
                if width < 29:
                    line += NL
                    self.list.append(line)
                    line = ""
                    width = self.tui.width

        if line != "":
            line += NL
            self.list.append(line)

        self.render()

    def hscroll(self, num):
        pass

    def click(self, x, y, button):
        pass

    def vscroll(self, num):
        if num > 0 and num + self.start < len(self.list) or \
           num < 0 and num + self.start >= 0:
            self.start += num
            self.render()

gdb.register_window_type("arm64", RegWinFactory)
