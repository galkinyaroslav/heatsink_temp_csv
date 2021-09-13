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

# returns <class 'datetime.datetime'>
def get_file_time(m_line):
    m_newline = m_line.strip("\n") + ','
    m_newline = m_newline.replace('Сохранено: ', 'Дата,') # it can be deleted
    m_newline = m_newline.replace(' ', ',')
    m_newline = m_newline.replace(';', ',')
    m_newline = m_newline.replace('-', ',')
    m_newline = m_newline.replace(':', ',')
    m_newlinelist = m_newline.split(sep=',')
    curentfiledate = datetime(year=int(m_newlinelist[6]), month=int(m_newlinelist[5]), day=int(m_newlinelist[4]),
                              hour=int(m_newlinelist[1]), minute=int(m_newlinelist[2]), second=int(m_newlinelist[3]))
    print("curentfiledate")
    # print(type(curentfiledate))
    print(curentfiledate)
    return curentfiledate

def struct_first_line(m_line_count,m_line,m_timedelta):
    if m_line_count == 0:
        m_firstline = "Время,"+str(m_timedelta)+","

        print("4+++")
        print(m_firstline)
        return m_firstline
    else:
        dict_all_values_in_a_file_key = m_line[:m_line.find("-")]
        # print(dict_all_values_in_a_file_key)
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
        dict_all_values.update({m_timedelta:dict_all_values_in_a_file.copy()})
        return m_newline

def diff_dates(date1, date2):
    # date1 = datetime.strptime(d1, "%Y-%m-%d ")
    # date2 = datetime.strptime(d2, "%Y-%m-%d")
    if date1.year == 1 or date2.year == 1:
        return 0
    else:
        return abs(date2-date1).seconds
dict_all_values={}
dict_all_values_in_a_file={}
dict_unit_keys={"1.7V":0,
       "1.7W":0,
       "3.0V":0,
       "3.0W":0,
       "3.8V":0,
       "3.8W":0,
       "T1°C":0,
       "T2°C":0}

previousfiledate = datetime(year=int(1), month=int(1), day=int(1),
                            hour=int(0), minute=int(0), second=int(0))
print(previousfiledate)
timedelta=0
try:
    with open(csvfilename, mode='w', encoding="utf-8") as writefile:
        file_counter=0
        for each in arrfiles:
            try:
                with open(each, mode='r', encoding="utf-8") as readfile:
                    list_readfile=[]
                    list_readfile=list(readfile)
                    currentfiledate=get_file_time(list_readfile[0])
                    timedelta+=diff_dates(previousfiledate,currentfiledate)
                    print("timedelta")
                    print(type(timedelta))
                    print(timedelta)
                    line_count=0
                    for line in list_readfile:
                        writefile.write(struct_first_line(line_count,line,timedelta))
                        line_count+=1
                        # print(line_count)
                    # print(dict_all_values_in_a_file)
                    file_counter += 1 #ERROR?
                    writefile.write('\n')
                    previousfiledate=currentfiledate
            except IOError:
                print("'['1']'An IOError has occurred!")
except IOError:
    print("'['2']'An IOError has occurred!")
print("dict_all_values_in_a_file")
print(dict_all_values_in_a_file)

# print("dict_all_values")
# print(dict_all_values)

order_of_SAMPA="a1,a2,a3,b3,b2,b1,d3,e2,e1,d1,d2,c3,c2,c1,g1,g2,f3,e3,f2,f1,h1,h2,g3,i2,i1,j1,j2,h3,i3,k2,k1,j4,h5,g6,f7,e7,f6,g5,i4,g4,f5,h4,f4,e5,d6,c6,d5,e4,d4,c5,c4,a4,a5,a6,a7,b7,b6,b5,b4"
order_of_FPGA="a4,a5,a6,a7,b7,b6,b5,d4,c4,b4,f4,f5,e5,d6,e6,d7,c7,c6,c5,d5,e4,j4,h5,g6,f7,e7,f6,g5,g4,h4,i4,a1,a2,a3,b3,d2,d1,c1,c2,b2,b1,g3,g2,g1,f1,f2,f3,e3,d3,c3,e2,e1,k1,k2,i3,h3,h2,h1,i1,i2,j2,j1"
list_order_of_SAMPA=order_of_SAMPA.split(",")
list_order_of_FPGA=order_of_FPGA.split(",")


for time in dict_all_values[0]:
    str_off=""+str(dict_all_values[0][time])
    print(time)

# print(dict_all_values[0])
# print(dict_all_values[82])

# try:
#     with open(csvfilename, mode='r', encoding="utf-8") as csvreadfile:
#         with open("temperature.csv", mode='w', encoding="utf-8") as csvwritefile:
#             csv_reader = csv.reader(csvreadfile, delimiter=',')
#             line_count = 0
#             for row in csv_reader:
#                 if line_count == 0:
#                     val = 1
#                     strrow = 'Time,'
#                     for val in range(62):
#                         strrow += row[4 + 9 * val] + '-T1,'+row[4 + 9 * val]+'-T2,'
#                     print(strrow)
#                     csvwritefile.write(strrow + '\n')
#                     strrow = str(row[3]) + ','
#                     for val in range(62):
#                         # print(f'{row[10 + 9 * val]}<->{row[11 + 9 * val]}')
#                         strrow += row[11 + 9 * val] + ','
#                         strrow += row[12 + 9 * val] + ','
#                     print(strrow)
#                     csvwritefile.write(strrow + '\n')
#                     line_count += 1
#                 else:
#                     strrow = str(row[3])+','
#                     for val in range(62):
#                         strrow += row[11 + 9 * val] + ','
#                         strrow += row[12 + 9 * val] + ','
#                     print(strrow)
#                     csvwritefile.write(strrow + '\n')
#                     line_count += 1
# except IOError:
#     print("An IOError has occurred!")