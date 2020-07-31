
import tabula

file = tabula.read_pdf("Padrao_TISS_Atualizado.pdf", multiple_tables=True, encoding="utf-8", pages="81-87")
print(file)
print(type(file))
tabula.convert_into("Padrao_TISS_Atualizado.pdf", "Padrao_TISS_Atualizado.csv", output_format="csv", pages="87")
