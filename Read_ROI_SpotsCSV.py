from ij import IJ
import csv
from ij import WindowManager
from ij.plugin.frame import RoiManager
from ij.gui import Roi
from ij.process import ImageStatistics as IS
from ij.measure import ResultsTable


'''
Requires a Stack 
Tracking is done using trackmate
The sports are exported to a csv file
Selected ROI is then exported to IJ roi manager in the actions page

CLICK ON THE IMAGE BEFORE RUNNING THE CODE
'''


#	method for trackmates spots csv file
csvimportbool=False
csvfilename = 'C:/Raju/Trackmate/3900.csv'


def TrackmateCSVimport(csvfilename):
	data=[] #Contains the spot information in the form of one spot per dictionary
	with open(csvfilename) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			data.append(row) # Each row corresponds to the quantified information of one spot
	return data

def getSpotTrackmateData(spot,data):	
	# This looks for a match with the spot name in the csv file and roi manager
	# The corresonding index is then used to copy information to results table
	spotindex = next((index for (index, d) in enumerate(data) if d["LABEL"] == spot), None)
	if (spotindex != None):
	    rt.addValue("TRACK_ID",data[spotindex]['TRACK_ID'])
	    rt.addValue("QUALITY",float(data[spotindex]['QUALITY']))
	    rt.addValue("MEAN INTENSITY",float(data[spotindex]['MEAN_INTENSITY_CH1']))
	    rt.addValue("MEDIAN INTENSITY",float(data[spotindex]['MEDIAN_INTENSITY_CH1']))
	    rt.addValue("MIN INTENSITY",float(data[spotindex]['MIN_INTENSITY_CH1']))
	    rt.addValue("MAX INTENSITY",float(data[spotindex]['MAX_INTENSITY_CH1']))
	    rt.addValue("TOTAL INTENSITY",float(data[spotindex]['TOTAL_INTENSITY_CH1']))
	    rt.addValue("STD INTENSITY",float(data[spotindex]['STD_INTENSITY_CH1']))
	    rt.addValue("ELLIPSE X0",float(data[spotindex]['ELLIPSE_X0']))
	    rt.addValue("ELLIPSE Y0",float(data[spotindex]['ELLIPSE_Y0']))
	    rt.addValue("ELLIPSE MAJOR",float(data[spotindex]['ELLIPSE_MAJOR']))
	    rt.addValue("ELLIPSE MINOR",float(data[spotindex]['ELLIPSE_MINOR']))
	    rt.addValue("ELLIPSE THETA",float(data[spotindex]['ELLIPSE_THETA']))
	    rt.addValue("ELLIPSE ASPECT RATIO",float(data[spotindex]['ELLIPSE_ASPECTRATIO']))
	    rt.addValue("AREA",float(data[spotindex]['AREA']))
	    rt.addValue("PERIMETER",float(data[spotindex]['PERIMETER']))
	    #print(roi.getTPosition(),roi.getName())

		
'''
	The spots are stored as a list of dictionary in variable data
	data[index]['LABEL']) returns the spot id 
	The spot id is then searched for in the exported ROIs
	Everytime a match is found, the data is added to the results table
'''
# Assigns the currently opened image to imp
imp = WindowManager.getCurrentImage()

if csvimportbool:
	print "importing trackmate csv data"
	data=TrackmateCSVimport(csvfilename)
else:
	print "No trackmate CSV file"

# Opens / selects the roi manager
rm = RoiManager.getInstance()
if not rm:
    rm = RoiManager()
# calculates all available statistical information for spots in ROI    
options = IS.ALL_STATS 
count=rm.getCount()
# All roi's are stored as an array in rois
rois=rm.getRoisAsArray()
# An instance to invoke the imagej Results table
rt=ResultsTable()

for roi in rois:
	imp.setRoi(roi)
	name=roi.getName()
# If the csv import bool is True, then Z and T are interchanged during trackmate	
	if csvimportbool:
		Slice=roi.getTPosition()
	else:
		Slice=roi.getTPosition()
	IJ.setSlice(Slice)
	rt.incrementCounter() # Adds a row in Results table
	#rt.addValue adds a value corresponding to column name
	rt.addValue("Slice",Slice) 
	rt.addValue("Label",roi.getName())
	spot=roi.getName()
# If the csv import bool is True, then getSpotTrtackmateData method retrieves the spot information
	if csvimportbool:
		getSpotTrackmateData(spot,data)

	stats=imp.getStatistics(options)
	rt.addValue("xCOM",stats.xCenterOfMass)
	rt.addValue("yCOM",stats.yCenterOfMass)
	rt.addValue("xCentroid",stats.xCentroid)
	rt.addValue("yCentroid",stats.yCentroid)
'''
# To obtain the pixels within the roi	
	length= len(roi.getContainedPoints())
	xs=[]
	ys=[]
	value=[]
	for i in range(length):	
		xs.append(roi.getContainedPoints()[i].x)
		ys.append(roi.getContainedPoints()[i].y)
		value.append(imp.getProcessor().getPixelValue(xs[i],ys[i]) )

	print zip(xs,ys,value)		
'''

rt.sort("Slice")
length=rt.size()
print(r'Total number of frames in the roi are ',length)
rt.show("Spots on a given track as a function of frame number")
#rt.saveAs("C:\Raju\Trackmate\Single_Track_X_Y_COM_Centroid.csv")

