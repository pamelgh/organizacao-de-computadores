.data
	vetor: .word 3,2,80

.text
	
main:
	la a0, vetor  #end. inicial original
	la s0, vetor #salva o endereco inical para manipulacao
	add t6, zero, ra
	jal swap_vetor 
	
	nop
	ebreak

swap_vetor:

	lw  a1, 0(a0)	#lê indice 1
	addi s0, a0, 8 #anda 2 posicoes
	lw a2, (s0) #le indice 2
	add t3, zero, a1 #aux
	sw a2, 0(a0)
	sw a1, 0(s0)
	
	lw a2, (s0)	 #atualiza valores salvos
	lw a1, (a0)
	ret

