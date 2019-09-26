main:
	
	addi a0, zero, 0 #n fatorial
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

	mul a1,a1,a0
	ret
	
fim: 	
	addi a1, zero, 1
	ret
