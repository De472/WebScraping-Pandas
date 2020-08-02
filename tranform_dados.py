
import pdfplumber
import pandas
import dic_acentos
import zipfile
import os

#fiz esse "programinha" para testes, mas pode rodar sem ele também

#talvez n exista esse programinha
'''

print("Iniciado\n\n")
print("Selecione a(s) página(s) que deseja extrair uma tabela.\n")
print("Exemplo: 81, 82, 83, 84, 85, 86")
num_paginas_raw = input("Página(s): ")
print("\nSua tabela é a primeira da primeira página selecionada? Se for, digite 1,")
print("se não for digite 2 caso seja a segunda, 3 para terceira, em diante.")
num_tabela_raw = input("Tabela: ")

num_paginas = num_paginas_raw.split(",")
num_tabela = num_paginas_raw.strip()
'''
print("\nOk, aguarde um momento.\n")
#no pandas não consegui manter caracteres especiais (com acento),
#função criada para trocar o caracter especial com um normal
def caracter_especial (palavra):
    for key in dic_acentos.dic.keys():
        palavra = palavra.replace(key, dic_acentos.dic[key])
    return palavra

#pdfplumber + pandas
#pdfplumber trata os dados do pdf e pandas cria dataframes (tabelas)
#consegue apenas pegar tabelas com 2 colunas
nome = ""
def tabela_pdf_para_csv(pagina, num_tabela = 1):
    global nome
    #le o arquivo pdf
    file = pdfplumber.open("Padrao_TISS_Atualizado.pdf")
    #identifica tabelas na página e seleciona qual será extraida
    tabela_raw = file.pages[pagina - 1].find_tables()
    tabela_raw = tabela_raw[num_tabela - 1].extract()
    col1 = []
    col2 = []
    print("Antes de printar tabela_raw")
    print(tabela_raw)
    index = -1
    #algumas tabelas o pdfplumber reconhece com linhas fantasmas:
    #linhas com "" ou com None   -   (4 ou 6 linhas no total, de acordo com meus testes)
    #caso isso aconteça a tabela cai nesse tratamento especial
    if len(tabela_raw[0]) >= 4:
        print("caiu na tabela 4")
        for item in tabela_raw:
            for palavra in item:
                index += 1
                #filtra os None
                if type(palavra) == type("a"):
                    #nos testes que fiz sempre cai uma palavra antes da metade e a outra depois
                    if index <= 2:
                        #evita duplicidade e mantem igualdade de tamanho
                        if caracter_especial(palavra) in col1:
                            col2.append("")
                        else:
                            col1.append(caracter_especial(palavra))
                    else:
                        #quando identifica 6 linhas isso mantem a igualdade
                        if palavra == "":
                            pass
                        else:
                            col2.append(caracter_especial(palavra))
            index = -1

    #situação normal. 2 linhas
    elif len(tabela_raw[0]) == 2:
        print("caiu na tabela 2")
        for item in tabela_raw:
            print(item)
            for index in range(len(item)):
                col1.append(caracter_especial(item[index]))
                col2.append(caracter_especial(item[index + 1]))
                break

    if col1[0] == "":
        nome = col1[1]
    else:
        nome = col1[0]
    print(col1)
    print(col2)
    print("Antes de fazer a tabela")
    tabela = [col1, col2]
    print("Antes de fazer o dataframe")
    print(tabela)
    #cria uma tabela vazia e adiciona as duas colunas
    data_frame = pandas.DataFrame()
    data_frame["A"] = col1
    data_frame["B"] = col2
    print(data_frame)
    print("a")
    #cria o arquivo csv
    data_frame.to_csv("Testando.csv", index=False)
    return data_frame

def criar_zip ():
    arquivo_zip = zipfile.ZipFile("Teste_Intuitive_Care_Devanir_Ramos_Junior.zip", "w")
    arquivo_zip.write((nome + ".csv"))
    arquivo_zip.close()




arquivos = []


tabela_pdf_para_csv(81).to_csv((("/tabelas" + nome + ".csv")), index=False)
criar_zip()
for index in range(6):
    arquivos.append(tabela_pdf_para_csv(81 + index))
    print("-" * 50)
merge = pandas.concat(arquivos)
print(merge)
merge.to_csv((nome + ".csv"), index=False)
criar_zip()

tabela_pdf_para_csv(87).to_csv((nome + ".csv"), index=False)

criar_zip()