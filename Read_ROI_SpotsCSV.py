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

'''

csvfilename = '3900.csv'

imp = WindowManager.getCurrentImage()
    # Add points to ROI manager
#print(imp.getStack())

'''
Reading the trackmate output file in csv format
'''

data=[] #Contains the spot information in the form of one spot per dictionary
with open(csvfilename) as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		data.append(row) # Each row corresponds to the quantified information of one spot

'''
	The spots are stored as a list of dictionary in variable data
	data[index]['LABEL']) returns the spot id 
	The spot id is then searched for in the exported ROIs
	Everytime a match is found, the data is added to the results table
'''

# Opens / selects the roi manager
rm = RoiManager.getInstance()
if not rm:
    rm = RoiManager()

options = IS.ALL_STATS 
# calculates all available statistical information for spots in ROI
count=rm.getCount()
# All roi's are stored as an array in rois
rois=rm.getRoisAsArray()
# An instance to invoke the imagej Results table
rt=ResultsTable()

for roi in rois:
	imp.setRoi(roi)
	stats=imp.getStatistics(options)
	rt.incrementCounter() # Adds a row in Results table
	#rt.addValue adds a value corresponding to column name
	rt.addValue("Slice",roi.getTPosition()) 
	rt.addValue("Label",roi.getName())
	spot=roi.getName()
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
	    print(roi.getTPosition(),roi.getName())
	
	rt.addValue("xCOM",stats.xCenterOfMass)
	rt.addValue("yCOM",stats.yCenterOfMass)
	rt.addValue("xCentroid",stats.xCentroid)
	rt.addValue("yCentroid",stats.yCentroid)
	#rt.addValue("Area",stats.area)
	#rt.addValue("Mean",stats.mean)
	#rt.addValue("Max",stats.max)
	#rt.addValue("Min",stats.min)
	#rt.addValue("xminor",stats.minor)
	#rt.addValue("xmajor",stats.major)

rt.sort("Slice")
length=rt.size()
print(r'Total number of frames in the roi are ',length)
rt.show("Spots on a given track as a function of frame number")
#rt.saveAs("C:\Raju\Trackmate\Single_Track_X_Y_COM_Centroid.csv")


'''
sliceno=rt.getColumn("Slice")
xcom=rt.getColumn("xCOM")
ycom=rt.getColumn("yCOM")
xcentroid=rt.getColumn("xCentroid")
ycentroid=rt.getColumn("yCentroid")


print(sliceno)
print(xcom)
print(ycom)
print(xcentroid)
print(ycentroid)

# plotting

from ij.gui import Plot


# title, X label, Y label
plot1 = Plot("xCOM_Centroid", "Framee_no", "X")

# Series 1
plot1.setColor("blue")
plot1.add("line", sliceno,xcom)

# Series 2
plot1.setColor("black")
plot1.add("line",sliceno,xcentroid)

plot1.addLegend("Center of Mass \t Centroid")


plot2 = Plot("yCOM_Centroid", "Framee_no", "Y")

# Series 1
plot2.setColor("blue")
plot2.add("line", sliceno,ycom)

# Series 2
plot2.setColor("black")
plot2.add("line",sliceno,ycentroid)
plot2.addLegend("Center of Mass \t Centroid")

plot1.show()
plot2.show()
'''