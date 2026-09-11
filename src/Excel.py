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
        "Mínimo",
        "Máximo",
        "Rápidos"
    ])

    return planilha, aba

def salvar(planilha, sheet, ciclo, media, mediana, minimo, maximo, rapidos):
    sheet.append([ciclo, media, mediana, minimo, maximo, rapidos])

    planilha.save("resultados.xlsx")