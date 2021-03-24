import subprocess, os, time

os.system('python ./fasa_program.py')
os.system('python ./usfa_program.py')
os.system('python ./usssa_program.py')
os.system('fix_duplicates.py')
os.system('python ./write_to_excel_spreadsheet1.py')
os.system('python ./write_to_excel_spreadsheet2.py')
# os.system('rm -r ./data_out/*.json')

time.sleep(100000)

print("Finished");