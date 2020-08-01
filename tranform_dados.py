
import tabula
import pdfplumber
import pandas
import dic_acentos

#tabula será usado para a tabela 31, na 30 e 32 gera apenas uma coluna e não consegui resolver na tabula
a = False
if a:
    file = tabula.read_pdf("Padrao_TISS_Atualizado.pdf", area=[119, 138, 211, 342], pages="81")
    print(file)
    print(type(file))
    #tabula.convert_into("Padrao_TISS_Atualizado.pdf", "Padrao_TISS_Atualizado.csv", output_format="csv", pages="81-86")

#pdfplumber + pandas nas tabelas 30
#pdfplumber trata os dados do pdf e pandas cria dataframes (tabelas)
file = pdfplumber.open("Padrao_TISS_Atualizado.pdf")
tabela_raw = file.pages[80].extract_table(table_settings={})
col1 = []
col2 = []
index = -1
print(tabela_raw)
for item in tabela_raw:
    print(item)
    for palavra in item:
        index += 1
        print(item[index])
        if type(palavra) == type("a"):
            if index <= 2:
                if palavra in col1:
                    col2.append("")
                else:
                    col1.append(palavra)
            else:
                    col2.append(palavra)
    index = -1

tabela = [col1, col2]
data_frame = pandas.DataFrame()
data_frame["A"] = col1
data_frame["B"] = col2
data_frame.replace({"B" : dic_acentos.dic}, regex=True)
print(data_frame)
print("a")
data_frame.to_csv("Testando.csv", index=False, encoding="utf-8")




