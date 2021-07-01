
#Devanir Ramos Junior
#email: junior472399@gmai.com

#pip install pdfplumber
import pdfplumber
#pip install pandas
import pandas
import dic_acentos
import zipfile
import os
import webscraping

arquivo = "Padrao_TISS_Componente_Organizacional_202006.pdf"
#o programa baixa todas as tabelas de 2 colunas do pdf do TISS (o mesmo do webscraping)
print("Iniciado\n")
print("O programa irá extrair todas as tabelas de 2 colunas do arquivo pdf")
print("\"Padrao_TISS_Componente_Organizacional_XXXXXX\"")
print("As tabelas ficarão armazenadas no arquivo zip.")
print("\nDeseja baixar o arquivo? (caso não tenha)")
while True:
    print("1 - Sim, quero baixar;")
    baixar = input("2 - Não, já tenho.\n")
    if baixar in "12":
        if baixar == "1":
            print("Ok, o arquivo será baixado.")
            webscraping.webscraping()
            break
        else:
            print("Ok, não será baixado.")
            break
    else:
        print("Por favor, digite \"1\" ou \"2\".\n")

print("\nPor favor, aguarde um momento.\n")
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
def tabela_dataframe(pagina, num_tabela = 1):
    global nome
    #le o arquivo pdf
    file = pdfplumber.open(arquivo)
    #identifica tabelas na página e seleciona qual será extraida
    tabela_raw = file.pages[pagina - 1].find_tables()
    tabela_raw = tabela_raw[num_tabela - 1].extract()
    col1 = []
    col2 = []
    index = -1
    #algumas tabelas o pdfplumber reconhece com linhas fantasmas:
    #linhas com "" ou com None   -   (4 ou 6 linhas no total, de acordo com meus testes)
    #caso isso aconteça a tabela cai nesse tratamento especial
    if len(tabela_raw[0]) >= 4:
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
                        if palavra == "":
                            pass
                        else:
                            col2.append(caracter_especial(palavra))
            index = -1

    #situação normal. 2 linhas
    elif len(tabela_raw[0]) == 2:
        for item in tabela_raw:
            for index in range(len(item)):
                col1.append(caracter_especial(item[index]))
                col2.append(caracter_especial(item[index + 1]))
                break

    #guarda a palavra/título da tabela
    if col1[0] == "":
        nome = col1[1]
    else:
        nome = col1[0]
    #cria uma tabela vazia e adiciona as duas colunas
    data_frame = pandas.DataFrame()
    data_frame["A"] = col1
    data_frame["B"] = col2
    return data_frame

def criar_zip (nome_arquivo):
    arquivo_zip = zipfile.ZipFile("Teste_Intuitive_Care_Devanir_Ramos_Junior.zip", "a")
    arquivo_zip.write(nome_arquivo + ".csv")
    arquivo_zip.close()

#usado quando a tabela ocupa mais de uma página
arquivos = []
nomes = []
merge = ""
#numero da página com cada tabela
#o valor vazio é pra indicar que não é uma tabela de várias paginas
paginas = [56, "", 81, "", 81, 82, 83, 84, 85, 86, "", 87, "", 92, ""]
#o número da cada tabela na página,
#se tem duas tabelas na página e quero pegar a segunda o número será 2
num_tabela = [1, 0, 1, 0,  2, 1, 1, 1, 1, 1, 0,  1, 0, 1, 0]

for index in range(len(paginas)):
    if paginas[index] == "":
        pass
    else:
        resultado = tabela_dataframe(paginas[index], num_tabela[index])
        print("Transformando tabela...")
        if paginas[index + 1] != "":
            arquivos.append(resultado)
            nomes.append(nome)
        else:
            if len(arquivos) > 0:
                merge = pandas.concat(arquivos)
                merge.to_csv(nomes[0] + ".csv", index=False)
                criar_zip(nomes[0])
                os.remove(nomes[0] + ".csv")
                arquivos = []
                nomes = []
            else:
                resultado.to_csv(nome + ".csv", index=False)
                criar_zip(nome)
                os.remove(nome + ".csv")

#lembrando que no excel tem que colocar para delimitar a primeira coluna  por virgula
print("\nPrograma finalizado.")
