// regwin q2 q3 v1 v4 v5

.text

.globl _start

_start:
    ldr x0, =num1
    ldp q2, q3, [x0]

    ld1 { v4.4s, v5.4s }, [x0]
    fmul v1.4s, v4.4s, v5.4s

    ldr x0, =num2
    ldp q2, q3, [x0]
    add v1.4s, v2.4s, v3.4s
    

end:
    mov     x0, #0      /* status */
    mov     x8, #93     /* exit is syscall 93 */
    svc     #0          

    .data
    .align 2


.data

num1:
    .single 10
    .single 10
    .single 10
    .single 10
    .single 10
    .single 10
    .single 10
    .single 10
num2:
    .word 10
    .word 10
    .word 10
    .word 10
    .word 10
    .word 10
    .word 10
    .word 10
