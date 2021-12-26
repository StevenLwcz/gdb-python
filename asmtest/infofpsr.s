.text

.globl _start
_start:

/* (gdb) info fpsr */
 
    ldr w0, num1
    ldr w1, num2
    fmov s0, w0
    fmov s1, w1

    sqadd s2, s1, s0   /* QC not set */
    mrs x0, fpsr
    tst x0, 0x08000000
    beq l1
    bl sub1
l1:
    sqadd s2, s1, s2   /* QC set */
    mrs x0, fpsr
    tst x0, 0x08000000
    beq end
    bl sub1

end:
    mov     x0, #0      /* status */
    mov     x8, #93     /* exit is syscall 93 */
    svc     #0          

sub1:   /* reset QC */
    bic x0, x0, 0x8000000
    msr fpsr, x0
    ret

.data
.balign 16

num1: .word 0x7fffff00
num2: .word 0xff
