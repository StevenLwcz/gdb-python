from platform import machine
#--------------------------
# Colours

GREEN = "\x1b[38;5;47m"
BLUE  = "\x1b[38;5;14m"
WHITE = "\x1b[38;5;15m"
GREY  = "\x1b[38;5;246m"
RESET = "\x1b[0m"
NL = "\n\n"

#--------------------------
# Register list

reg_aarch64 = {"x0": 0, "x1": 1, "x2": 2, "x3": 3, "x4": 4, "x5": 5, "x6": 6, "x7": 7, "x8": 8,
       "x9": 9, "x10": 10, "x11": 11, "x12": 12, "x13": 13, "x14": 14, "x15": 15, "x16": 16,
       "x17": 17, "x18": 18, "x19": 19, "x20": 20, "x21": 21, "x22": 22, "x23": 23, "x24": 24,
       "x25": 25, "x26": 26, "x27": 27, "x28": 28, "x29": 29, "x30": 30,
       "b0": 31, "b1": 32, "b2": 33, "b3": 34, "b4": 35, "b5": 36, "b6": 37, "b7": 38, "b8": 39,
       "b9": 40, "b10": 41, "b11": 42, "b12": 43, "b13": 44, "b14": 45, "b15": 46, "b16": 47,
       "b17": 48, "b18": 49, "b19": 50, "b20": 51, "b21": 52, "b22": 53, "b23": 54, "b24": 55,
       "b25": 56, "b26": 57, "b27": 58, "b28": 59, "b29": 60, "b30": 61, "b31": 62,
       "h0": 63, "h1": 64, "h2": 65, "h3": 66, "h4": 67, "h5": 68, "h6": 69, "h7": 70, "h8": 71,
       "h9": 72, "h10": 73, "h11": 74, "h12": 75, "h13": 76, "h14": 77, "h15": 78, "h16": 79,
       "h17": 80, "h18": 81, "h19": 82, "h20": 83, "h21": 84, "h22": 85, "h23": 86, "h24": 87,
       "h25": 88, "h26": 89, "h27": 90, "h28": 91, "h29": 92, "h30": 93, "h31": 94,
       "s0": 95, "s1": 96, "s2": 97, "s3": 98, "s4": 99, "s5": 100, "s6": 101, "s7": 102, "s8": 103,
       "s9": 104, "s10": 105, "s11": 106, "s12": 107, "s13": 108, "s14": 109, "s15": 110, "s16": 111,
       "s17": 112, "s18": 113, "s19": 114, "s20": 115, "s21": 116, "s22": 117, "s23": 118, "s24": 119,
       "s25": 120, "s26": 121, "s27": 122, "s28": 123, "s29": 124, "s30": 125, "s31": 126,
       "d0": 127, "d1": 128, "d2": 129, "d3": 130, "d4": 131, "d5": 132, "d6": 133, "d7": 134, "d8": 135,
       "d9": 136, "d10": 137, "d11": 138, "d12": 139, "d13": 140, "d14": 141, "d15": 142, "d16": 143,
       "d17": 144, "d18": 145, "d19": 146, "d20": 147, "d21": 148, "d22": 149, "d23": 150, "d24": 151,
       "d25": 152, "d26": 153, "d27": 154, "d28": 155, "d29": 156, "d30": 157, "d31": 158,
       "q0": 159, "q1": 160, "q2": 161, "q3": 162, "q4": 163, "q5": 164, "q6": 165, "q7": 166, "q8": 167,
       "q9": 168, "q10": 169, "q11": 170, "q12": 171, "q13": 172, "q14": 173, "q15": 174, "q16": 175,
       "q17": 176, "q18": 177, "q19": 178, "q20": 179, "q21": 180, "q22": 181, "q23": 182, "q24": 183,
       "q25": 184, "q26": 185, "q27": 186, "q28": 187, "q29": 188, "q30": 189, "q31": 190,
       "v0": 191, "v1": 192, "v2": 193, "v3": 194, "v4": 195, "v5": 196, "v6": 197, "v7": 198, "v8": 199,
       "v9": 200, "v10": 201, "v11": 202, "v12": 203, "v13": 204, "v14": 205, "v15": 206, "v16": 207,
       "v17": 208, "v18": 209, "v19": 210, "v20": 211, "v21": 212, "v22": 213, "v23": 214, "v24": 215,
       "v25": 216, "v26": 217, "v27": 218, "v28": 219, "v29": 220, "v30": 221, "v31": 222,
       "lr": 223, "pc": 224, "sp": 225, "cpsr": 226, "fpsr": 227, "fpcr": 228}

