#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 09:44:27 2022

this script is checking proxies from https://free-proxy-list.net/
if they work they will get stored in a csv file with all providen informations so that they can be used in further scripts


@author: kbstn
"""
import requests
import pandas as pd 
from proxy_checker import ProxyChecker

# get a list of free proxies

resp = requests.get('https://free-proxy-list.net/') 

# read the list from html page
df = pd.read_html(resp.text)[0]

# transorm http info yes or no into https or http
df['http']= df.Https.map(lambda x: 'https' if x == 'yes' else 'http')

#build the proper connection string 
df['connection']=df['IP Address'].map(str)+':'+df.Port.map(str)
df['connection_all']=df['http'].map(str)+'://'+df['IP Address'].map(str)+':'+df.Port.map(str)


# proxy = pd.Series(df.connection.values,index=df.http)

# create a list containing all ip adresses and ports of the proxies
proxylist= df.connection.tolist()

# ProxyChecker will return information as dictionary, we create a empty one to fill it with results
working_proxies ={}
for count,proxy in enumerate(proxylist):
    
      #Get a proxy from the pool
      
      print("Request "+str(count)+'/'+str(len(proxylist))+' --> checking '+ proxy)

    
      checker = ProxyChecker()
      # check proxy
      check=checker.check_proxy(proxy)
      
      if check == False:
          print(proxy+' not working')
      else:
          working_proxies[proxy] = check
          print(' --> working proxy, details: '+str(check))
          
# create a dataframe with the results
result= pd.DataFrame(working_proxies).T.reset_index()

# save working proxies as csv
result.to_csv('working_proxies.csv')

