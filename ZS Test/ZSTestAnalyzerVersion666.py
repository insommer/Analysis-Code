# -*- coding: utf-8 -*-
"""CSV import test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Wwf7-MVBJv5dWaykZijaYF4VxWUFioGu

Package Import
"""

import csv
# import itertools
import pandas as pd
#import plotly.express as px
import numpy as np 
#import kaleido
# import io
# from sklearn import preprocessing
#import plotly.graph_objects as go
# import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rcParams
#import matplotlib.patches as patches


# Reading an excel file using Python
import xlrd
#import xlwt
from xlutils.copy import copy

print("What is the scan number?")
scan = input()
n = int(scan)

#use this if you want to loop over multiple scans 
# scan_array = np.linspace(1, 26, 26).astype(int).astype(str)

#if you want to loop over the scans, indent everyting after the "for" statement
# for x in scan_array:
# scan = x
# n = int(x)
####################################################
############## Find TOPAS Data #####################
####################################################
#Adjust the font size on the plots
rcParams.update({'font.size': 12})
#Input csv file in formate "scanX.csv"
location = r"C:\Users\Sommer Lab\Documents\Data\2022\02 Feb 2022\22 Feb\scan"
filename = location+scan+".csv"
print("filename = "+str(filename))



####################################################
################ Find Run Data #####################
####################################################
loc = (r"C:\Users\Sommer Lab\Documents\Data\2022\02 Feb 2022\22 Feb\ZS_Test_Parameters_Feb_22.xls")
# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
#Pictures Taken According to Data Sheet
Pictures_Taken = int(sheet.cell_value(n, 1))
#Start Voltage According to Data Sheet
Start_Voltage = float(sheet.cell_value(n, 3))
#End Voltage According to Data Sheet
End_Voltage = float(sheet.cell_value(n, 4))
#AOM Frequency of the probe laser According to Data Sheet
AOM_Frequency = float(sheet.cell_value(n, 8))*2



####################################################
########### TOPAS PROCESSING VALUES ################
####################################################
df=[]
P2P_Voltage = 83.22096-82.76787
P2P_Freq = 228
Shift_Per_Volt = P2P_Freq / P2P_Voltage 
D2_Transition_um = 0.670977338
K = 1 / D2_Transition_um
####################################################
########### TOPAS PROCESSING VALUES ################
####################################################


####################################################
################# TOPAS Graphs #####################
####################################################
signals=[]
signals_min = []
voltages=[]
Red_Shift=[]
#Open the TOPAS csv data
with open(filename, 'r') as f:
  variableNames = f.readline().split(";")
  #print(variableNames)
  #for i in range(10):
  while f:
    for i in range(1000):
      f.readline() #speed through 1000 lines


    line = f.readline()
    if line:
      line=line.split(";")
      # example: '83.126656;0.208156;\n'
      # line = ['83.126656', '0.208156', '\n']
      signals.append(float(line[1]))
      signals_min.append(float(line[1]))
      voltages.append(float(line[0]))
      Red_Shift.append((float(line[0])-End_Voltage)*Shift_Per_Volt)
      min_y = min(signals_min)
      min_x = int(Red_Shift[signals_min.index(min_y)])
    else:
      break


####################################################
################ Trouble Shoot #####################
#################################################### 
#print("min(signals) = "+str(min(signals)))
#print("Red_Shift[signals.index(min_y)] = "+str(Red_Shift[signals.index(min_y)]))  
####################################################
################ Trouble Shoot #####################
#################################################### 


#################################################################
#######################!!!Frequency Shift!!!#####################
#################################################################
rb = xlrd.open_workbook(loc)
wb = copy(rb)
w_sheet = wb.get_sheet(0)
#correction frequency
w_sheet.write(n,12,AOM_Frequency-min_x+114)
# wb.save(loc)
The_Shift = int(AOM_Frequency+114-min_x)
#################################################################
#######################!!!Frequency Shift!!!#####################
#################################################################





#Adjust the font size on the plots
rcParams.update({'font.size': 12})

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
#Correction Frequency just written into sheet
Correction_Frequency = int(sheet.cell_value(n, 12))



