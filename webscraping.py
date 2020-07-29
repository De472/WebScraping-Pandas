
import bs4
import requests

#request para acessar o site e beautifulsoup para fazer tratamentos/filtrar
site1 = "http://www.ans.gov.br/prestadores/tiss-troca-de-informacao-de-saude-suplementar"
site1_request = requests.get(site1).text
soup1 = bs4.BeautifulSoup(site1_request, "html.parser")
site2 = ""
site2_request = ""
soup2 = ""

#print(soup1.prettify())

#procura essa classe específica porque os links "ISS" estão ai
for linha in soup1.find_all("div", class_= "alert alert-icolink"):
    string = str(linha)
    #verifica se no texto do link tem "versão" e pega o link
    if "versão" in string.lower():
        string_separada = string.split("href=")
        site2 = string_separada[1].split("\"")
        site2_request = requests.get(site1[:22] + site2[1]).text
        soup2 = bs4.BeautifulSoup(site2_request, "html.parser")
#print(soup2.prettify())

for linha in soup2.find_all("tr"):
    string = str(linha)
    if "componente organizacional" in string.lower():
        string_separada = string.split("href=")
        file = string_separada[1].split("\"")
        print(file[1])
        file_request = requests.get(site1[:22] + file[1])
        pdf = open("Padrao_TISS.pdf", 'wb')
        pdf.write(file_request.content)
        pdf.close()




