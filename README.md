  ## Geração de CFG e visualização de caminhos

O projeto consiste em uma automação que em sua atual versão objetiva ser um complemento para o algoritmo de geração de CFG do fuzzing book para auxílio de testes de cobertura de grafos de programas mais simples em python. Há ainda muitas melhorias que podem ser implementadas para que se torne uma ferramenta robusta capaz de auxiliar profissionais com os mais complexos testes de softwares. A automação foi implementada utilizando Anaconda 4.13.0 e a linguagem python3 versão 3.10. O usuário tem duas opções de utilizá-la, pode-se rodar o código através do notebook ipynb presente no repositório ou pela aplicação web contida na pasta "Web Application" 

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
