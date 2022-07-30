
def baralho3(entrada):
    cartas = []
    for i in range(0,len(entrada),3):
        cartas = cartas + [entrada[i:i+3]]
        
    cartas.sort()
    valores = ['01','02','03','04','05','06','08','09','10','11','12','13']
    ordem = ['C','E','U', 'P']
    faltam = [13, 13, 13, 13]

    i = 0
    for valor in valores:       
        for j in [0,1,2,3]:
            naipe = ordem[j]
            carta = cartas[i]            
            if carta == valor + naipe:
                if faltam[j] != 'erro':
                    faltam[j] = faltam[j] - 1
                i = i + 1
                while i < len(cartas) and cartas[i] == carta:
                    faltam[j] = 'erro'
                    i = i + 1
                if i == len(cartas):
                    return faltam
                    
entrada = input()
baralho3(entrada)

