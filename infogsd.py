from platform import machine

GREEN = "\x1b[38;5;47m"
WHITE = "\x1b[38;5;15m"
RESET = "\x1b[0m"

#-------------
# register lists

r_list = {"r0": 0, "r1": 1, "r2": 2, "r3": 3, "r4": 4, "r5": 5, "r6": 6, "r7": 7, "r8": 8,
          "r9": 9, "r10": 10, "r11": 11, "r12": 12}

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

#-----------
# GDB command classes

class InfoGSD(gdb.Command):

    def invoke(self, arguments, from_tty):
        argv = gdb.string_to_argv(arguments)
        
        list = []
        expand = False
        prev = None

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
        else:
            list = self.reglist

        frame = gdb.selected_frame()
        for name in list:
            val = frame.read_register(name)
            print(f'{GREEN}{name:<10}{RESET}{self.format_reg(val):<24} {self.format_reg_hex(val)}')

    def format_reg(self, val):
        return val.format_string()

    def format_reg_hex(self, val):
        return val.format_string(format='x')

#---- general ----- 

class InfoGeneral64(InfoGSD):
    """info general AArch64"""

    cmd = "general"
    reglist = x_list

    def __init__(self):
       super(InfoGeneral64, self).__init__("info general", gdb.COMMAND_DATA)

class InfoGeneral32(InfoGSD):
    """info general Armv8-a"""

    cmd = "general"
    reglist = r_list

    def __init__(self):
       super(InfoGeneral32, self).__init__("info single", gdb.COMMAND_DATA)

#---- single ----- 

class InfoSingle64(InfoGSD):
    """info single AArch64"""

    cmd = "single"
    reglist = s_list

    def __init__(self):
       super(InfoSingle64, self).__init__("info single", gdb.COMMAND_DATA)

    def format_reg(self, val):
        return val['f'].format_string()

    def format_reg_hex(self, val):
        return val['u'].format_string(format='z')

type_ptr_double = gdb.Value(0.0).type.pointer()

class InfoSingle32(InfoGSD):
    """info single Armv8-a"""

    cmd = "single"
    reglist = s_list

    def __init__(self):
       super(InfoSingle32, self).__init__("info single", gdb.COMMAND_DATA)


    def format_reg_hex(self, val):
        return val.cast(type_ptr_double).format_string(format="z")

#---- double ----- 

class InfoDouble64(InfoGSD):
    """info double AArch64"""

    cmd = "double"
    reglist = d_list

    def __init__(self):
       super(InfoDouble64, self).__init__("info double", gdb.COMMAND_DATA)

    def format_reg(self, val):
        return val['f'].format_string()

    def format_reg_hex(self, val):
        return val['u'].format_string(format='x')

class InfoDouble32(InfoGSD):
    """info double Armv8-a"""

    cmd = "double"
    reglist = d_list

    def __init__(self):
       super(InfoDouble32, self).__init__("info double", gdb.COMMAND_DATA)

    def format_reg(self, name, val):
        return val['f64'].format_string()

    def format_reg_hex(self, val):
        return val['u64'].format_string(format='x')

if machine() == "aarch64":
    InfoGeneral64()
    InfoSingle64()
    InfoDouble64()
else:
    InfoGeneral32()
    InfoSingle32()
    InfoDouble32()
