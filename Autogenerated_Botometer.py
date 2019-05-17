# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 12:55:05 2019

@author: Naman
"""

import re 
import pandas as pd
  
# Function to match the string 
def match(text): 
          
        # regex 
        pattern='\d.*[A-Z]|[A-Z].*\d'  #regulare exp for checking if the username has atleast 1 lower,upper and one number
        # searching pattern 
        if re.search(pattern, text): 
                return('Yes') 
        else: 
                return('No') 
  
# Driver Function 



test = pd.read_csv(r'C:\Users\Naman\Desktop\Bank of America\3MCutJobs.csv')

my_listSource=test['source'].values

c1=0
my_lists=[]
for i in my_listSource:   #take array with ifttt as source
    if(i=='IFTTT'):
        my_lists.append(i)
        c1=c1+1
        
dataS= test[test['source'].isin(my_lists)]  #data with source IFTTT

# checking all the condtions if source is IFTTT::: Username contains atleat 1 lower upper and numeric 
#AND username is of lenght 15
# AND Location is not null AND Followers is atleast 10 If all conditions are satfified ITS A BOT
#import pandas as pd
myList_bots=[]
myList_Nbots=[]
for index,rows in dataS.iterrows():
    #print(rows['Author'])
    r1= match(rows['Author'])
    if(r1=='Yes' and len(rows['Author'])==15 and rows['Twitter.Followers']<10 and pd.isnull(rows['user_location'])):
        myList_bots.append(rows['Author'])
    else:
        myList_Nbots.append(rows['Author'])
        #print(rows['Author'])
    

dataFinal= dataS[dataS['Author'].isin(myList_Nbots)] #taking list with genuine values  

test=test[test['source'].values !='IFTTT'] #deleting data with source ifttt. We will append it again with genuie values.

dataFinalized=pd.concat([test, dataFinal], ignore_index=True) #final dataframe #concating both test(without IFTTT) and dataFinal(only genuine IFTTT)

#dataFinalized.to_csv(r'C:\Users\Naman\Desktop\Bank of America\at_tp.csv', encoding='utf-8', index=False)


#-----------------------------------
#We will put dataFinalized or final output to botometer check where followers are less than 300

import botometer

mashape_key = "ec7358768fmsh96890135304d634p13b0a9jsna206304e9fea"
twitter_app_auth = {
    'consumer_key': 'ck186Ovisd90UwoJk2xBxaCWh',
    'consumer_secret': 'k0f9167YEZM19td2W2ME18Bl859ZSgFjGxuz73aJQSaKrgl3Kz',
    'access_token': '975529263632912389-gOv572De8VjVW27PaQ9heD6okF1ZHOK',
    'access_token_secret': '9JDKZVjpC7CsAkNxZdPQWxOC3Qv19sHcizOzFTblYo6jB',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          mashape_key=mashape_key,
                          **twitter_app_auth)


my_list=dataFinalized['Author'].values

count1=0
for i in my_list:
    count1=count1+1
print(count1)
print('dataFinnalized')
    
#my_list = list(set(my_list))  #taking the disctinct user names only

#Selecting values for botometer wrt Number of Followers: Currently keeping number of follower check as less than 300
list_followersC=[]
for index, rows in dataFinalized.iterrows():
    if(rows['Twitter.Followers']<10):
        list_followersC.append(rows['Author'])
    

adict ={}  
# this step will take lot of time bcoz its calling the botometer for each id

count=0
for screen_name, result in bom.check_accounts_in(list_followersC):
    #print(result)
    adict[screen_name] =result
    count=count+1
    print(count)
    # Do stuff with `screen_name` and `result`
    
import numpy as np

resultdict={}
for keys,values in adict.items():
    try:
        resultdict[keys]= values['display_scores']['english']
        #print(keys,resultdict[keys])
    except:
        resultdict[keys] = np.nan
        #print(keys,resultdict[keys])


res={}
unclean={}  #it will keep data whose value of botometer is greater than 4.3
for i in resultdict:
    if(resultdict[i]< 4.3  ):
        
        res[i]=resultdict[i]
        
    else:
        unclean[i]=resultdict[i]

testt=dataFinalized[dataFinalized['Twitter.Followers'].values> 10] # removing value from mai data frame whose follower is less than specified
#testt.to_csv(r'C:\Users\Naman\Desktop\Bank of America\testt.csv', encoding='utf-8', index=False)

dataClean=dataFinalized[dataFinalized['Author'].isin(res)]
#dataClean.to_csv(r'C:\Users\Naman\Desktop\Bank of America\dataClean.csv', encoding='utf-8', index=False)

dataUseful=pd.concat([testt, dataClean], ignore_index=True) 

dataUseful.to_csv(r'C:\Users\Naman\Desktop\Bank of America\3MCutJobsCleanToday.csv', encoding='utf-8', index=False)
