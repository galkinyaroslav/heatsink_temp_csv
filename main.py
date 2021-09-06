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

arrfiles = find('*.rocx', '.')
print(arrfiles)


def struct_first_line(m_line_count,m_line):
    if m_line_count == 0:
        m_newline = m_line.strip("\n") + ','
        m_newline = m_newline.replace('Сохранено: ', 'Дата,')
        m_newline = m_newline.replace(' ', ',')
        m_newline = m_newline.replace(';', ',')
        m_newline = m_newline.replace('-', ',')
        m_newline = m_newline.replace(':', ',')
        m_newlinelist = m_newline.split(sep=',')
        print(m_newlinelist)

        curentfiledate = datetime(year=int(m_newlinelist[6]), month=int(m_newlinelist[5]), day=int(m_newlinelist[4]),
                                  hour=int(m_newlinelist[1]), minute=int(m_newlinelist[2]), second=int(m_newlinelist[3]))
        del m_newlinelist[-6:]
        m_newlinelist[1] = str(curentfiledate)
        m_newlinelist += ['dt']
        prevfiledate = datetime.now()
        prevdelta = 0
        print(prevfiledate)
        if file_counter == 0:
            m_newlinelist += ['0']
            prevfiledate = curentfiledate
        else:
            delta = int((curentfiledate - prevfiledate).total_seconds())
            m_newlinelist += [str(delta + prevdelta)]
            prevfiledate = curentfiledate
            prevdelta += delta
        newlinestr = ','.join(m_newlinelist) + ','
        print(newlinestr)
        return newlinestr
    else:
        dict_all_values_in_a_file_key = m_line[:m_line.find("-")]
        print(dict_all_values_in_a_file_key)
        m_newline = m_line.strip("\n") + ','
        m_newline = m_newline.replace(';', ',')
        m_newline = m_newline.replace('W', '')
        m_newline = m_newline.replace('V', '')
        m_newline = m_newline.replace('°C', '')
        list1 = (m_newline[m_newline.find("-") + 1:len(m_newline)]).split(",")
        # print("list1"+str(list1))
        m_newline = m_newline.replace('-', ',')
        # print(m_newline)
        counter = 0
        for i in dict_unit_keys.keys():
            """dict1[i]=list1[counter]"""
            dict_unit_keys.update({i: list1[counter]})
            counter += 1
        dict_all_values_in_a_file.update({dict_all_values_in_a_file_key: dict_unit_keys.copy()})
        return m_newline

dict_all_values_in_a_file={}
dict_unit_keys={"1.7V":0,
       "1.7W":0,
       "3.0V":0,
       "3.0W":0,
       "3.8V":0,
       "3.8W":0,
       "T1°C":0,
       "T2°C":0}

try:
    with open(csvfilename, mode='w', encoding="utf-8") as writefile:
        file_counter=0
        for each in arrfiles:
            try:
                with open(each, mode='r', encoding="utf-8") as readfile:

                    line_count=0
                    for line in readfile:
                        writefile.write(struct_first_line(line_count,line))
                        line_count+=1
                        # print(line_count)
                    print(dict_all_values_in_a_file)
                    file_counter += 1 #ERROR?
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