import csv
import pandas as pd
import mysql.connector

from datetime import datetime
import re
import sys

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="somedb"
)

mycursor = mydb.cursor()

# User inputs
fname = r'C:\Users\Downloads\some.csv'
tail_len = 12

# The two steps in the description
n_rows = sum(1 for row in open(fname, 'r'))
df = pd.read_csv(fname, skiprows=range(0, n_rows - tail_len))

print(df)
df.to_csv("new_csv.csv",index=False)


#to store final json list
result = []

#declare json variables
right_temp = 0
left_temp = 0
gas_flow = 0


with open('new_csv.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        
        print(row)
                        
        if(row[1] == ' Left Temperature'):
             left_temp =  row[2] 
             
        if(row[1] == ' Right Temperature'):
             right_temp =  row[2]
             
        if(row[1] == ' Gas Flow'):
             gas_flow =  row[2] 
        
        if( (left_temp != 0) and (right_temp != 0) and (gas_flow != 0)):
            
            time_stamp_value =  str(row[0]) 
            
            #convert time to mysql date time format
          
            time_stamp_value_removed_am_pm = re.sub(r'[^0-9, :-]+', '',time_stamp_value) 
            time_and_date = [i for j in time_stamp_value_removed_am_pm.split() for i in (j, ' ')][:-1]
            g_date = time_and_date[0]
            g_time = time_and_date[2]
            new_date =  datetime.strptime(str(g_date), '%d-%m-%Y').strftime('%Y-%m-%d')
            final_concat_date_time = new_date + ' ' + str(g_time)
            
            # print(g_date)
            # print(new_date)
            # print(g_time)
            # print(final_concat_date_time)
            
            my_dict = [ { "time_stamp_data" : final_concat_date_time , "left_temp" : str(left_temp) , "right_temp" : str(right_temp) , "gas_flow" : str(gas_flow ) } ]   
                 
            result.append(my_dict)
            
#print(result)

#remove all duplicateds values
new_list = []
for one_student_choice in result:
    if one_student_choice not in new_list:
        new_list.append(one_student_choice)
        


print(new_list)

#loop through and insert into mysql
for data_sets in new_list:
    formatted_dict_values = str(data_sets).replace('[','').replace(']','')
    new_ff = formatted_dict_values.replace("'", '"')
    
    #convert string dict to actual dict format
    time_stamp_v = eval(new_ff)
    
    #print(time_stamp_v)
    # print(time_stamp_v['time_stamp_data'])
    # print(time_stamp_v['left_temp'])
    # print(time_stamp_v['right_temp'])
    # print(time_stamp_v['gas_flow'])
    
    # sql = "INSERT INTO device_data_inc (inc_name, left_temp, right_temp, gas_flow, time_stamp) VALUES (%s, %s, %s, %s, %s)"
    # val = ("device_name", time_stamp_v['left_temp'],time_stamp_v['right_temp'],time_stamp_v['gas_flow'], time_stamp_v['time_stamp_data'])
    
    # mycursor.execute(sql, val)

    print({ time_stamp_v['time_stamp_data'] ,  time_stamp_v['left_temp'] , time_stamp_v['right_temp'] , time_stamp_v['gas_flow'] })

    # mydb.commit()

    # print(mycursor.rowcount, "record inserted.")
    
sys.exit(0)
