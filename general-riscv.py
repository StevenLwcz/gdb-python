from platform import machine
#--------------------------
# Colours

GREEN = "\x1b[38;5;47m"
BLUE  = "\x1b[38;5;14m"
WHITE = "\x1b[38;5;15m"
GREY  = "\x1b[38;5;246m"
RESET = "\x1b[0m"
NL = "\n"

#--------------------------
# Register list

reg_rv64 = {"x0": 0, "x1": 1, "x2": 2, "x3": 3, "x4": 4, "x5": 5, "x6": 6, "x7": 7, "x8": 8,
       "x9": 9, "x10": 10, "x11": 11, "x12": 12, "x13": 13, "x14": 14, "x15": 15, "x16": 16,
       "x17": 17, "x18": 18, "x19": 19, "x20": 20, "x21": 21, "x22": 22, "x23": 23, "x24": 24,
       "x25": 25, "x26": 26, "x27": 27, "x28": 28, "x29": 29, "x30": 30, "x31": 31, 
       "ra": 32, "sp": 33, "gp": 34, "tp": 35, "t0": 36, "t1": 37, "t2": 38, "t3": 39, "t4": 40,
       "t5": 41, "t6": 42, "fp": 43, "s0": 44, "s1": 45, "s2": 46, "s3": 47, "s4": 48, "s5": 49,
       "s6": 50, "s7": 51, "s8": 52, "s9": 53, "s10": 54, "s11": 55, 
       "a0": 56, "a1": 57, "a2": 58, "a3": 59, "a4": 60, "a5": 61, "a6": 62, "a7": 63,
       "pc": 255}

registers = reg_rv64

#--------------------------
# class view of registers for formatting

class Register(object):

    frame = None

    def __init__(self, name):
        self.name = name
        self.val = None
        self.fmt = 'd'
        self.colour = WHITE

    @classmethod
    def Factory(self, name):
        try:
            if name[1:2].isdigit():
                return reg_class[name[0:1]](name)
            else:
                return reg_special[name](name)
        except:
            raise BasicException("Invalid Register")

    def __format__(self, format_spec):
        return self.colour + format(str(self), format_spec)
         
    def __str__(self):
        return self.val.format_string(format=self.fmt)

    def value(self):
        val = Register.frame.read_register(self.name)
        self.colour = BLUE if self.val != val else WHITE
        self.val = val
        return self.val

    def is_vector(self):
        return False

class XReg(Register):
    pass

class HSDReg(Register):

    def __init__(self, name):
        super().__init__(name)
        self.fmt = 'f'

    def __str__(self):
        if self.fmt == 'd': 
            self.fmt = 's'
        if self.fmt in ['s', 'u', 'f']:
            return self.val[self.fmt].format_string()
        else:
            return self.val['u'].format_string(format='z')

class LRReg(Register):

    def __str__(self):
        return self.val.format_string()

class PCReg(Register):

    def __str__(self):
        return self.val.format_string()

class SPReg(Register):

    def __str__(self):
        return self.val.format_string()

# used to print floats in hex by casting the value to a pointer. We could use any pointer type really.
type_ptr_double = gdb.Value(0.0).type.pointer()

class SReg(Register):

    def __str__(self):
        hex = True if self.fmt == "z" or self.fmt == 'x' else False
        return self.val.cast(type_ptr_double).format_string(format="z") if hex else self.val.format_string()

class DReg(Register):

    def __init__(self, name):
        super().__init__(name)
        self.fmt = 'f'

    def __str__(self):
        return self.val['u64'].format_string(format=self.fmt)
        # return self.val['u64'].format_string(format="z") if self.hex else self.val['f64'].format_string()


reg_class = {'x': XReg, 'a': XReg, 't': XReg, 's': XReg}
reg_special = {'ra': LRReg, 'pc': PCReg, 'sp': SPReg}


#--------------------------
# decode system registers

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
   # if n == v: str += " GE"
   if not n == v: str += " LT"
   # if z or (not n == v): str += " LE"

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
#--------------------------
# Register command and Register Window

