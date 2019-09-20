.data
	vetor: .word 3,2,80,1

.text
	
main:
	la a0, vetor  #end. inicial original
	addi a1, zero, 4 #tam vetor
	la t3, vetor #0->0,1,2,3. 1-> 0, 1, 2,3...
	addi a4, zero, 0 #cont_out
	jal ordena
ordena:
	beq a4, a1, fimfim
	lw t4, 0(t3) #valor atual de fora
	 		
	
	addi t0, zero, 0 #cont_in
	lw t2, (a0) #1° valor do vetor
	addi s1, zero, 1 #aux verific.
	jal menor_vetor

	addi t3, t3, 4 #anda no vetor de fora
	addi a4, a4, 1 # percorre todo o vetor 4 vezes seguidas
	jal ordena
	nop
	ebreak
menor_vetor:
	#laço que percorre todos
	beq t0, a1, fim 
	#comparação p/ver qual é menor
	lw  t1, 0(a0)	#le valor apontado em cada iteração
	slt s0, t1, t2 #se o prox valor é menor que o atual menor, seta s0 com 1.
	beq s0, s1, muda #se for 1, ela atualiza o menor (t2).
#	beq s0, s1, swap_vetor #  troca ambos valores
	
	
	addi a0, a0, 4 #anda no vetor
	addi t0, t0, 1 #cont++
	j menor_vetor

muda: #atualização do menor e do indice
	add s3, t0, zero #indice a trocar
	add t2, zero, t1 #valor do novo menor
	ret

fim:
	
	nop
	
	
	
#swap_vetor:
	la s4, vetor #end incial
	add s4, a4, zero 
#    menor; t2 ja ta certo
	
	add s7, zero,t2   #s7 = menor
	sw t2, (s4) #maior = menor
	sw s7, (a0) #reg menor = s7
		
	lw s7,(s4)	 
	lw t2, (a0)
	ret



 fimfim:
 	nop
