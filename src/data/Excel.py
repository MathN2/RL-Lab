from openpyxl import Workbook

planilha = Workbook()
sheet_original = planilha.active
planilha.remove(sheet_original) # type: ignore

def criar_sheet(sheet_name):
    aba = planilha.create_sheet(sheet_name)

    aba.append([
        "Ciclo",
        "Média",
        "Mediana",
        "Menor",
        "Maior",
        "Eficiencia"
    ])

    return planilha, aba

def salvar_resultados(planilha, sheet, ciclo, media, mediana, menor, maior, rapidos):
    sheet.append([ciclo, media, mediana, menor, maior, rapidos])

    planilha.save("data/resultados.xlsx")

def salvar_passos(dados):
    with open("data/passos.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write("".join(dados))

def salvar_qtable(dados):
    with open("data/qtable.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write("".join(dados))