class RegisterCmd(gdb.Command):
    """Add registers to the custom TUI Window register.
register OPT|/FMT register-list
/FMT: x: hex, z: zero pad hex, s: signed, u: unsigned, f: float, c: char
OPT: del register-list
     clear - clear all registers from the window
     save filename - save register-list to file (use so filename to read back)
Ranges can be specified with -"""

    def __init__(self):
        if machine() == "aarch64":
            self.__doc__ += "\nregister x0 x10 - x15 s0 s4 - s6 d5 - d9 w0 w10 - w15\nSpecial registers: lr, pc, sp, cpsr, fpsr, fpcr"
        else:
            self.__doc__ += "\nregister r0 r10 - r15 s0 s4 - s6 d5 - d9\nSpecial registers: lr, pc, sp, cpsr, fpscr"
 
        super(RegisterCmd, self).__init__("register", gdb.COMMAND_DATA)
        self.win = None

    def set_win(self, win):
        self.win = win

    def invoke(self, arguments, from_tty):
        if self.win == None:
            print("register: Tui Window not active.")
            return
     
        reg_list = []
        prev = None
        expand = False
        delete = False
        format = None

        args = gdb.string_to_argv(arguments)
        argc = len(args)
        if argc == 0:
            print("register register-list")
            return
        elif args[0][0:1] == '/':
            if argc > 1:
                f = args[0][1:2]
                if f in ['x', 'z', 's', 'u', 'f', 'c', 'a']:
                    format = 'd' if f == 's' else f
                else:
                    print(f'register /FMT: x, z, s, u, f, c or a expected: {f}')
                    return
                del args[0]
            else:
                print(f'register /FMT register-list')
                return
        elif args[0] == "clear":
            self.win.clear_registers()
            return
        elif args[0] == "del":
            if argc > 1:
                delete = True
                del args[0]
            else:
                print("register del register-list")
                return
        elif args[0] == 'save':
            if argc == 2:
                self.win.save_registers(args[1])
                return
            else:
                print("register save filename")
                return
            
        for reg in args:
            if reg == "-":
                expand = True
                continue
            elif not reg in registers:
                print("register: invalid register %s" % reg)
                return

            if expand:
                if prev == None:
                    print("register: no start to range")
                    return
                start = registers[prev] 
                finish = registers[reg]
                reg_list.extend([k for k, v in registers.items() if v > start and v <= finish])
                expand = False
            else: 
                prev = reg
                reg_list.append(reg)

        if delete:
            self.win.del_registers(reg_list)
        elif format is not None:
            self.win.format_registers(reg_list, format)
        else:
            self.win.add_registers(reg_list)

regWinCmd = RegisterCmd()

def RegisterFactory(tui):
    win = RegisterWindow(tui)
    gdb.events.before_prompt.connect(win.create_register)
    regWinCmd.set_win(win)
    return win

class RegisterWindow(object):

    regs_save = {}

    def __init__(self, tui):
        self.tui = tui
        tui.title = "Registers"
        self.regs = RegisterWindow.regs_save
        self.start = 0
        self.tui_list = []

    def add_registers(self, list):
        for name in list:
            if not name in self.regs:
                try:
                    self.regs[name] = Register.Factory(name)
                except:
                    print(f'register: invalid register {name}.')
            
    def del_registers(self, list):
        for name in list:
            try:
                del self.regs[name]
            except:
               print(f'register del {name} not found')

    def format_registers(self, args, format):
        for name in args:
            if not name in self.regs:
                self.add_registers([name])

            self.regs[name].fmt = format

    def clear_registers(self):
        self.regs.clear()

    def save_registers(self, filename):
        try:
            with open(filename, "w") as f:
                for name in self.regs:
                    f.write(f'reg {name}\n')
                    print(f'reg {name}')
        except IOError:
            print(f'reg: could not write to {filename}')

    def close(self):
        RegisterWindow.regs_save = self.regs
        gdb.events.before_prompt.disconnect(self.create_register)

    def render(self):
        if not self.tui.is_valid():
            return

        self.tui.erase()

        for l in self.tui_list[self.start:]:
            self.tui.write(l)

    def create_register(self):
        self.tui_list = []

        if not self.tui.is_valid():
            return
        
        try:
            Register.frame = gdb.selected_frame()
        except gdb.error:
            self.start = 0
            self.title = "No Frame"
            self.tui_list.append("No frame currently selected" + NL)
            self.render()
            return
        
        width = self.tui.width
        line = ""

        for name, reg in self.regs.items():
            reg.value()

            if width < 53 and reg.is_vector() or width < 29 and not reg.is_vector():
                line += NL
                self.tui_list.append(line)
                line = ""
                width = self.tui.width

            line += f'{GREEN}{name:<5}{reg:<24}{RESET}'
            width -= 53 if reg.is_vector() else 29

        if line != "":
            line += NL
            self.tui_list.append(line)

        self.render()

    def vscroll(self, num):
        if num > 0 and num + self.start < len(self.tui_list) or \
           num < 0 and num + self.start >= 0:
            self.start += num
            self.render()

gdb.register_window_type("register", RegisterFactory)
