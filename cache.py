'''
        UNIVERSIDADE FEDERAL DA FRONTEIRA SUL
            ORGANIZAÇÃO DE COMPUTADORES
            Profº.: Luciano L. Caimi
            Estudantes: Naomi F. Mello
                        Pamela Gheno
'''

import random
import pandas
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)                      #Ignora os 'warnings' referente a incompatibilidade de dados

#Estrutura para as estatísticas
statistic_dict = {  "Accesses"  : 0,
                    "Read"      : 0,
                    "Write"     : 0,
                    "Hit_Read"  : 0,
                    "Miss_Read" : 0,
                    "Hit_Write" : 0,
                    "Miss_Write": 0,

}
#Estrutura para Memória Cache
cache = {'LFU'    :[0, 0, 0, 0, 0, 0, 0, 0], 
         'Status' :['available', 'available', 'available', 'available',
                     'available', 'available', 'available', 'available'],
         'Tag'    :['0', '0', '0', '0', '0', '0', '0', '0'], 
         'Cell:01':['0', '0', '0', '0', '0', '0', '0', '0'],
         'Data:01':['0', '0', '0', '0', '0', '0', '0', '0'],
         'Cell:02':['0', '0', '0', '0', '0', '0', '0', '0'], 
         'Data:02':['0', '0', '0', '0', '0', '0', '0', '0'],
         'Cell:03':['0', '0', '0', '0', '0', '0', '0', '0'],
         'Data:03':['0', '0', '0', '0', '0', '0', '0', '0'], 
         'Cell:04':['0', '0', '0', '0', '0', '0', '0', '0'],
         'Data:04':['0', '0', '0', '0', '0', '0', '0', '0'],
        } 
#Estrutura para a Memória Principal
ram = { 'Block'   :[],
        'Cell:01' :[],
        'Data:01' :[],
        'Cell:02' :[],
        'Data:02' :[], 
        'Cell:03' :[],
        'Data:03' :[], 
        'Cell:04' :[],
        'Data:04' :[],
}

#Função que converte um valor em um número binário de 7 bits
def binary(count):                                                                  
    count=bin(count)                                                                #A função bin() converte para uma string binário com 'b' concatenado

    aux=count.split('b')                                                            #count.split encontra o 'b' para remover da string
    count=aux[1]                                                                    #O retorno de split() é um vetor, o valor binário fica na segunda posição do vetor

    while(len(count) < 7):                                                          #É feito o complemento dos bits 'faltantes' para se ter uma cadeia com 7 bits
        count='0'+count

    return count
#-------- END FUNCTION --------------

#Função que inicializa a estrutura da Memória Principal 
def start_ran(ram):
    count=0
    for i in range(0, 32):
        ram['Block'].append(i)                                                      #Inicializa a coluna de bloco pois será usada como índice

        ram['Cell:01'].append(binary(count))                                        #Adiciona o endereço binário em cada célula
        count+=1
        ram['Cell:02'].append(binary(count))
        count+=1
        ram['Cell:03'].append(binary(count))
        count+=1
        ram['Cell:04'].append(binary(count))
        count+=1

        ram['Data:01'].append(str(hex(random.randrange(500))))                      #Preenche as células com dados aleatórios em hexadecimal
        ram['Data:02'].append(str(hex(random.randrange(500))))
        ram['Data:03'].append(str(hex(random.randrange(500))))
        ram['Data:04'].append(str(hex(random.randrange(500))))

    df_ram = pandas.DataFrame(ram)                                                  #Cria um DataFrame para a MP
    df_ram = df_ram.set_index('Block')                                              #Seta a coluna de blocos como índice do DataFrame

    return df_ram
#-------- END FUNCTION --------------

#Função que apresenta dados estatísticos
def statistic():
    print("  STATISTICS")
    print("---------------\n")
    for i in statistic_dict:                                                        #Percorre o dicionário imprimindo seus valores absoluto e as chaves associadas
        print(i,":",abs(statistic_dict[i]))
   
    print("\n   PERCENT %")
    print("-----------------\n")

    if statistic_dict["Read"] == 0:
        print("Hit_Read: 0.0 %")
        print("Miss_Read: 0.0 %")
    else:
        print("Hit_Read:",   (statistic_dict["Hit_Read"]*100)/statistic_dict["Read"],"%")
        print("Miss_Read:",  (statistic_dict["Miss_Read"]*100)/statistic_dict["Read"],"%")
    
    if statistic_dict["Write"] == 0:
        print("Hit_Write: 0.0 %")
        print("Miss_Write: 0.0 %")
    else:
        print("Hit_Write:",  (statistic_dict["Hit_Write"]*100)/statistic_dict["Write"],"%")
        print("Miss_Write:", (statistic_dict["Miss_Write"]*100)/statistic_dict["Write"],"%")

    input()
    menu()
