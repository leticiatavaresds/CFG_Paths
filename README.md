# Geração de CFG e visualização de caminhos

# Índice

- [Introdução](#introdução)
- [Microdados ENADE](#microdados-enade)
- [Obtenção dos Dados](#obtenção-dos-dados)
- [Modelagem de Dados](#modelagem-de-dados)
- [Tratamento de Dados](#tratamento-de-dados)
- [Análise Exploratória](#análise-exploratória)
- [Modelo de Predição](#modelo-de-predição)
- [Execução](#execução)
- [Licença](#licença)

# Introdução

O projeto consiste em uma automação que em sua atual versão objetiva ser um complemento para o algoritmo de geração de CFG do fuzzing book para auxílio de testes de cobertura de grafos de programas mais simples em python. Há ainda muitas melhorias que podem ser implementadas para que se torne uma ferramenta robusta capaz de auxiliar profissionais com os mais complexos testes de softwares. A automação foi implementada utilizando Anaconda 4.13.0 e a linguagem python3 versão 3.10. O usuário tem duas opções de utilizá-la, pode-se rodar o código através do notebook ipynb presente no repositório ou pela aplicação web contida na pasta [Web Application](https://github.com/leticiatavaresds/CFG_Paths/tree/main/Web%20Application)

# Metodologia

O [algoritmo](https://www.fuzzingbook.org/html/ControlFlow.html#Control-Flow-Graph/) desenvolvido pelo fuzzing book integrado à automação gera um CFG para um programa em python cuja representação visual procura ser bem intuitiva. O formato de cada nó é determinado pelo seu tipo: o início e o fim são ovais e possuem bordas duplas, nós com instrução condicional são em formato de diamante enquanto todo o resto são retangulares. Já os arcos variam em relação a cor, há arcos coloridos de forma a ser mais intuitivo para o usuário identificar qual caminho é seguido se a condição presente no nó for verdadeira (arco azul) ou falsa (arco vermelho). Esses tipos de recursos podem auxiliar o usuário a ler melhor o grafo.

Cada nó do grafo pode ter um ou mais filhos dependendo do tipo de instrução que ele representa. Por exemplo, um nó que representa um comando de loop ou condicional terá dois filhos, um para caso a condição seja verdadeira e o outro para o caso de ser falsa. Um nó de instrução de loop também terá pelo menos mais um arco vindo da última instrução dentro do loop.
  
Com acesso ao código fonte fornecido pelo usuário mais a estrutura do CFG produzido, nossa abordagem analisa cada linha do script, já que para cada instrução do programa é necessário verificar seu conteúdo para modificá-lo corretamente de forma que ele consiga gerar o caminho certo para qualquer entrada, isso porque percebe-se que algumas instruções não afetam o fluxo de execução enquanto outras como os comandos for ou while ou instruções condicionais como if, elif e else  ou palavras reservadas break, continue ou return exercem forte influência no fluxo. 
  
Após modificações no script do programa de acordo com as análises das linhas, temos um novo script que reflete o CFG criado, ou seja, além das linhas originais, há também linhas que adicionam os nós nas partes certas do código para que quando seja executado, o caminho que a execução percorre no grafo seja devidamente identificado. Nossa automação cria então três novos scripts que podem ser utilizados para verificar o caminho que um teste concreto percorre para os critérios de cobertura de nós, cobertura de arcos e cobertura de pares de arcos. O Script também apresenta o conjunto TR do critério para o CFG e encerra a execução caso todos os critérios do conjunto sejam satisfeitos.
  
# Implementação

A automação foi desenvolvida em Python versão 3.10 como complemento ao algoritmo de geração de CFG do fuzzing book a fim de aumentar sua funcionalidade. O usuário deve fornecer como entrada o arquivo .py com o programa fonte escrito necessariamente em linguagem python, sem falhas. Uma vez em posse das instruções do programa de entrada, o primeiro passo realizado é a geração do grafo de controle de fluxo de acordo com as instruções através do algoritmo fuzzing book, construído  com a ajuda de algumas bibliotecas como o ‘PyGraphViz’. 

Percebe-se que, para cada nó, a representação apresenta sua respectiva instrução antecedida por um número que indica em qual linha do arquivo de entrada a instrução se encontra. Instruções com comando de loop como for resultam em três nós, um para a inicialização da variável utilizada para o controle do loop, outro para a checagem da condição de parada e outro para o incremento da variável de controle, por isso, no exemplo abaixo temos três nós com o número 8. Após uma análise dos grafos, concluímos que a separação desses nós era redundante para a construção do caminho, assim, optamos por utilizar esses números como identificadores e tratamos os nós que apresentam o mesmo número e são em sequência como um só. Essa união só não vale para os nós de entrada e saída de função, onde apesar de apresentarem o mesmo número, deixamos um nó de entrada e um nó de saída os diferenciando pelas palavras "enter" e "exit" que os acompanha.

A maneira encontrada de permitir que o usuário veja o caminho que uma entrada executa é criar uma versão modificada do script original que apresenta uma lista para armazenação dos nós ao longo da execução. A lista se inicia vazia e, através de comandos de append, adiciona os nós ao longo do código de maneira a seguir os mesmos fluxos do grafo gerado para o script. Por exemplo, para o código apresentado na figura 1, ao realizarmos essa modificação para apresentar os fluxos do grafo obtido, ficaríamos com a versão apresentada abaixo, onde para o usuário ver o caminho de uma entrada, basta executar o script com o input desejado e olhar a lista “nos” ao final da execução.

Para que a automação realize as modificações apresentadas acima no código fonte de modo que o usuário visualize o caminho que determinada entrada realiza de acordo com o grafo produzido é necessário que ela tenha acesso não só ao código fonte, como também ao próprio grafo. Interpretar a estrutura do CFG através da imagem seria uma tarefa bastante árdua, contudo, além da representação visual, os dados do digrafo construído são armazenados em uma variável denominada cache. Assim, através da função “cache_to_json”, o algoritmo constrói um dicionário para cada nó a partir da cache, com as seguintes informações:  
- id
- nós pais
- nós filhos
- identificação da linha em que se encontra a instrução 
- tipo da instrução. 

Com acesso às linhas do código fonte e aos dados do grafo para referência, inicia-se então as modificações do script original através da função “make_code_path”, onde para cada linha realiza-se uma análise de seu conteúdo e de suas informações no grafo, caso existam. Há três situações que observamos que necessitava de um tratamento diferenciado e uma estrutura de controle para adicionar os nós nos lugares certos do script, abaixo descrevemos a maneira com que a automação lida com cada uma dessas situações:

- blocos de loop com for ou while:  Em loops, inicialmente passa-se pelo nó de verificação da condição de entrada, caso verdadeira, segue-se por todos os nós presentes no bloco, realizando assim uma iteração. Após cada iteração, é necessário voltar para o nó de checagem da condição de entrada, que se falsa, pula o bloco e segue para o próximo nó fora do loop. Assim, em um CFG, o nó da última instrução do bloco do loop e nós de instrução de continue devem apontar para o nó de checagem de entrada do loop. Para que a automação conseguisse adicionar a linha “nos.append(x)” nesses pontos, precisamos criar uma estrutura que para cada linha que apresenta o comando for ou while, armazena seu identificador, sua indentação e o indicador se o bloco do loop já foi finalizado, inicialmente atribuído com o valor falso. Dessa forma, caso apareça um comando de continue, pega-se o último identificador adicionado que apresenta o indicador falso na estrutura a assim conseguimos adicionar a linha “nos.append(x)” com x sendo o identificador correto do loop ao qual o comando pertence imediatamente antes de adicionar a linha com a instrução continue. Como em python podemos identificar o fim de um bloco pela indentação, para cada linha analisa-se se há algum identificador na estrutura com o indicador falso e com indentação igual ou maior, caso haja, significa que a linha analisada é primeira linha fora do bloco dos loops desses identificadores, com isso conseguimos colocar a linha “nos.append(x)” no fim dos blocos desses loops adicionando “nos.append(x)” com indentação igual à indentação indicada na estrtura mais um tab.

- blocos de função com o comando def: em uma função, inicialmente passa-se pelo nó de entrada e ao fim das instruções da função, ou caso apareça um nó de return, segue-se para o nó de saída da função. Para que a automação conseguisse adicionar a linha “nos.append(“x: exit”)” nesses pontos de saída da função também foi necessário criar uma estrutura que para cada linha que apresenta o comando def, armazena seu identificador, sua indentação e o indicador se o bloco da função já foi finalizado, inicialmente atribuído com o valor falso. Dessa forma, caso apareça um comando de return, pega-se o último identificador adicionado que apresenta o indicador falso na estrutura a assim conseguimos adicionar a linha “nos.append(x)” com x sendo o identificador correto da linha da função ao qual o comando referencia. Para cada linha analisa-se se há algum identificador na estrutura com o indicador falso e com indentação igual ou maior, caso haja, significa que a linha analisada é primeira linha fora do bloco da função desses identificadores, com isso conseguimos colocar a linha “nos.append(x)” no fim dos blocos dessas funções adicionando “nos.append(x)” com indentação igual à indentação indicada na estrtura mais um tab.

- blocos de elif e blocos de else após um elif: nos blocos de elif deve ter o comando “nos.append(x)” para os nós de checagem de cada elif antecedente, isso porque a execução de um bloco de elif implica que os blocos de outros elif anteriores não foram executados, porém os nós de checagem dessas condições devem aparecer no caminho, já que passamos por eles, só não passamos pelos nós de seus blocos já que as checagens deram False. Para fazer essas adições corretamente há um dicionário que caso a linha analisada apresente o primeiro comando elif após um if, armazena-se nesse dicionário,utilizando como chave a indentação da linha, uma lista inicializada apenas com o identificador da linha e um indicador se a sequência de elif’s já foi finalizada, inicialmente atribuído com o valor falso. Assim, para cada linha com elif subsequente é adicionado seu identificador à lista e adiciona-se a linha “nos.append(x)” ao script modificado para cada identificador presente na lista. O mesmo acontece para uma linha que apresente o comando else caso o dicionário apresente um valor para a indentação com indicador False, que implica que há uma sequência de blocos de elif’s ainda não finalizada antes do else. O final de blocos de elif’s é determinado por meio de comparação de indentações, onde caso tenha um bloco de elif’s ativo no dicionário e apareça uma linha com indentação menor que a do bloco, implica que esse bloco foi finalizado,

Para instruções que não se encaixam em nenhuma das situações abordadas acima, primeiro a automação checa se há nó na cache cuja instrução está situada na linha sendo analisada. Se não, a instrução apenas é copiada no novo script modificado, se sim, além de copiar a linha, adiciona-se também a instrução “nos.append(x)” com x sendo o identificador da linha analisada seguindo a mesma indentação.

Terminadas as análises das linhas e a modificação do código fonte, ficamos então com um novo script que apresenta a variável “nos” inicializada como uma lista vazia e que através de comandos “nos.append(x)”, presentes ao longo de suas instruções consegue refletir o CFG criado para o script original e dessa forma, se o usuário executar o novo script poderá ver o caminho percorrido pelo input no digrafo ao olhar para a variável “nos” após a execução. 

Pensado nos testes de Cobertura de Nós, Cobertura de Arcos e Cobertura de Pares de Arcos, a partir do script modificado, a automação cria um script para cada um desses três testes. Esses scripts apresentam o conjunto de requisitos de teste TR para a o tipo de cobertura em questão e através de um loop, mantém a execução até que os testes concretos passados pelo usuário satisfaçam o TR. A cada teste passado é mostrado o caminho percorrido pela entrada, os requisitos satisfeitos pelo caminho e os requisitos que ainda não foram satisfeitos por nenhum teste concreto desde o início da execução.

Importante ressaltar que muitos programas podem apresentar requisitos insatisfatíveis para esses testes de coberturas, como por exemplo um par de arco que nunca é percorrido por qualquer entrada. A primeiro momento, decidimos não tratar desses casos, pois iria demandar mais atenção e tempo para implementação, assim caso o programa apresente requisitos insatisfatíveis, o script ficará em loop até que o usuário force sua parada. Contudo, nossa automação adiciona aos scripts de teste um comando para que se forem realizados mais testes concretos do que duas vezes o número de comandos condicionais presentes no script original, é impresso para o usuário que os requisitos ainda não satisfeitos podem ser insatisfatíveis e que ele deveria analisar o grafo para realizar essa checagem.

Para mostrar a funcionalidade da automação, vamos utilizar como entrada o programa desenvolvido para o problema de baralho dado durante o curso. O código da automação se encontra na página do github [5] e é necessário seguir os passos presentes no arquivo “README” para garantir uma execução correta. Com o repositório baixado e ambiente devidamente configurado, o usuário tem duas opções de executar a automação, a primeira é pelo notebook python presente no repositório, enquanto que a segunda é executar a aplicação web seguindo as instruções presentes na página do github.

Optando pela execução da aplicação web, primeiro, é necessário salvar o programa em um script .py como mostrado na figura acima e salvá-lo dentro da pasta “uploads”. Inicialmente o usuário se depara com a tela inicial como apresentada na figura 6. É necessário então clicar em “Choose a File”, selecionar o script .py dentro da pasta “uploads”, clicando em submit em seguida.

Caso de fato exista o script na pasta e o código esteja no padrão aceito, a automação irá gerar o grafo e os script de testes de coberturas para o programa selecionado. Uma nova tela aparecerá como na figura 7 contendo quatro opções. A primeira levará o usuário para uma tela que contém o grafo gerado, enquanto que as três últimas opções irão redirecionar para uma página com o script para teste de cobertura de nós, teste de cobertura de arcos e teste de cobertura de pares de arcos como indicado.

O usuário pode então realizar o download desses arquivos e utilizá-los para testes. Para exemplificar, realizamos o download do “Script Cobertura de Nós” e o executamos. Primeiramente é exibido os Requisitos de teste do tipo de cobertura em questão obtidos a partir do grafo gerado. Em seguida inicia-se o loop onde, para cada teste, o usuário deve fornecer a entrada esperada pelo programa para que o script indique então o caminho percorrido no grafo, os requisitos satisfeitos pelo teste, os requisitos satisfeitos por todos os teste até o momento e quais requisitos faltam cobrir. Na execução do script apresentada na figura 8, temos o conjunto de requisitos indicados pelo “TR Cobertura de Nós”, o primeiro teste em que o usuário deu como entrada o baralho “01C” e o segundo teste onde foi dado como entrada o baralho “01U01P01P”. 

Nota-se pela figura que o script encerra a execução logo após o segundo teste, isso porque o conjunto composto pelos dois testes satisfaz todos os requisitos. Porém, se houvesse requisitos insatisfatíveis como acontece no caso de cobertura de pares de arcos desse problema, a execução se manteria em loop até que o usuário forçasse sua parada, exibindo a mensagem “Há chances dos pares de arcos não serem alcançáveis. Verifique o grafo.” a partir de determinado teste. O usuário pode então tentar verificar quais são são os requisitos insatisfatíveis através do grafo gerado e manualmente retirá-los do conjunto TR declarado no script de teste.

# Execução

### Opção 2 - Aplicação Web
Inicialmente, é necessário criar um ambiente virtual com a versão correta do python e as bibliotecas utlizadas devidamente instaladas, para isso execute o comando:

```sh
$ conda env create --file environment.yml
```

Após a criação do ambiente, é necessário ativá-lo através do comando:
```sh
$ conda activate CFG_paths
```

Com o ambiente instalado e as bibliotecas instaladas, basta apenas rodar o projeto com o comando:
```sh
$ python app.py
```

A aplicação ficará então disponível no endereço endicado no cmd podendo ser acessado por qualquer navegador.

# Licença

The MIT License (MIT) 2022 - Letícia Tavares. Leia o arquivo [LICENSE.md](https://github.com/leticiatavaresds/CFG_Paths/blob/master/LICENSE.md) para mais detalhes.

[⬆ Voltar ao topo](#geração-de-cfg-e-visualização-de-caminhos)<br>
