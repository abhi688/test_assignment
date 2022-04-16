
import xml.dom.minidom as md
from datetime import date,timedelta,datetime
import pytz
from pytz import timezone
import json
import csv
timeStamp=0
label=2
responseCode=3
responseMessage=4
failureMessage=8


#Question-1
# Create a python method that takes arguments int X and int Y,
# and updates DEPART and RETURN fields
# in test_payload1.xml:

def replace_xml_values(x,y):
    depart_value= str(date.today()+timedelta(days=x)).replace("-","")
    return_value= str(date.today()+timedelta(days=y)).replace("-","")
    file = md.parse( "test_payload1.xml" )
    file.getElementsByTagName("DEPART")[0].firstChild.nodeValue = depart_value
    file.getElementsByTagName("RETURN")[0].firstChild.nodeValue = return_value

    with open( "modifed_xml.xml", "w" ) as fs: 
        fs.write( file.toxml() )
        fs.close()
    print(f"Depart, Return Value modified and saved to modified_xml.xml")

# 2. Create a python method that takes a json element
# as an argument, and removes that element from test_payload.json.
def recurse_json(data,json_element):
    for ele in data:
        if ele == json_element:
            del data[ele]
            break
        elif type(data[ele]) == dict:
            recurse_json(data[ele],json_element)

def remove_json(json_element):
    jdata = json.load(open("test_payload.json"))
    recurse_json(jdata,json_element)
    with open("modified_json.json", 'w') as f:
        json.dump(jdata, f, indent=4)
        print(f"Removed {json_element} and modified to file modified_json.json")

# 3. Create a python script that parses jmeter log files in CSV format,
# and in the case if there are any non-successful endpoint responses recorded in the log,
# prints out the label, response code, response message, failure message,
# and the time of non-200 response in human-readable format in PST timezone
# (e.g. 2021-02-09 06:02:55 PST).

def jmeter_read_logs(jmeter_file):
    with open(jmeter_file) as jmeter_test:
        csv_reader = csv.reader(jmeter_test)
        next(csv_reader)
        data=list(csv_reader)
        # print(data)
        for d in data:
            if d[responseCode] != str(200):
                date_format='%Y-%m-%d %H:%M:%S %Z'
                date = datetime.fromtimestamp(int(d[timeStamp])/1e3,tz=pytz.utc)
                date = date.astimezone(timezone('US/Pacific'))
                print('Label =',d[label])
                print('Local date & time is  =', date.strftime(date_format))
                print("Response Code =" , d[responseCode])
                print("Response Message =",d[responseMessage])
                print("Failure Message =", d[failureMessage])
                print("###################")

# Tests
# Question-1
replace_xml_values(1,10)


#Question - 2
#non -nested
remove_json('outParams')
print("-----")

#nested
remove_json('appdate')
print("-----")

#Question - 3
#jmete log1
jmeter_read_logs('Jmeter_log1.jtl')
print("-----")


