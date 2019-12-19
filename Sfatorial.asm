

main:

addi a0, zero,4 #n fatorial
jal fatorial
ebreak


fatorial:
beq a0, zero, fim
addi sp, sp, -8
sw a0, 4(sp)
sw ra, 0(sp)
addi a0, a0, -1
jal fatorial
lw a0, 4(sp)
lw ra, 0(sp)
addi sp, sp, 8
j multiplica

multiplica:

#mul a1,a1,a0
add a4, zero, zero
add a5, zero, zero
j laco
laco:
beq a4, a0, fim_laco
add a5, a5, a1
addi a4, a4, 1
j laco
fim_laco:
add a1, a5, zero
ret

fim:
addi a1, zero, 1
ret
