import sys
import os
from scipy.optimize import curve_fit
from scipy.ndimage import rotate
from scipy.integrate import simpson
 
# # getting the name of the directory
# # where the this file is present.
# current = os.path.dirname(os.path.realpath(__file__))
 
# # Getting the parent directory name
# # where the current directory is present.
# parent = os.path.dirname(current)
 
# # adding the parent directory to
# # the sys.path.
# sys.path.append(parent)
 
# # now we can import the module in the parent
# # directory.
from ImageAnalysis import ImageAnalysisCode
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.close('all')

####################################
#Set the date and the folder name
####################################
date = '11/12/2024'
data_path =r"D:\Dropbox (Lehigh University)\Sommer Lab Shared\Data"

data_folder = r'/FLIR/Focus top cam'

# plt.rcParams['image.interpolation'] = 'nearest'


####################################
#Parameter Setting
####################################
examNum = 6 #The number of runs to exam.
examFrom = None #Set to None if you want to check the last several runs. 
do_plot = True

showTimestamp = True
variablesToDisplay = None
variablesToDisplay = [
    'wait',
    # 'ODT Position',
    # 'ZSBiasCurrent',
    # 'VerticalBiasCurrent',
    # 'CamBiasCurrent'
    ]
# variablesToDisplay = ['wait','cMOT coil', 'ZSBiasCurrent', 'VerticalBiasCurrent', 'CamBiasCurrent']

variableFilterList = None
variableFilterList = [
    # 'wait==3', 
    # 'VerticalBiasCurrent==9.5',
    # 'ZSBiasCurrent==5.5'
    ] # NO SPACE around the operator!


# rowstart = 80
# rowend = 225
# columnstart = 130
# columnend = 320

rowstart = 1
rowend = -1
columnstart = 1
columnend = -1

binsize=1

centerx = 165 * binsize
centery = 80 * binsize
radius = 300

####################################
####################################

dataLocation = ImageAnalysisCode.GetDataLocation(date, DataPath=data_path)
data_folder = dataLocation + data_folder
variableLog_folder = dataLocation + r'/Variable Logs'
examFrom, examUntil = ImageAnalysisCode.GetExamRange(examNum, examFrom)
    
# data_folder =  './FLIR/odt align'
t_exp = 10e-6
picturesPerIteration = 3
# t0 = 40e-6



params = ImageAnalysisCode.ExperimentParams(date, t_exp = t_exp, picturesPerIteration= picturesPerIteration, cam_type = "chameleon")
images_array, fileTime = ImageAnalysisCode.loadSeriesPGM(picturesPerIteration=picturesPerIteration, data_folder = data_folder, 
                                               binsize=binsize, file_encoding = 'binary', 
                                               examFrom=examFrom, examUntil=examUntil, return_fileTime=1)

variableLog = ImageAnalysisCode.LoadVariableLog(variableLog_folder)
logTime = ImageAnalysisCode.Filetime2Logtime(fileTime, variableLog)


if variableFilterList:        
    filterList = ImageAnalysisCode.VariableFilter(logTime, variableLog, variableFilterList)
    images_array = np.delete(images_array, filterList, 0)
    logTime = list(np.delete(logTime, filterList, 0))

ImageAnalysisCode.ShowImagesTranspose(images_array, logTime, variableLog, 
                                      variablesToDisplay, showTimestamp=showTimestamp)



Number_of_atoms, N_abs, ratio_array, columnDensities, deltaX, deltaY = ImageAnalysisCode.absImagingSimple(images_array, 
                                                                                                          params=params,
                firstFrame=0, correctionFactorInput=1, rowstart = rowstart, rowend = rowend, columnstart = columnstart,
                columnend = columnend, subtract_burntin=0, preventNAN_and_INF=True)


plt.figure()
plt.imshow(ratio_array[0], vmin = 0, cmap = 'gray') #vmax = 1.5
plt.colorbar()
plt.show()

angle_deg= 40 #rotates ccw

fitVals = []

