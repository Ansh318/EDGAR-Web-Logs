##NAME:- ANSH AGARWAL

import csv
import sys
import pandas as pd
import netaddr
import time
import json
from zipfile import ZipFile
from io import TextIOWrapper
import itertools
import geopandas
from collections import defaultdict
import re,requests

def ip_search(ip,addr):
    output_dict = {}
    with open('ip2location.csv') as f:
        data = list(csv.reader(f))
        t1 = time.time()
        for row in data[1:]:
            if int(row[0]) <= ip <= int(row[1]): 
                t2 = time.time()
                output_dict['ip'] = addr
                output_dict['int_ip'] = ip
                output_dict['region'] = row[3]
                output_dict['ms'] = (t2 - t1) * 1000
        return output_dict

def ip_check(*arguments):
    dict_ls = list()
    ip_addr_ls = arguments[0]
    
    for idx in range(len(ip_addr_ls)):
        ip_addr = ip_addr_ls[idx]
        curr_ip_num = int(netaddr.IPAddress(ip_addr))
        #BASE CASE
        if idx == 0:
            dict_ls.append(ip_search(curr_ip_num,ip_addr))
        else:
            output_dict = {}
            prev_ip_num = int(netaddr.IPAddress(ip_addr_ls[idx - 1]))
            t1 = time.time()    
            if curr_ip_num - prev_ip_num == 1:
                t2 = time.time()
                output_dict['ip'] = ip_addr
                output_dict['int_ip'] = curr_ip_num
                output_dict['region'] = dict_ls[idx - 1]['region']
                output_dict['ms'] = (t2 - t1) * 1000
                dict_ls.append(output_dict)           
            else:
                dict_ls.append(ip_search(curr_ip_num,ip_addr))
    print(json.dumps(dict_ls))

def zip_csv_iter(name):
    with ZipFile(name) as zf:
        with zf.open(name.replace(".zip", ".csv")) as f:
            reader = csv.reader(TextIOWrapper(f))
            for row in reader:
                yield row
                
def ip_cleaner(row, ip_idx = 0):
    return int(netaddr.IPAddress(row[ip_idx][:-3] + "000"))

def sample(input_zip,output_zip,stride):
    
    row_list = []
    reader = zip_csv_iter(input_zip)
    header = next(reader)
    header.append('region')
    ip_idx = header.index('ip')
    
    sampler = list(itertools.islice(reader, 0, None, int(stride)))
    
    for row in sampler:
        ip_addr_str = row[ip_idx][:len(row[ip_idx]) - 3] + "000"
        ip_num = ip_cleaner(row)
        ip_dict = ip_search(ip_num,ip_addr_str)
        row.append(ip_dict['region'])
        row_list.append(row)
    row_list.sort(key = ip_cleaner)
    
    with ZipFile(output_zip, "w") as zf:
        with zf.open(output_zip.replace(".zip",".csv"), "w") as raw:
            with TextIOWrapper(raw) as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow(header) 
                for row in row_list:
                    writer.writerow(row)    
                    
                    
def world(file, svg_name):
   
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    world.set_index("name", drop=False, inplace=True)
    world = world[(world.name!="Antarctica")]
   
    reader = zip_csv_iter(file)
    header = next(reader)
    cidx = header.index("region")
    counts = defaultdict(int)
    for row in reader:
        counts[row[cidx]] += 1

    world["color"] = "purple"

    for country, count in counts.items():

        if not country in world.index:
            continue

        if count == 1:
            color = "blue"
        if count >= 2:
            color = "red"    
        if count >= 5:
            color = "pink"
        if count >= 10:
            color = "orange"
        if count >= 100:
            color = "yellow"
        world.at[country, "color"] = color

    ax = world.plot(color=world["color"], legend=True, figsize=(16, 4))
    ax.figure.savefig(svg_name, bbox_inches="tight")
    
    
def phone(file_name):
    num_list = []
    req_str = ""
    with ZipFile(file_name) as zf:
        for file_name in zf.namelist():
            with zf.open(file_name, "r") as f:
                tio = TextIOWrapper(f)
                string_1 = tio.read()
                req_str += string_1
        num = re.findall(r"\d{3}-\d{3}-\d{4}",req_str)
        num2 = re.findall(r"\(.*?\)\s\d{3}-\d{4}", req_str)
        num3 = re.findall(r"\(.*?\)\d{3}-\d{4}", req_str)
        num_list = list(set(num + num2 + num3))
        
    for phone_num in num_list:
        print(phone_num)
        
def main():
    if len(sys.argv) < 2:
        print("usage: main.py <command> args...")
    elif sys.argv[1] == "ip_check":
        ips = sys.argv[2:]
        ip_check(ips)
    elif sys.argv[1] == "sample":
        zip1 = sys.argv[2]
        zip2 = sys.argv[3]
        stride = sys.argv[4]
        sample(zip1,zip2,stride)
    elif sys.argv[1] == "world":
        file = sys.argv[2]
        svg_name = sys.argv[3]    
        world(file, svg_name)
    elif sys.argv[1] == "phone":
        file_name = sys.argv[2]
        phone(file_name)
    
if __name__ == '__main__':
     main()