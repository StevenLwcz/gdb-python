.text

.globl _start
_start:

/* (gdb) info fpsr */
 
    ldr x0, =num1
    ldr  s1, [x0]
    fmov s0, 1
    fsub s0, s0, s0
    fdiv s2, s1,  s0   /* DCE set */
    bl sub1
    
    mrs x0, fpcr
    orr x0, x0, 0x200
    msr fpcr, x0
    /* fpcr still 0 - can't set DZE */

    fdiv s2, s1,  s0

end:
    mov     x0, #0      /* status */
    mov     x8, #93     /* exit is syscall 93 */
    svc     #0          

sub1: /* clear dzc */
    mrs x0, fpsr
    bic x0, x0, 0x2
    msr fpsr, x0
    ret

.data
.balign 16

num1: .single 100.00
