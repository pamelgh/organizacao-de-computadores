.data
	vetor: .word 3,2,80,10,-200

.text
	
main:
	addi a1, zero, 5 #tam vetor
	la a0, vetor  #le endereço inicial
	addi t0, zero, 0 #inicia contador
	lw t2, 0(a0) #var auxiliar. 1º posição vetor equivale ao menor valor encontrado
	addi s1, zero, 1 #aux verific.
	jal menor_vetor 
	
	nop
	ebreak

menor_vetor:
	#laço que percorre todos
	beq t0, a1, fim #se t0 chegar ao final do vetor, vai pro fim. a1 define tamanho.
	#comparação p/ver qual é menor
	lw  t1, 0(a0)	#lê informação contida em cada endereço de a0.
	slt s0, t1, t2 #se o prox valor é menor que o atual menor, seta s0 com 1.
	beq s0, s1, muda #se for 1, ela atualiza o menor (t2).
	addi a0, a0, 4 #anda posições na memória
	addi t0, t0, 1 #incrementa contador
	j menor_vetor

muda: #atualização do menor e do indice
	add s3, t0, zero #a1-1 indice
	add t2, zero, t1
	ret

fim:
	#atribui e retorna
	add a1, zero, t2
	add a0, zero, s3
	nop