for count, img in enumerate(columnDensities):
    
    sutter_widthx, sutter_center_x, sutter_widthy, sutter_center_y = ImageAnalysisCode.fitgaussian(images_array[count, 1], 
                                                                                                   title='shutter fitting', do_plot=0)
   
    masked, vmax = ImageAnalysisCode.CircularMask(columnDensities[count], centerx=sutter_center_x, centery=sutter_center_y,
                                                      radius=radius/binsize)
    
    _, Xcenter, _, Ycenter = ImageAnalysisCode.fitgaussian(columnDensities[count], title = "Vertical Column Density",
                                                                        vmax = vmax, do_plot = 0, save_column_density=0,
                                                                        column_density_xylim=(columnstart, columnend, rowstart, rowend),
                                                                        count=count, logTime=logTime, variableLog=variableLog, 
                                                                        variablesToDisplay=variablesToDisplay, showTimestamp=True)
    
    
    rotatedCD = rotate(columnDensities[count][rowstart:rowend,columnstart:columnend], angle_deg, reshape = False)

    Xwidth, _, Ywidth, _ = ImageAnalysisCode.fitgaussian(rotatedCD, title = "Vertical Column Density",
                                                                        vmax = vmax, do_plot = 1, save_column_density=0,
                                                                        column_density_xylim=(columnstart, columnend, rowstart, rowend),
                                                                        count=count, logTime=logTime, variableLog=variableLog, 
                                                                        variablesToDisplay=variablesToDisplay, showTimestamp=True)
    
    row = {
        'Xwidth': Xwidth,
        'Ywidth': Ywidth,
        'Xcenter': Xcenter,
        'Ycenter': Ycenter
    }
    
    fitVals.append(row)


    print("Number of atoms:{}e6".format(round(Number_of_atoms[count]/(1e6))))


df_temp = pd.DataFrame(fitVals)
df_temp['atomNum'] = Number_of_atoms

var2append = variableLog[ variableLog.index.isin(logTime) ].reset_index()


df = pd.concat([df_temp, var2append], axis=1)
df = df.set_index('time')

#%%

# plt.figure()
# plt.errorbar(df['wait'])



#%%
'''
ImageAnalysisCode.imageFreqOptimization(np.loadtxt(data_folder+"/imgfreq.txt"), Number_of_atoms, ratio_array)
plt.imshow(ratio_array[0][rowstart:rowend,columnstart:columnend],vmin=0,vmax=1.2,cmap="gray")
densityvsrow = np.sum(n2d[0][rowstart:rowend,columnstart:columnend], 1)
print("densityvsrow = "+str(np.shape(densityvsrow)))
plt.figure(figsize=(4,3))
plt.plot(densityvsrow)
'''

def gaussianBeam(x, amp, center, w, offset, slope):
    return offset + amp*np.exp(-2*(x-center)**2/w**2) + slope*x


def fitgaussian(xdata, ydata, do_plot=True):
    popt, pcov = curve_fit(gaussianBeam, xdata, ydata,p0=[3e9, 670, 10, 5e9, 3e7])
    #print(popt)
    if (do_plot):
        plt.plot(xdata,ydata)
        plt.plot(xdata,gaussianBeam(xdata, *popt))
        plt.title("amplitude = {:.2e}".format(popt[0]))
        plt.ylabel("1D atomic density arb units")
        plt.xlabel("vertical row index")
        plt.tight_layout()
        # plt.savefig("atom count plot.png", dpi = 600)
    return popt,pcov

'''
#odt-specific code below
angle_deg= 0 #rotates ccw
rotated_columnDensities = rotate(columnDensities[0][rowstart:rowend,columnstart:columnend], angle_deg, reshape = False)
plt.imshow(rotated_columnDensities)
plt.colorbar()
densityvsrow = np.sum(rotated_columnDensities, 1)*deltaY
print("densityvsrow = "+str(np.shape(densityvsrow)))
plt.figure(figsize=(4,3))
plt.plot(densityvsrow)

nstart = 659
nstop = 685
xvalues = np.arange(nstart, nstop)
popt, pcov = fitgaussian(xvalues, densityvsrow[nstart:nstop], do_plot = 1)
odt_fit = gaussianBeam(xvalues, popt[0], popt[1], popt[2], popt[3], popt[4])-popt[4]*xvalues
num_atoms = simpson(odt_fit, xvalues)*deltaX
print("Number of atoms in ODT: {}e6".format(num_atoms/(1e6)))
plt.show()  
'''