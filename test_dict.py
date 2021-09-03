
str1="a1-1.7V;0.0W;3.0V;0.0W;3.9V;0.0W;17.9°C;16.5°C"
str2="a2-1.6V;0.1W;3.1V;0.1W;3.8V;0.1W;17.8°C;16.4°C"
str3="a3-1.5V;0.2W;3.2V;0.2W;3.7V;0.2W;17.7°C;16.3°C"
strlist=[str1,str2,str3]
"""print(str1.find("-1.7V"))
print(str1[:str1.find("-1.7V")])
print(str1[str1.find("-1.7V")+1:len(str1)])"""
dict2={}
dict1={"1.7V":0,
       "1.7W":0,
       "3.0V":0,
       "3.0W":0,
       "3.8V":0,
       "3.8W":0,
       "T1°C":0,
       "T2°C":0}
for str_i in strlist:

       list1=(str_i[str_i.find("-")+1:len(str_i)]).split(";")
       dict2_key=str_i[:str_i.find("-")]
       """print(list1)"""

       counter=0
       for i in dict1.keys():
           """dict1[i]=list1[counter]"""
           dict1.update({i: list1[counter]})
           counter+=1

       dict2.update({dict2_key:dict1.copy()})
       print(dict2[dict2_key])
