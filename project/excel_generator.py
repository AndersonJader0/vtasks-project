import pandas as pd
from openpyxl.styles import Alignment
from xlsxwriter import Workbook

class excelGenerator():
 
    def getExcel(self, tasks, tasks_aproveds):
        try:
            dados = pd.DataFrame(data= tasks)
            dados.to_excel('Tarefas.xlsx', index=False, sheet_name='Tarefas Committed - Sustentação')
            print("Relatório Excel gerado.")
        except:
            print("Algo deu errado na geração do relatório.")
 
        dados = dados._append({
        'PBI': '',
        'DESCRIÇÃO': '',
        'STATUS': tasks_aproveds,
        'EFFORT': ''
        },
        ignore_index=True)
        writer = pd.ExcelWriter('enhanced.xlsx', engine='xlsxwriter')
        dados.to_excel(writer, index=False, sheet_name='Tarefas Committed - Sustentação')
        workbook = writer.book
        worksheet = writer.sheets['Tarefas Committed - Sustentação']
        # Look xlsxwriter
        worksheet.set_zoom(100)
 
        #Set header formating
        header_format = workbook.add_format({
            "valign": "vcenter",
            "align": "center",
            "bg_color": "#195d7a",
            "bold": True,
            "font_color": "#fffff"
        })
 
        #Add title
        # title = "Tarefas Committed - Sustentação"
        format = workbook.add_format()
        format.set_font_size(25)
        format.set_font_color("#ffffff")
        
        for col_num, value in enumerate(dados.columns.values):
            worksheet.write(0, col_num, value, header_format)
 
        #Adjust the column width
        worksheet.set_column('B:B', 70)
 
        # total_aprovadas_cell = dados['C{}'.format(len(dados) - 1)]
        # total_aprovadas_cell.alignment = Alignment(horizontal='right')
        right_format = workbook.add_format({'align':'right'})
 
        tmn = int(len(tasks)) + 1
        worksheet.write(tmn, 1, "Total Aprovadas",right_format)

        writer._save()