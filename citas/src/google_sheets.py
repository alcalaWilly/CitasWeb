#script para manipular hojas  de calculo de Google sheets
import gspread

class GoogleSheets:
    def __init__(self,credentials,document,sheet_name):
        self.gc = gspread.service_account_from_dict(credentials)
        self.sh = self.gc.open(document)
        self.sheet = self.sh.worksheet(sheet_name)

    def escribir_dato(self, range,data):
        self.sheet.update(range,data)

    #el rango donde escribir
    def escribir_untimaFila(self):
        ultima_fila = len(self.sheet.get_all_values()) + 1
        deta = self.sheet.get_values()
        range_start = f"A{ultima_fila}"
        range_end = f"{chr(ord('A')+len(deta[0])-1)}{ultima_fila}"#determinar el rango de la hoja
        return f"{range_start}:{range_end}"
