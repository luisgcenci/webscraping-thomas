import json
import xlwt
from xlwt import Workbook

data = {}
with open('usssa_coach_list.json', 'r') as file:
    data = json.load(file)

wb = Workbook()
db = wb.add_sheet('Sheet1')

row = 0

for team in data:
    db.write(row, 0, data[team]['team_name'])
    db.write(row, 6, data[team]['coach'])

    row += 1

wb.save('usssa_coach_list.xls')