#-------- END FUNCTION --------------

#Função para leitura de dados na cache
def read(df_cache, df_ram):
    statistic_dict["Read"] += 1                                                     #Ao selecionar leitura atualiza o dicionário de estatísticas
    statistic_dict["Accesses"] += 1
    
    address = input("Type binary address... ")                                      #Entrada do endereço
    tag = address[0:5]                                                              #Como a entrada é uma string, é feita a separação dos primeiros 5 bits e atribuído a tag

    aux_cache = df_cache.loc[df_cache['Tag'] == tag]                                #Retorna para aux_cache a linha do DataFrame df_cache com a informação referente a tag se não encontrar retorna vazio

    if not aux_cache.empty:                                                         #Se o valor estiver no DataFrame da cache
        statistic_dict["Hit_Read"]  +=1                                             #Atualiza as estatísticas de leitura como acerto

        print("\nAddress FOUND in cache!\n")
        print("        INFO")
        print("--------------------\n")
        print("READ HIT")
        
        idx_block = idxBlock(df_ram, address)                                       #Recupera o índice do bloco em que está o endereço
        print("Block:          ", idx_block)
        
        aux_cache = df_cache.loc[df_cache['Tag'] == tag]                            #Retorna para aux_cache a linha do DataFrame df_cache com a informação referente a tag se não encontrar retorna vazio
        SearchIdxCache(df_cache, aux_cache, address)                                #Função que procura o índice da MC
        print("\n--------------------")
        input()
        menu()
     
    elif address in df_ram.values:                                                  #Verifica se o valor existe na MP, retorna um DataFrame indicando TRUE no endereço
        statistic_dict["Miss_Read"] += 1                                            #Atualiza as estatísticas de leitura como erro

        print("\nHouston, we've got a problem!")
        print("\nSearching for the address in MP. Wait...\n")
        
        print("        INFO")
        print("--------------------\n")
        print("READ MISS")
        getValueFromRan(df_ram, df_cache, address)                                  #Função que resgata o valor na MP e insere na MC
        print("\n--------------------")
        input()
        menu()
            
    else:  
        print("\nInvalid address! Try again!")                                      #Mensagem de erro quando o valor não é encontrado
        menu()
#-------- END FUNCTION --------------

#Função para escrita de dados na cache
def write(df_cache, df_ram):
    statistic_dict["Write"] += 1                                                    #Atualiza as estatísticas de escrita e acesso
    statistic_dict["Accesses"] += 1

    address = input("Type binary address... ")                                      #Entrada do endereço
    data    = input("Type data... ")                                                #Entrada do dado para substituição
    
    tag = address[0:5]                                                              #Separação dos primeiros 5 bits do endereço e atribuído a tag

    aux_cache = df_cache.loc[df_cache['Tag'] == tag]                                #Retorna para aux_cache a linha do DataFrame df_cache com a informação referente a tag se não encontrar retorna vazio

    if not aux_cache.empty:                                                         #Se o valor estiver no DataFrame da cache
        statistic_dict["Hit_Write"]  +=1                                            #Atualiza as estatísticas de escrita como acerto

        print("\nWriting data in cache, wait!\n")
        print("        INFO")
        print("--------------------\n")
        print("WRITE HIT")

        idx_block = idxBlock(df_ram, address)                                       #Recupera o índice do bloco em que está o endereço
        print("Block:          ", idx_block)

        SearchIdxCache(df_cache, aux_cache, address)                                #Função que procura o índice da MC
        aux_cache = df_cache.loc[df_cache['Tag'] == tag]                            #Retorna para aux_cache a linha do DataFrame df_cache com a informação referente a tag se não encontrar retorna vazio
        updateMemories(df_cache, df_ram, aux_cache, address, data)                  #Função que atualiza os valores das memórias após escrita

    elif address in df_ram.values:                                                  #Verifica se o valor existe na MP, retorna um DataFrame indicando TRUE no endereço
        statistic_dict["Miss_Write"] += 1                                           #Atualiza as estatísticas de escrita como erro

        print("\nLoading data into MC...")
        print("        INFO")
        print("--------------------\n")
        print("WRITE MISS")
        
        getValueFromRan(df_ram, df_cache, address)                                  #Função que resgata o valor da MP e passa para a MC
        aux_cache = df_cache.loc[df_cache['Tag'] == tag]                            #Retorna para aux_cache a linha do DataFrame df_cache com a informação referente a tag se não encontrar retorna vazio
        updateMemories(df_cache, df_ram, aux_cache, address, data)                  #Função que atualiza os valores das memórias após escrita
            
    else:  
        print("\nInvalid address! Try again!")
        menu()
