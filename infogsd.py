# add /fmt option for d on 32 and 64
# add /fmt option for s on 64

from platform import machine

GREEN = "\x1b[38;5;47m"
WHITE = "\x1b[38;5;15m"
RESET = "\x1b[0m"

#-------------
# register lists

r_list = {"r0": 0, "r1": 1, "r2": 2, "r3": 3, "r4": 4, "r5": 5, "r6": 6, "r7": 7, "r8": 8,
          "r9": 9, "r10": 10, "r11": 11, "r12": 12, 'sp': 13, 'lr': 14, 'pc': 15, 'cpsr': 16, 'fpscr': 17}

x_list = {"x0": 0, "x1": 1, "x2": 2, "x3": 3, "x4": 4, "x5": 5, "x6": 6, "x7": 7, "x8": 8,
          "x9": 9, "x10": 10, "x11": 11, "x12": 12, "x13": 13, "x14": 14, "x15": 15, "x16": 16,
          "x17": 17, "x18": 18, "x19": 19, "x20": 20, "x21": 21, "x22": 22, "x23": 23, "x24": 24,
          "x25": 25, "x26": 26, "x27": 27, "x28": 28, "x29": 29, "x30": 30, 'sp': 31, 'pc': 32, 'cpsr': 33, 'fpsr': 34, 'fpcr': 35}

s_list = {"s0": 0, "s1": 1, "s2": 2, "s3": 3, "s4": 4, "s5": 5, "s6": 6, "s7": 7, "s8": 8,
          "s9": 9, "s10": 10, "s11": 11, "s12": 12, "s13": 13, "s14": 14, "s15": 15, "s16": 16,
          "s17": 17, "s18": 18, "s19": 19, "s20": 20, "s21": 21, "s22": 22, "s23": 23, "s24": 24,
          "s25": 25, "s26": 26, "s27": 27, "s28": 28, "s29": 29, "s30": 30, "s31": 31}
 
d_list = {"d0": 0, "d1": 1, "d2": 2, "d3": 3, "d4": 4, "d5": 5, "d6": 6, "d7": 7, "d8": 8,
          "d9": 9, "d10": 10, "d11": 11, "d12": 12, "d13": 13, "d14": 14, "d15": 15, "d16": 16,
          "d17": 17, "d18": 18, "d19": 19, "d20": 20, "d21": 21, "d22": 22, "d23": 23, "d24": 24,
          "d25": 25, "d26": 26, "d27": 27, "d28": 28, "d29": 29, "d30": 30, "d31": 31}

v_list = {"v0": 0, "v1": 1, "v2": 2, "v3": 3, "v4": 4, "v5": 5, "v6": 6, "v7": 7, "v8": 8,
          "v9": 9, "v10": 10, "v11": 11, "v12": 12, "v13": 13, "v14": 14, "v15": 15, "v16": 16,
          "v17": 17, "v18": 18, "v19": 19, "v20": 20, "v21": 21, "v22": 22, "v23": 23, "v24": 24,
          "v25": 25, "v26": 26, "v27": 27, "v28": 28, "v29": 29, "v30": 30, "v31": 31}

q_list = {"q0": 0, "q1": 1, "q2": 2, "q3": 3, "q4": 4, "q5": 5, "q6": 6, "q7": 7, "q8": 8,
          "q9": 9, "q10": 10, "q11": 11, "q12": 12, "q13": 13, "q14": 14, "q15": 15}

#-----------
# GDB command classes

class InfoGSD(gdb.Command):

    def invoke(self, arguments, from_tty):
        argv = gdb.string_to_argv(arguments)
        
        list = []
        expand = False
        prev = None

        l = len(argv) 

        self.hex = False
        if l > 0 and argv[0] == '/x':
            self.hex = True
            del argv[0]
            l -= 1

        if l == 0:
            list = self.reglist
        else:
            for name in argv:
                if name == "-":
                    expand = True
                    continue
                elif not name in self.reglist:
                    print(f'info {self.cmd} {name} invalid register.')
                    return

                if expand:
                    if prev == None:
                        print(f'info {self.cmd} no start to range .')
                    start = self.reglist[prev]
                    finish = self.reglist[name]
                    list.extend([k for k, v in self.reglist.items() if v > start and v <= finish])
                    expand = False
                else:
                   prev = name
                   list.append(name)

        frame = gdb.selected_frame()
        for name in list:
            val = frame.read_register(name)
            print(f'{GREEN}{name:<10}{RESET}{self.format_reg(val):<24}')

    def format_reg(self, val):
        return val.format_string(format='x') if self.hex else val.format_string()

#---- general ----- 

class InfoGeneral64(InfoGSD):
    """info general [/x] [register-list] (x0 - x30 sp lr pc cpsr fpsr fpcr)
Use - to specify a range of registers.
info general x0 x4 - x9 pc cpsr
/x: display in hex"""

    cmd = "general"
    reglist = x_list

    def __init__(self):
       super().__init__("info general", gdb.COMMAND_DATA)

