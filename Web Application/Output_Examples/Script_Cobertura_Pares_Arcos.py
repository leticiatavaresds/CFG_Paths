# Script Teste Cobertura de Pares de Arcos
pares_arcos = [(28, '2: enter', 3), ('2: enter', 3, 4), (3, 4, 5), (3, 4, 7), (5, 4, 5), (5, 4, 7), (4, 5, 4), (4, 7, 8), (7, 8, 9), (8, 9, 10), (9, 10, 12), (10, 12, 13), (12, 13, '2: exit'), (12, 13, 14), (14, 13, '2: exit'), (14, 13, 14), (13, 14, 13), (13, 14, 15), (24, 14, 13), (24, 14, 15), (17, 14, 13), (17, 14, 15), (14, 15, 16), (15, 16, 17), (16, 17, 14), (16, 17, 18), (17, 18, 19), (17, 18, 20), (18, 19, 20), (19, 20, 21), (18, 20, 21), (20, 21, 22), (20, 21, 24), (23, 21, 22), (23, 21, 24), (21, 22, 23), (22, 23, 21), (21, 24, 14), (21, 24, 25), (24, 25, '2: exit'), (27, 28, '2: enter')]
TR_arcos = set(sorted(pares_arcos, key=lambda x: int(str(x[0]).split(':')[0])))


def code_graph():
    nos = []
    def baralho3(entrada):
        nos.append('2: enter')
        nos.append(3)
        cartas = []
        nos.append(4)
        for i in range(0,len(entrada),3):
            nos.append(5)
            cartas = cartas + [entrada[i:i+3]]
            
            nos.append(4)
        nos.append(7)
        cartas.sort()
        nos.append(8)
        valores = ['01','02','03','04','05','06','08','09','10','11','12','13']
        nos.append(9)
        ordem = ['C','E','U', 'P']
        nos.append(10)
        faltam = [13, 13, 13, 13]
        nos.append(12)
        i = 0
        nos.append(13)
        for valor in valores:       
            nos.append(14)
            for j in [0,1,2,3]:
                nos.append(15)
                naipe = ordem[j]
                nos.append(16)
                carta = cartas[i]            
                nos.append(17)
                if carta == valor + naipe:
                    nos.append(18)
                    if faltam[j] != 'erro':
                        nos.append(19)
                        faltam[j] = faltam[j] - 1
                    nos.append(20)
                    i = i + 1
                    nos.append(21)
                    while i < len(cartas) and cartas[i] == carta:
                        nos.append(22)
                        faltam[j] = 'erro'
                        nos.append(23)
                        i = i + 1
                        nos.append(21)
                    nos.append(24)
                    if i == len(cartas):
                        nos.append(25)
                        nos.append('2: exit')
                        return faltam
                        
                nos.append(14)
            nos.append(13)
        nos.append('2: exit')
    nos.append(27)
    entrada = input()
    nos.append(28)
    baralho3(entrada)
    return nos

# Teste de arcos
pares_arcos_testes = set([])
n_teste = 1

print(f"\n\033[38;5;87mTR Cobertura de Pares de Arcos: \033[0;0m\n{TR_pares_arcos} \033[0;0m\n")

while(1):
   
    print(f"\033[38;5;39mTeste {n_teste}: \033[0;0m", end = "")
    n_teste += 1
    nos = code_graph()

    print(f"\n\033[38;5;11mCaminho:\033[0;0m\n{nos}\n")

    pares_arcos = []
    for i in range(len(nos)-2):  
        pares_arcos.append((nos[i], nos[i+1],nos[i+2]))

    pares_arcos = [(str(n1), str(n2), str(n3)) for (n1,n2,n3) in pares_arcos]  

    set_pares_arcos = sorted(set(pares_arcos))
    pares_arcos_testes = pares_arcos_testes.union(set_pares_arcos)

    pares_arcos_print = [list(item) for item in set_pares_arcos]
    print(f"\033[38;5;11mPares de arcos percorridos: \033[0;0m \n{pares_arcos_print}\n")

    print(f"\033[38;5;47mRequisitos já satisfeitos: \033[0;0m \n{pares_arcos_testes}\n")

    if (pares_arcos_testes == TR_pares_arcos):
        print(f'\033[48;5;42m\033[38;5;16m \033[1m TODOS OS REQUISITOS SATISFATÍVEIS FORAM ABRANGIDOS. \033[0;0m\n')
        break

    msg = f"\033[38;5;208mFalta passar pelos pares de arcos: {TR_pares_arcos - pares_arcos_testes} \033[0;0m"
    print(msg)


    if n_teste > 14:
        print(f"\033[2;31mHá chances dos pares de arcos não serem alcançáveis. Verifique o grafo.\033[0;0m")
    
    print("\033[2;34m" + "-" * 75 + "\033[0;0m")


    if n_teste > 14:
        print(f"\033[2;31mHá chances dos pares de arcos não serem alcançáveis. Verifique o grafo.\033[0;0m")
    print("\033[2;34m" + "-" * len(msg) + "\033[0;0m") 
