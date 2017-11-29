from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
import numpy as np
import os

# set the directory with the ODB databases
wdr = "C:\Users\David\Documents\NEO_Data\PaperB"

os.chdir(r"%s" %wdr)

# function for open te database
def odbOpen(odbName):
    o1 = session.openOdb(    name=odbName+'.odb')
    session.viewports['Viewport: 1'].setValues(displayedObject=o1)
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(    CONTOURS_ON_DEF, ))
    return odbName

# function for close the database
def odbClose(odbName):
    closeOdb = session.odbs[odbName+'.odb'].close(    )
    return closeOdb

# function for displacement and force components extraction
def extractDF(odbName,curveName):
    odb = session.odbs[odbName+'.odb']
    session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('RF', 
        NODAL, ((COMPONENT, 'RF3'), )), ('U', NODAL, ((COMPONENT, 'U3'), )), ), 
        nodeSets=('REFERENCE_POINT_        2', 'REFERENCE_POINT_        1', ))
    xy1 = session.xyDataObjects['U:U3 PI: ASSEMBLY N: 2']
    xy2 = session.xyDataObjects['RF:RF3 PI: ASSEMBLY N: 1']
    xy3 = combine(-xy1, xy2/1000)
    xy3.setValues(
        sourceDescription='combine(-"U:U3 PI: ASSEMBLY N: 2","RF:RF3 PI: ASSEMBLY N: 1"/1000)')
    tmpName = xy3.name
    session.xyDataObjects.changeKey(tmpName, "%s" %curveName)
    del session.xyDataObjects['RF:RF3 PI: ASSEMBLY N: 1']
    del session.xyDataObjects['RF:RF3 PI: ASSEMBLY N: 2']
    del session.xyDataObjects['U:U3 PI: ASSEMBLY N: 1']
    del session.xyDataObjects['U:U3 PI: ASSEMBLY N: 2']
    return curveName

# Extracting the necessary data from ODB simulations-database
data = np.array(["LD10-DT25-K0","LD10-DT25-K25","LD10-DT25-K50","LD10-DT25-K75","LD10-DT25-K100"])

for i in range(0,len(data),1):
    odbOpen("J-"+data[i]+"-FD")
    extractDF("J-"+data[i]+"-FD",data[i])
    odbClose("J-"+data[i]+"-FD")

# routine to export the extracted data
x0 = session.xyDataObjects['LD10-DT25-K0']
x1 = session.xyDataObjects['LD10-DT25-K25']
x2 = session.xyDataObjects['LD10-DT25-K50']
x3 = session.xyDataObjects['LD10-DT25-K75']
x4 = session.xyDataObjects['LD10-DT25-K100']
session.xyReportOptions.setValues(interpolation=ON)
session.writeXYReport(fileName='abaqus.rpt', xyData=(x0, x1, x2, x3, x4))

