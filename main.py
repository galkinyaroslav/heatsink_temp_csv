import csv
import fnmatch
import os
from datetime import datetime

# Change the file name where you want to store a data
csvfilename = "raw_rocx_30_10_2020.csv"

# Function scans files in the directory(path) and returns a list of files with the pattern
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

prevfiledate = datetime.now()
prevdelta=0
print(prevfiledate)
arrfiles = find('*.rocx', '.')
print(arrfiles)

try:
    with open(csvfilename, mode='w', encoding="utf-8") as writefile:
        file_counter=0
        for each in arrfiles:

            try:
                with open(each, mode='r', encoding="utf-8") as readfile:
                    line_count=0
                    for line in readfile:
                        if line_count==0:
                            newline = line.strip("\n") + ','
                            newline = newline.replace('Сохранено: ', 'Дата,')
                            newline = newline.replace(' ', ',')
                            newline = newline.replace(';', ',')
                            newline = newline.replace('-', ',')
                            newline = newline.replace(':', ',')
                            newlinelist= newline.split(sep=',')
                            print(newlinelist)
                            curentfiledate=datetime(year=int(newlinelist[6]),month=int(newlinelist[5]),day=int(newlinelist[4]),hour=int(newlinelist[1]),minute=int(newlinelist[2]),second=int(newlinelist[3]))
                            del newlinelist[-6:]
                            newlinelist[1]=str(curentfiledate)
                            newlinelist+=['dt']
                            if file_counter==0:
                                newlinelist+=['0']
                                prevfiledate=curentfiledate
                            else:
                                delta=int((curentfiledate-prevfiledate).total_seconds())
                                newlinelist += [str(delta+prevdelta)]
                                prevfiledate=curentfiledate
                                prevdelta+=delta
                            newlinestr=','.join(newlinelist)+','
                            print(newlinestr)
                            writefile.write(newlinestr)
                            line_count+=1
                        else:
                            newline = line.strip("\n") + ','
                            newline = newline.replace('-', ',')
                            newline = newline.replace(';', ',')
                            newline = newline.replace('W', '')
                            newline = newline.replace('V', '')
                            newline = newline.replace('°C', '')
                            writefile.write(newline)
                            line_count += 1
                        file_counter += 1
                    writefile.write('\n')
            except IOError:
                print("'['1']'An IOError has occurred!")
except IOError:
    print("'['2']'An IOError has occurred!")

try:
    with open(csvfilename, mode='r', encoding="utf-8") as csvreadfile:
        with open("temperature.csv", mode='w', encoding="utf-8") as csvwritefile:
            csv_reader = csv.reader(csvreadfile, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    val = 1
                    strrow = 'Time,'
                    for val in range(62):
                        strrow += row[4 + 9 * val] + '-T1,'+row[4 + 9 * val]+'-T2,'
                    print(strrow)
                    csvwritefile.write(strrow + '\n')
                    strrow = str(row[3]) + ','
                    for val in range(62):
                        # print(f'{row[10 + 9 * val]}<->{row[11 + 9 * val]}')
                        strrow += row[11 + 9 * val] + ','
                        strrow += row[12 + 9 * val] + ','
                    print(strrow)
                    csvwritefile.write(strrow + '\n')
                    line_count += 1
                else:
                    strrow = str(row[3])+','
                    for val in range(62):
                        strrow += row[11 + 9 * val] + ','
                        strrow += row[12 + 9 * val] + ','
                    print(strrow)
                    csvwritefile.write(strrow + '\n')
                    line_count += 1
except IOError:
    print("An IOError has occurred!")