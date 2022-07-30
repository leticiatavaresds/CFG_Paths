# Script Teste Cobertura de Nós
TR_nos = set(['2: enter', '2: exit', 3, 4, 4, 4, 5, 7, 8, 9, 10, 12, 13, 13, 13, 14, 14, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28])


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

# Teste de nós
nos_testes = set([])
n_teste = 1

print(f"\n\033[38;5;87mTR Cobertura de Nós: \033[0;0m\n{TR_nos} \033[0;0m\n")

while(1):

    print(f"\033[38;5;39mTeste {n_teste}: \033[0;0m", end = "")
    n_teste += 1

    nos = code_graph()
    prev = object()
    nos = [prev:=v for v in nos if prev!=v]

    print(f"\n\033[38;5;11mCaminho:\033[0;0m\n{nos}\n")
    nos_testes = nos_testes.union(set(nos))

    print(f"\033[38;5;11mNós percorridos: \033[0;0m\n{list(set(nos))}\n")

    print(f"\033[38;5;47mRequisitos já satisfeitos: \033[0;0m \n{nos_testes}\n")

    # print(TR_nos - nos_testes)
    if (nos_testes == TR_nos):
        print(f'\033[48;5;42m\033[38;5;16m \033[1m TODOS OS REQUISITOS SATISFATÍVEIS FORAM ABRANGIDOS. \033[0;0m\n')
        break

    msg = f"\033[38;5;208mFalta passar pelos nós: {TR_nos - nos_testes} \033[0;0m"
    print(msg)

    if n_teste > 14:
        print(f"\033[2;31mHá chances dos nós não serem alcançáveis. Verifique o grafo.\033[0;0m")
    
    print("\033[2;34m" + "-" * 75 + "\033[0;0m")
