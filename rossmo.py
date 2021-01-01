import point
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb 

#Grid Dimensions
nRows = 65
nCols = 50

#Known locations of committed crimes
crime_locations = [
    point.Point(3,53),
    point.Point(10,24),
    point.Point(30,10),
    point.Point(40,46),
    point.Point(45,29)
]

#Constants to be fiddled with to get alternate heatmaps
#buffer affects the size of the area around committed crimes that is unlikely
#to be where the serial criminal lives
#f affects how quickly the likelihood decays beyond the buffer zone
#g affects how quickly the likelihood decays within the buffer zone
buffer = 10
f = 2/3
g = 3/4

def main():
    aList = create_coord_list(nRows, nCols)
    aList = rossmo_list(aList)
    aTable = create_coord_table(aList)
    fig, ax = plt.subplots(figsize=(11, 9))
    sb.heatmap(aTable, cmap="icefire")
    ax.invert_yaxis()
    plt.show()

# Creates a list to store cell coordinate locations
def create_coord_list(nRows, nCols):
    aList = list()
    for y in range(nRows):
        for x in range(nCols):
            aList.append(point.Point(x,y))
    return aList

#Turns a list of cell coordinates into a table
def create_coord_table(aList):
    table = np.array(aList)
    table = table.reshape(nRows,nCols)
    table = pd.DataFrame(table)
    return table

#Given a list of crime locations and a cell location, returns an array of all
#distances from the crime
def crime_distance(cell, crime_locations):
    crime_distances = list()
    idx = 0
    for crime in crime_locations:
        crime_distances.append(cell.taxicab_distance(crime_locations[idx]))
        idx += 1
    return crime_distances

#Returns an individual summand of Rossmo's equation
def rossmo_summand(distance, buffer, f, g):
    if distance > buffer:
        return 1/distance**f
    else:
        return (buffer**(f-g))/(2*buffer-distance)**g

#Returns a likelihood for a cell using Rossmo's equation by summing over each
#crime scene location
def rossmo_prob(crime_distances):
    px = 0
    for i in range(len(crime_distances)):
        if rossmo_summand(crime_distances[i], buffer, f, g) == None:
            px += 0
        else:
            px += rossmo_summand(crime_distances[i], buffer, f, g)
    return px

#Given a list of cell coordinates, calculates likelihood for each cell
def rossmo_list(coords):
    aList = list()
    for coord in coords:
        crime_distances = crime_distance(coord, crime_locations)
        aList.append(rossmo_prob(crime_distances))
    return aList

main()