reg_armv8a = {"r0": 0, "r1": 1, "r2": 2, "r3": 3, "r4": 4, "r5": 5, "r6": 6, "r7": 7, "r8": 8,
       "r9": 9, "r10": 10, "r11": 11, "r12": 12,
       "s0": 13, "s1": 14, "s2": 15, "s3": 16, "s4": 17, "s5": 18, "s6": 19, "s7": 20, "s8": 21,
       "s9": 22, "s10": 23, "s11": 24, "s12": 25, "s13": 26, "s14": 27, "s15": 28, "s16": 29,
       "s17": 30, "s18": 31, "s19": 32, "s20": 33, "s21": 34, "s22": 35, "s23": 36, "s24": 37,
       "s25": 38, "s26": 39, "s27": 40, "s28": 41, "s29": 42, "s30": 43, "s31": 44,
       "d0": 45, "d1": 46, "d2": 47, "d3": 48, "d4": 49, "d5": 50, "d6": 51, "d7": 52, "d8": 53,
       "d9": 54, "d10": 55, "d11": 56, "d12": 57, "d13": 58, "d14": 59, "d15": 60, "d16": 61,
       "d17": 62, "d18": 63, "d19": 64, "d20": 65, "d21": 66, "d22": 67, "d23": 68, "d24": 69,
       "d25": 70, "d26": 71, "d27": 72, "d28": 73, "d29": 74, "d30": 75, "d31": 76,
       "q0": 77, "q1": 78, "q2": 79, "q3": 80, "q4": 81, "q5": 82, "q6": 83, "q7": 84, "q8": 85,
       "q9": 86, "q10": 87, "q11": 88, "q12": 89, "q13": 90, "q14": 91, "q15": 92,
       "lr": 93, "pc": 94, "sp": 95, "cpsr": 96, "fpscr": 97}

registers = reg_aarch64 if machine() == "aarch64" else reg_armv8a

#--------------------------
# class view of registers for formatting

class Register(object):

    frame = None

    def __init__(self, name):
        self.name = name
        self.val = None
        self.hex = False
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
        return self.val.format_string(format='x') if self.hex else self.val.format_string()

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

    def __str__(self):
        return self.val['u'].format_string(format="z") if self.hex else  self.val['f'].format_string()

class BReg(Register):

    def __str__(self):
        return self.val['u'].format_string(format="z") if self.hex else self.val['u'].format_string()

class QReg(Register):

    def __format__(self, format_spec):
        return self.colour + format(str(self), "<53")

    def __str__(self):
        return self.val['u'].format_string(format="z") if self.hex else self.val['u'].format_string()

    def is_vector(self):
        return True

class VReg(Register):

    def __format__(self, format_spec):
        return self.colour + format(str(self), "<53")

    def __str__(self):
        return self.val['q']['u'][0].format_string(format="z") if self.hex else self.val['q']['u'][0].format_string()

    def is_vector(self):
        return True

class LRReg(Register):
    pass

class PCReg(Register):
    pass

class SPReg(Register):
    pass

class FPCRReg(Register):

    def __str__(self):
        flags = decode_fpcr(self.val)
        return self.val.format_string(format='z') + " " + flags if self.hex else flags

class FPSRReg(Register):

    def __str__(self):
        flags = decode_fpsr(self.val)
        return self.val.format_string(format='z') + " " + flags if self.hex else flags

class CPSRReg(Register):

    def __str__(self):
        flags = decode_cpsr(self.val, False)[0]
        return self.val.format_string(format='z') + " " + flags  if self.hex else flags

# used to print floats in hex by casting the value to a pointer. We could use any pointer type really.
type_ptr_double = gdb.Value(0.0).type.pointer()

class SReg(Register):

    def __str__(self):
        return self.val.cast(type_ptr_double).format_string(format="z") if self.hex else self.val.format_string()

class DReg(Register):

    def __str__(self):
        return self.val['u64'].format_string(format="z") if self.hex else  self.val['f64'].format_string()

class Qav8Reg(Register):

    def __format__(self, format_spec):
        return self.colour + format(str(self), "<53")

    def __str__(self):
        return self.val["u64"][1].format_string(format="z") + " " + self.val["u64"][0].format_string(format="z")

    def is_vector(self):
        return True

class FPSCRReg(Register):

    def __str__(self):
        flags, st = decode_fpscr(self.val)
        return " " + self.val.format_string(format='z') + " " + flags if self.hex else " " + flags + st

if machine() == "aarch64":
    reg_class = {'x': XReg, 's': HSDReg, 'd': HSDReg, 'h': HSDReg, 'b': BReg, 'q': QReg, 'v': VReg}
    reg_special = {'lr': LRReg, 'pc': PCReg, 'sp': SPReg, 'cpsr': CPSRReg, 'fpsr': FPSRReg, 'fpcr': FPCRReg}
else:
    reg_class = {'r': XReg, 's': SReg, 'd': DReg, 'q': Qav8Reg}
    reg_special = {'lr': LRReg, 'pc': PCReg, 'sp': SPReg, 'cpsr': CPSRReg, 'fpscr': FPSCRReg}


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
register OPT register-list
Register-list space separated. Ranges can be specified with -. For example:
  register x0 x10 - x15 s0 s4 - s6 d5 - d9*
  register r0 r10 - r15 s0 s4 - s6 d5 - d9
Special registers: lr, pc, sp, cpsr, fpsr*, fpcr*, fpscr. *AArch64
OPT: del register-list
     hex {on|off} register-list
   clear - clear all registers from the window"""

    def __init__(self):
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
        hex = None

        args = gdb.string_to_argv(arguments)
        argc = len(args)
        if argc == 0:
            print("register register-list")
            return
        elif args[0] == "hex":
            if argc > 2:
                if args[1] == 'on':
                    hex = True
                elif args[1] == 'off':
                    hex = False
                else:
                    print("register hex [on|off] register-list")
                    return
            else:
                print("register hex [on|off] register-list")
                return
            del args[0]
            del args[0]
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
        elif hex is not None:
            self.win.hex_registers(reg_list, hex)
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

    def hex_registers(self, args, mode):
        for name in args:
            if not name in self.regs:
                self.add_registers([name])

            self.regs[name].hex = mode

    def clear_registers(self):
        self.regs.clear()

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