class InfoGeneral32(InfoGSD):
    """info general [register-list] (r0 - r12 sp lr pc cpsr fpscr)
Use - to specify a range of registers.
info general r0 r4 - r9 pc cpsr
/x: display in hex"""

    cmd = "general"
    reglist = r_list

    def __init__(self):
       super().__init__("info general", gdb.COMMAND_DATA)

#---- single ----- 

class InfoSingle64(InfoGSD):
    """info single [/x] [register-list] (s0 - s31)
Use - to specify a range of registers.
info double s0 s4 - s9
x: display in hex"""

    cmd = "single"
    reglist = s_list

    def __init__(self):
       super().__init__("info single", gdb.COMMAND_DATA)

    def format_reg(self, val):
        return val['u'].format_string(format='z') if self.hex else val['f'].format_string()

type_ptr_double = gdb.Value(0.0).type.pointer()

class InfoSingle32(InfoGSD):
    """info single [/x] [register-list] (s0 - s31)
Use - to specify a range of registers.
info double s0 s4 - s9
x: display in hex"""

    cmd = "single"
    reglist = s_list

    def __init__(self):
       super().__init__("info single", gdb.COMMAND_DATA)

    def format_reg(self, val):
        return val.cast(type_ptr_double).format_string(format="z") if self.hex else val.format_string()

#---- double ----- 

class InfoDouble64(InfoGSD):
    """info double [/x] [register-list] (d0 - d31)
Use - to specify a range of registers.
info double d0 d4 - d9
x: display in hex"""

    cmd = "double"
    reglist = d_list

    def __init__(self):
       super().__init__("info double", gdb.COMMAND_DATA)

    def format_reg(self, val):
        return val['u'].format_string(format='x') if self.hex else val['f'].format_string()

class InfoDouble32(InfoGSD):
    """info double [/x] [register-list] (d0 - d31)
Use - to specify a range of registers.
info double d0 d4 - d9
x: display in hex"""

    cmd = "double"
    reglist = d_list

    def __init__(self):
       super().__init__("info double", gdb.COMMAND_DATA)

    def format_reg(self, val):
        return val['u64'].format_string(format='x') if self.hex else val['f64'].format_string()

#---- vector ----- 

class InfoVector64(InfoGSD):
    """info vector /FMT [/x] [vector-register-list] (v0 - v31}
/FMT: {b, h, s, d, q}{f, s, u} [/x]
width - b: byte, h: 2 bytes, s: 4 bytes, d: 8 bytes, q: 16 bytes.
type  - f: float, s: signed, u: unsigned
Use - to specify a range of registers.
info vector /df v0 v2 - v4
x: display in hex"""

    cmd = "vector"
    reglist = v_list

    def __init__(self):
       super().__init__("info vector", gdb.COMMAND_DATA)

    def invoke(self, arguments, from_tty):
        l = len(arguments)
        if l > 2 and arguments[0:1] == "/":
            if arguments[1:2] in ['b', 'h', 's', 'd', 'q']:
                self.width = arguments[1:2]
                if arguments[2:3] in ['f', 's', 'u']:
                    self.type = arguments[2:3]
                    i = 4
                    super().invoke(arguments[i:], from_tty)
                else:
                    print(f'info vector /FMT: f,s,u expected: {arguments[2:3]}')
            else:
                print(f'info vector /FMT: b,h,s,d,q expected: {arguments[1:2]}')
        else:
            print("info vector /FMT register-list")

    def format_reg(self,  val):
        return val[self.width]['u'].format_string(format='z', repeat_threshold=0) if self.hex \
               else val[self.width][self.type].format_string(repeat_threshold=0)

    def format_reg_hex(self, val):
        return ""

class InfoVector32(InfoGSD):
    """info vector /FMT [/x] [vector-register-list] (q0 - q15}
/FMT: {u8, u16, u32, u64, f32, f64}
x   : display in hex
Use - to specify a range of registers.
info vector /u32 q0 q2 - q4"""

    cmd = "vector"
    reglist = q_list

    def __init__(self):
       super().__init__("info vector", gdb.COMMAND_DATA)

    def invoke(self, arguments, from_tty):
        l = len(arguments)
        
        if l > 2 and arguments[0:1] == "/":
            arguments += ' '
            i = arguments.index(' ')
            fmt = arguments[1:i]

            if fmt in ['u8', 'u16', 'u32', 'u64', 'f32', 'f64']:
                self.width = fmt
                super().invoke(arguments[i:], from_tty)
            else:
                print(f'info vector /FMT u8, u16, u32, u64, f32, f64 expected: {fmt}')
        else:
            print("info vector /FMT register-list")

    def format_reg(self,  val):
        if self.width == 'f32': hex = 'u32'
        elif self.width == 'f64': hex = 'u64'
        else: hex = self.width
        return val[hex].format_string(format='z', repeat_threshold=0) if self.hex \
               else val[self.width].format_string(repeat_threshold=0)

if machine() == "aarch64":
    InfoGeneral64()
    InfoSingle64()
    InfoDouble64()
    InfoVector64()
else:
    InfoGeneral32()
    InfoSingle32()
    InfoDouble32()
    InfoVector32()
