import re
import time

# SCRIPT UTILIZADO PARA TRANSFORMAR O ARQUIVO DE LOG EM UM BINÁRIO PARA SER EXPLORADO.

# Expressão regular para extrair as 4 "words" de cada endereço de memória
exp = re.compile(r'^([a-f0-9A-F]+):\s+((?:[a-f0-9A-F]{8}\s+){3}[a-f0-9A-F]{8})')
# traduzindo a expressão: "Procurar no inicio da linha por um ou mais caracteres alfanuméricos seguido de um ':' (grupo 1) seguido de um ou mais espaços em branco e seguido por
# outros 3 blocos de 8 caracteres alfanuméricos (que não serão capturados pois estão diantes de um grupo de não captura '?:') seguido de um ou mais espaços em branco seguido por um
# ultimo bloco de 8 caracteres alfanuméricos (grupo 2)"

# Assim uma linha "9f000020: 100001a8 00000000 100001a6 00000000    ................" se torna "100001a8 00000000 100001a6 00000000"

qtde_linhas = 0
inicio = time.time()

with open('dump_word_by_word.log', 'r') as f:
    with open('extracted_bin.bin', 'wb') as bf:
        for line in f.readlines():
            qtde_linhas+=1
            words = exp.match(line).group(2).split(sep=' ')

            for word in words:
                bin_data = bytes.fromhex(word)
                bf.write(bin_data)


final = time.time()

print(f"Tempo decorrido com split: {(final-inicio):.4f}")
print(f"Linhas processadas: {qtde_linhas}")