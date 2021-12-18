.text

.globl _start
_start:

/* (gdb) define hook-stop
 * >info cpsr
 * >end
 */

    mov x0, 10
    mov x1, 10
    cmp x0, x1         // Z C - EQ - HS LS - GE LE - PL VC
    mov x1, 0
    cmp x0, x1         // C   - NE - HI HS - GT GE - PL VC
    mov x1, 20
    cmp x0, x1         // N   - NE - LO LS - LT LE - MI VC

    // trigger overflow V
    mov  x0, 0xffff
    movk x0, 0xffff, lsl 16
    movk x0, 0xffff, lsl 32
    movk x0, 0x7fff, lsl 48
    mov  x1, 1

    // sign bit gets changed (set)
    adds x2, x1, x0    // N V - NE - LO LS - GT GE - MI VS

    // clear flags
    adds x3, x1, 0     //     - NE - LO LS - GT GE - PL VC

    // sign bit gets changed (cleared)
    subs x2, x2, x1    // C V - NE - HI HS - LT LE - PL VS

end:
    mov     x0, #0      /* status */
    mov     x8, #93     /* exit is syscall 93 */
    svc     #0          

sub1:
    mov x10, 10
.data