#-------- END FUNCTION --------------

#Função que procura o índice da MC
def SearchIdxCache(df_cache, aux_cache, address):
    idx = aux_cache.index.astype(int)[0]                                            #Busca em aux_cache e retorna em idx o índice da linha do dataframe que se encontra o endereço

    cell_name = (aux_cache == address).idxmax(axis=1)[0]                            #Retorna para cell_name o nome da coluna em que se encontra o endereço
    cell_idx = df_cache.columns.get_loc(cell_name)                                  #Retorna para cell_idx o índice da coluna em que se encontra o endereço

    df_cache.loc[idx, 'LFU']    =1                                                 #Atualiza o contador da política de substituição
    df = aux_cache.iloc[idx, [cell_idx, cell_idx+1]]                                #Seleciona as colunas com o endereço e o dado a partir do índice da cache
    
    print(df.to_string())                                                           #Converte para String (por questões estéticas) e imprime o endereço e o dado na MP
    print("Cache line:     ", idx)

#-------- END FUNCTION --------------

#Função que resgata o valor da MP e passa para a MC
def getValueFromRan(df_ram, df_cache, address):
    tag = address[0:5]
    idx_block = idxBlock(df_ram, address)                                           #Recupera o índice do bloco em que está o endereço

    aux_ram = df_ram.loc[idx_block]                                                 #Retorna para aux_ram uma 'lista' com as informações do bloco do endereço
    
    cell_name = aux_ram[aux_ram == address].index[0]                                #Recupera e retorna o nome da coluna do endereço
    cell_idx = df_ram.columns.get_loc(cell_name)                                    #A partir do nome da coluna encontra o índice da coluna do endereço
    
    df = aux_ram.iloc[[cell_idx, cell_idx+1]]                                       #Busca o endereço pelo índice(idx_block) e as colunas com o endereço e o dado (cell_idx, cell_idx+1) e armazena em df
    
    print("Block:          ", idx_block)
    print(df.to_string())                                                           #Converte para String (por questões estéticas) e imprime o endereço e o dado na MP

    is_avaliable = df_cache.loc[df_cache['Status'] == 'available']                  #Para quando todas as linhas da cache estiverem cheias
    if is_avaliable.empty:                                                          #Verifica se não há colunas 'available' caso não houver, retorna um DataFrame vazio
        lfu = df_cache['LFU']                                                       #lfu recebe a coluna LFU para encontrar o menor valor
        idx = lfu.idxmin()                                                          #Função retorna o índice do menor valor da Série

        df_cache.loc[idx, 'LFU']    = 1                                            #Atualiza o contador da política de substituição
        df_cache.loc[idx, 'Tag']     = tag                                          #Adiciona o novo rótulo

        x=0
        while(x < 8):
            df_cache.iloc[idx, x+3] = df_ram.iloc[idx_block, x]                     #Atribui os dados da MP para a nova linha da MC
            x += 1

        print("Cache line:     ", idx)                                              #Imprime a linha da cache em que o dado se encontra
    else:
        row=0
        while(row < 8):
            if(df_cache.loc[row, 'Status'] == 'available'):                         #Para quando houver espaço na cache
                
                df_cache.loc[row, 'LFU']    = 1                                    #Atualiza o contador da política de substituição
                df_cache.loc[row, 'Status']  = 'occupied'                           #Atualiza o status para 'ocupado'
                df_cache.loc[row, 'Tag']     = tag                                  #Atualiza o rótulo

                x=0
                while(x < 8):
                    df_cache.iloc[row, x+3] = df_ram.iloc[idx_block, x]             #Atribui os dados da MP para a nova linha da MC
                    x += 1
                print("Cache line:     ", row)                                      #Imprime a linha da cache em que o dado se encontra
                break
            row+=1
