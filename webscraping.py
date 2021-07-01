
#Devanir Ramos Junior
#email: junior472399@gmai.com

#pip install beautifulsoup4
import bs4
#pip install requests
import requests

if __name__ == '__main__':
    print("Iniciado.\n")
    print("Selecione a opção que deseja:\n")
    # é possivel baixar o padrao TISS atual ou verificar o histórico das versões
    while True:
        print("1 - Baixar Padrão TISS (atualizado);")
        escolha = input("2 - Verificar o histórico do Padrão TISS.\n")
        print()
        if escolha in "12":
            if escolha == "1":
                palavra = "versão"
                break
            else:
                palavra = "versões"
                break
        else:
            print("Por favor, digite \"1\" ou \"2\".\n")

    print("Aguarde um momento, por favor.\n")

arquivo = ""
def webscraping(palavra_chave = "versão", escolha = "1"):
    #uso no programa de tranformar dados
    global arquivo

    # request para acessar o site e beautifulsoup para fazer tratamentos/filtrar
    site1 = "http://www.ans.gov.br/prestadores/tiss-troca-de-informacao-de-saude-suplementar"
    site1_request = requests.get(site1).text
    soup1 = bs4.BeautifulSoup(site1_request, "html.parser")

    # procura essa classe específica porque os links estão ai
    for linha in soup1.find_all("div", class_="alert alert-icolink"):
        string = str(linha)
        # verifica se no texto do link tem "versão" ou "versões" e pega o link da próxima página
        if palavra_chave in string.lower():
            string_separada = string.split("href=")
            site2 = string_separada[1].split("\"")
            site2_request = requests.get(site1[:22] + site2[1]).text
            soup2 = bs4.BeautifulSoup(site2_request, "html.parser")
            # se a escolha foi baixar o TISS atual:
            if escolha == "1":
                #analisa a tabela da página para encontrar o link do arquivo
                for linha in soup2.find_all("tr"):
                    string = str(linha)
                    if "componente organizacional" in string.lower():
                        print("Baixando...\nPode demorar alguns segundos...\n")
                        string_separada = string.split("href=")
                        file = string_separada[1].split("\"")
                        file_request = requests.get(site1[:22] + file[1])
                        arquivo = file[1].split("/")
                        arquivo = arquivo[-1]
                        pdf = open(arquivo, 'wb')
                        pdf.write(file_request.content)
                        pdf.close()
                        print("Versão mais nova do Padrão TISS salva como \"" + arquivo + "\"")
                        break
            # se a escolha foi ver o histórico do TISS
            else:
                txt = open("Histórico_TISS.txt", "w", encoding="utf-8")
                for linha in soup2.find_all("tr"):
                    string = str(linha.text)
                    string_separada = string.split("\n")
                    texto = ["Competência", "Publicação", "Início de Vigência", "Limite de Implantação",
                             "Organizacional", "Conteúdo e Estrutura", "Representação de Conceitos",
                             "Segurança e Privacidade", "Comunicação"]
                    try:
                        for index in range(len(string_separada)):
                            text = (texto[index] + ": " + string_separada[index + 1])
                            print(text)
                            txt.write(text + "\n")
                    # try/except usado porque a primeira "linha" é uma única string com o cabeçalho da tabela
                    except:
                        pass

                    print("-" * 35)
                    txt.write("-" * 35 + "\n")

                txt.close()
                print("\nConteúdo salvo em \"Histórico_TISS.txt\"")
                break

            break




if __name__ == '__main__':
    webscraping(palavra, escolha)
    print("\nPrograma finalizado.")
