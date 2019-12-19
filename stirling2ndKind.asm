.data

msg_n: 		.string "Digite o valor de N: "
msg_k: 		.string "Digite o valor de K: "
msg_erro_um: 	.string "ERRO: N tem que ser maior ou igual a 1 "
msg_erro_dois:	.string "ERRO: K tem que ser menor ou igual a N "
msg_erro_tres:	.string "ERRO: K tem que ser maior ou igual a 1 "
resposta:	.string "Resposta: "

.text

main:
	addi s0, zero, 1					#registrador auxiliar para comparação com 1
	jal mensagem
	j verifica_n
	j fim

mensagem:							#chamada para inserir o valor de N
	la a0, msg_n 						#carrega endereço da mensagem N
	li a7,4  						#carrega em a7 o tipo de chamada do sistema (printString)
	ecall
	
	li a7,5 #readInt (5)
	ecall
	add a2, zero, a0 					#auxiliar que reutiliza a0
								#chamada para inserir o valor de K
	la a0, msg_k 						#carrega endereço da mensagem K
	li a7,4 
	ecall
	
	li a7,5 #readInt (5)
	ecall
	add a3, zero, a0
	
	ret
	
#O valor de N foi armazenado em a2 e o valor de K foi armazenado em a3
#a4 armazena um auxiliar para o valor de k

#Aqui ocorre a verificação dos valores para que as condições: N >= 1 e 1<= K <= N precisam ser satisfeita antes de chamar a função
verifica_n:		
	beq a2, s0, verifica_k_um				#verifica N = 1
	bge a2, s0, verifica_k					#verifica se N > 1
	la a0, msg_erro_um					#se não for, imprime o erro e volta para o início
	li a7, 4
	ecall
	j mensagem

verifica_k:
	bge zero, a3, k_zero					#verifica se K <= 0							
	bge a2, a3, carregamento				#verifica se N > K
	beq a2, a3, eh_um					#verifica se N = K
	la a0, msg_erro_dois					
	li a7, 4
	ecall
	j mensagem
	
verifica_k_um:							#verifica se K = 1
	beq a3, s0, eh_um					#
	la a0, msg_erro_dois
	li a7, 4
	ecall
	j mensagem

k_zero:
	la a0, msg_erro_tres					#imprime a mensagem de erro 3
	li a7, 4						#quando o valor de K é menor que 0
	ecall
	j mensagem

eh_um:								#se os valores forem 1 e 1 ou se N = K, 
	li   a7, 4						#o valor 1 é exibido como resposta
	la   a0, resposta
	ecall

	addi a0, zero, 1
	li   a7, 1
	ecall	
	j fim

#Aqui ocorre o carregamento dos valores auxiliares que serão atualizados no vetor para o cálculo do número de stirling
carregamento:
	addi s2, a2, 0						#auxiliar para N
	addi s3, a3, 0						#auxiliar para K
	addi s4, zero, 0					#armazena a resposta do cálculo
	jal ST_2
	
	li   a7, 4
	la   a0, resposta
	ecall
		
	addi a0, s4, 0
	li   a7, 1
	ecall
	
	j fim	

#Aqui ocorre o calculo recursivo de stirling				
ST_2:	
	beq s3, s0, retorna_um					#S(n,1) = 1
	beq s3, zero, retorna_zero				#S(n,0) = 0
	beq s3, s2, retorna_um					#S(n,n) = 1 

#Aqui, o valor de N, K e o endereço de retorno é salvo na pilha
#Esta parte resolve a primeira parte da equação k*(n-1,k)
	addi sp, sp, -4
	sw s2, 0(sp)						#N
	addi sp, sp, -4
	sw s3, 0(sp)						#K
	addi sp, sp, -4
	sw ra, 0(sp)						#Endereço para retorno na pilha
	
	addi s2, s2, -1						#N - 1 é subtraído até encontrar uma das condições de parada
	jal ST_2						#chama a função novamente
		
	lw s2, 8(sp)						#carrega o valor anterior de N na auxiliar
	lw s3, 4(sp)						#carrega o valoe de K na auxiliar
	lw ra, 0(sp)						#carrega o endereço de retorno																																				
	
	mul s4, s3, s4						#Multiplica K pela resposta salva em s4
	
	addi sp, sp, -4
	sw s4, 0(sp)						#Salva a resposta na pilha

#Segunda parte da equação
	addi s2, s2, -1						#N-1	
	addi s3, s3, -1						#K-1
	
	jal ST_2						#chama a função novamente para verificar as condições anteriores
	
	lw a0, 0(sp)						#carrega a resposta em a0																																				
	lw ra, 4(sp)						#carrega o registrador do retorno
	lw s3, 8(sp)						#Le o auxiliar K
	lw s2, 12(sp)						#Le o auxiliar N
	add s4, a0, s4						#Soma retorno multiplicado com o retorno da outra parte
	addi sp, sp, 16
	ret					
		
retorna_zero:
	addi s4, zero, 0
	ret							#retorna 0, para qualquer que seja o valor de N, quando K = 0)
		
retorna_um:		
	addi s4, zero, 1
	ret							#Retorna 1
	
fim:
	ebreak
	nop
