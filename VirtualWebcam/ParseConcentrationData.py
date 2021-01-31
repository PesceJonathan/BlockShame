# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 21:36:46 2021

@author: jonat
"""
import pandas as pd
import datetime
import csv

def getConcentrateData():
    # def parseData(): 
    data = pd.read_csv('./Data/ConcentrationDataV2.csv')
    df = pd.DataFrame([[None, '2021-01-30 23:03:42.669845']], columns=['StartTime', 'EndTime'])
    data = data.append(df, ignore_index=True)
    
    def parseDate(value):  
        if (pd.isna(value) == False):
            return datetime.datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S.%f')
        
        return None
    
    # Parse the strings to datetimes
    data['StartTime'] = data['StartTime'].apply(parseDate)
    data['EndTime'] = data['EndTime'].apply(parseDate)
    
    # Get the start and end time
    startTime = data[0:1]['StartTime'][0]
    endTime = data[len(data)-1:len(data)]['EndTime'][len(data)-1]
    data = data[1:len(data) - 1]
    
    intervalTimes = (endTime - startTime)/6
    
    data = data.values
    
    zeroTime = startTime - startTime
    
    startInterval = startTime
    endInterval = startInterval + intervalTimes
    timeNotConcentrated = zeroTime
    concentrateData = []
    
    for time in data:
        startTime = time[0]
        endTime = time[1]
        
        while True:
            if (startTime > endInterval):
                concentrateData.append(timeNotConcentrated)
                timeNotConcentrated = zeroTime
                endInterval += intervalTimes
                continue
            
            if (endTime <= endInterval):
                timeNotConcentrated += (endTime - startTime)
                break
            
            timeNotConcentrated += (endInterval - startTime)
            concentrateData.append(timeNotConcentrated)
            timeNotConcentrated = zeroTime
            startTime = endInterval
            endInterval = endInterval + intervalTimes
            
    if (len(concentrateData) < 5):
        concentrateData.append(timeNotConcentrated)
        
    for num in range(5 - len(concentrateData)):
        concentrateData.append(zeroTime)
        
    finalData = []
    
    for time in concentrateData:
        finalData.append(100 - (time/intervalTimes) * 100)
        
    return finalData


data = getConcentrateData()
with open("./Data/ConcentrateArray.csv","w+", newline='') as file:
    csvWriter = csv.writer(file, delimiter=',')
    csvWriter.writerow(data)