####################################################
########### Adjusted TOPAS GRAPHS ##################
####################################################
signals=[]
signals_min = []
Half_Shift=[]
Three_Half_Shift=[]
Half_Velocity45=[]
Three_Half_Velocity45=[]
TESTER1=[]
TESTER2=[]
TESTER3=[]
TESTER4=[]
TESTER5=[]
#Open the TOPAS csv data
with open(filename, 'r') as f:
  variableNames = f.readline().split(";")
  #print(variableNames)
  #for i in range(10):
  while f:
    for i in range(1000):
      f.readline() #speed through 1000 lines


    line = f.readline()
    if line:
      line=line.split(";")
      signals.append(float(line[1]))
      signals_min.append(float(line[1]))
      TESTER1.append((float(line[0])-End_Voltage)*Shift_Per_Volt - int(min_x) )
      TESTER2.append((float(line[0])-End_Voltage)*Shift_Per_Volt - int(min_x) +160)
      TESTER3.append((float(line[0])-End_Voltage)*Shift_Per_Volt - int(min_x) +160 +114)
      TESTER4.append(((float(line[0])-End_Voltage)*Shift_Per_Volt - int(min_x) +160 +114)/(K)*2**(1/2))
      TESTER5.append(((float(line[0])-End_Voltage)*Shift_Per_Volt + The_Shift)/(K)*2**(1/2))
      Three_Half_Shift.append((float(line[0])-End_Voltage)*Shift_Per_Volt +  Correction_Frequency)
      #Half_Velocity45.append(((float(line[0])-End_Voltage)*Shift_Per_Volt + Correction_Frequency)/(K)*2**(1/2))
      Three_Half_Velocity45.append(((float(line[0])-End_Voltage)*Shift_Per_Volt +  int(Correction_Frequency))/(K)*2**(1/2))
      min_32y = min(signals_min)
      min_32x = int(Three_Half_Shift[signals_min.index(min_32y)])
      min_TESTER1x = int(TESTER1[signals_min.index(min_32y)])
      min_TESTER2x = int(TESTER2[signals_min.index(min_32y)])
      min_TESTER3x = int(TESTER3[signals_min.index(min_32y)])
      min_TESTER4x = int(TESTER4[signals_min.index(min_32y)])
      min_TESTER5x = int(TESTER5[signals_min.index(min_32y)])
    else:
      break
  

#################################################################
########################### Camera Settings #####################
#################################################################

num_frames = Pictures_Taken
filename = filename.split('.csv')[0]+"_counts.csv"
#Make the plot:
total_counts = np.zeros(num_frames)
with open(filename, "r") as f:
    reader = csv.reader(f, delimiter="\n")
    for i, row in enumerate(reader):
       total_counts[i] = row[0]
#    for i in range(num_frames):
#     im_temp = images[i,ymin:ymax,xmin:xmax]
#     intensity = np.sum(im_temp)
#     total_counts[i] = intensity

# plt.figure(3)
# plt.plot(total_counts)

Picture_Number = list(range(1,Pictures_Taken))

Adjusted_Counts = total_counts * 10**(-8) *0.5

temp = total_counts - min(total_counts)
Adjusted_Counts = temp/max(temp)


Detune_Map_to_3HalfV45_Map=[]
Detune_Map_to_3HalfV45_Map= [(((Start_Voltage + ((End_Voltage - Start_Voltage)/Pictures_Taken)*(i+1)) -End_Voltage)*Shift_Per_Volt+Correction_Frequency)/(K)*2**(1/2) for i in range(Pictures_Taken)] 


adjusted_signals = np.array(signals)-min(signals)
adjusted_signals = adjusted_signals/max(adjusted_signals)
###############################################################
###############################################################
###############################################################
plt.figure()
plt.title('scan'+str(scan))
plt.rcParams.update({'font.size':12})
plt.xlabel("Resonant Velocity (m/s)")
plt.ylabel("Normalized Data Count")
plt.plot(Detune_Map_to_3HalfV45_Map, Adjusted_Counts, label = '3/2 Transition Camera Count')
plt.plot(Three_Half_Velocity45, adjusted_signals, label = '3/2 Transition TOPAS Data')
plt.legend(loc = 'best')
plt.show()

velocity_array = -np.array(Detune_Map_to_3HalfV45_Map)
plt.figure(figsize = (8, 8))
plt.rcParams.update({'font.size':14})
plt.xlabel("Atom Velocity (m/s)")
plt.ylabel("Normalized Data Count")
plt.plot(velocity_array, Adjusted_Counts, label = '3/2 Transition Camera Count')
# plt.plot(Three_Half_Velocity45, adjusted_signals, label = '3/2 Transition TOPAS Data')
# plt.legend(loc = 'best')
plt.tight_layout()
plt.show()
plt.savefig("ZS test plot 02-22-2022 scan 22.png", dpi = 600)

# plt.savefig(location.split('scan')[0]+'\Graphs\scan'+str(scan)+'.png', dpi = 300)
###############################################################
###############################################################
###############################################################


print(pd.DataFrame(sheet.row_values(n), sheet.row_values(0)))



###############################################################
################ DIAGNOSTICS ##################################
###############################################################

"""
#pyplot plot
# ax, =  plt.figure()
plt.xlabel("Frequency MHz")
plt.ylabel("Adjusted Signal")
plt.plot(Red_Shift, signals, label = 'Un-adjusted')
plt.plot(Three_Half_Shift, signals, label = 'Adjusted')
plt.legend(loc = 'best')
plt.show()


plt.xlabel("Frequency MHz")
plt.ylabel("Adjusted Signal")
plt.plot(TESTER1, signals, label = 'TESTER1')
plt.plot(TESTER2, signals, label = 'TESTER2')
plt.plot(TESTER3, signals, label = 'TESTER3')
plt.plot(TESTER4, signals, label = 'TESTER4')
plt.plot(TESTER5, signals, label = 'TESTER5')
plt.legend(loc = 'best')
plt.show()


print(Correction_Frequency)
print(min_32x-min_x)
print()
print(min_TESTER1x)
print(min_TESTER2x)
print(min_TESTER3x)
print(min_TESTER4x)
print(AOM_Frequency)
# print(total_counts)
"""