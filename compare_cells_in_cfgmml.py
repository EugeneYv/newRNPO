
cell1 = 'CELLID=6362,'
cell2 = 'CELLID=18586,'

with open("C:\wHesron\RNC\comparefile_6362_18586_UH_CR_allcommands.txt", "w") as comparefile:
    with open("C:\wHesron\RNC\CFGMML-20230502115415.txt", "r") as cfgmml:
        for line in cfgmml:
            if cell1 in line:
                comparefile.write(line)
                list1 = line.split(',')
                # print(list1)
                # print(list1[1:])
            elif cell2 in line:
                comparefile.write(line) # убрать если надо только неодинаковое записать
                comparefile.write('\n') # убрать если надо только неодинаковое записать
                list2 = line.split(',')
                # if list2[1:] != list1[1:]:  # этот блок нужен если надо записать только неодинаковое
                #    comparefile.write(line)
                #    comparefile.write('\n')