#-------- END FUNCTION --------------

#Função que atualiza os valores das memórias após escrita
def updateMemories(df_cache, df_ram, aux_cache, address, data):
    idx_cache = aux_cache.index.astype(int)[0]                                      #Busca em aux_cache e retorna em idx o índice da linha do DataFrame que se encontra o endereço
   
    cell_name_cache = (aux_cache == address).idxmax(axis=1).iloc[0]                 #Retorna para cell_name o nome da coluna em que se encontra o endereço
    cell_idx_cache = df_cache.columns.get_loc(cell_name_cache)                      #Retorna para cell_idx_cache o índice da coluna em que se encontra o endereço

    df_cache.iloc[idx_cache,cell_idx_cache+1] = data                                #Com o índice da coluna e o índice da linha a função iloc localiza aone o valor novo deve ser inserido na MC
                                                                                    ### FUNÇÕES DA MEMÓRIA PRINCIPAL ###
    idx_block = idxBlock(df_ram, address)                                           #Recupera o índice do bloco em que está o endereço
    aux_ram = df_ram.loc[idx_block]                                                 #Retorna para aux_ram uma Série com o bloco do endereço
    
    cell_name = aux_ram[aux_ram == address].index[0]                                #Retorna o nome da coluna do endereço
    cell_idx = df_ram.columns.get_loc(cell_name)                                    #Retorna o índice da coluna do endereço
    
    df_ram.iloc[idx_block,cell_idx+1] = data                                        #Com o índice da coluna e o índice da linha a função iloc localiza aone o valor novo deve ser inserido na MP

    print("\nUpdated!\n")
    input()
    menu()
#-------- END FUNCTION --------------

#Apenas uma função para retornar o índice do bloco de memória
def idxBlock(df_ram, address):
    df_bool = df_ram.loc[:,:] == address                                            #Retorna para cell_name um DataFrame booleano indicando como TRUE o endereço
    idx_block = df_bool.where(df_bool == True).dropna(how='all').index[0]           #Recupera o índice do bloco em que está o endereço marcado como TRUE
    
    return idx_block
#-------- END FUNCTION --------------

#Função que imprime as memórias
def showMemories(df_cache, df_ram):                                                 
    print("\n                           MAIN MEMORY")
    print("__________________________________________________________________________\n")
    print(df_ram)  

    print("\n\n")                                                     
    print("                         CACHE MEMORY")
    print("__________________________________________________________________\n")
    print(df_cache[['LFU', 'Status', 'Tag','Cell:01', 'Cell:02', 'Cell:03', 'Cell:04']])
    print("\n")
#------- END FUNCTION --------------

#Menu com as opções para seleção
def menu():
    print("\nChoose an option:\n")
    print("1) Read Data from Memory")
    print("2) Write Data in Memory")
    print("3) Show Statistics")
    print("4) Print Memories")
    print("5) Exit")

    op = int(input("-> "))

    while(op < 1 or op > 5):
        print("Invalid! Try again!!\n")
        op = int(input("-> "))

    if op==1:
        read(df_cache, df_ram)                                                      #Função para leitura dos dados da MC e MP
    elif op==2:
        write(df_cache,df_ram)                                                      #Função para escrita dos dados na MC e na MP
    elif op==3:
        statistic()                                                                 #Função para estatísticas da cache
    elif op==4:
        showMemories(df_cache, df_ram)                                              #Função para exibir a MC e MP
        menu()
    elif op==5:
        print("Hasta la vista, baby!")
        exit()
#------- END FUNCTION --------------

df_cache = pandas.DataFrame(cache)                                                  #Cria um DataFrame para a MC
df_ram = start_ran(ram)                                                             #Retorna para df_ram o DataFrame criado e inicializado

showMemories(df_cache, df_ram)                                                      #Função que imprime as memórias
menu()                                                                              #Menu com as opções para seleção
