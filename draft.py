#-----------------------------------------------
#Reshape-Polygon-by-Polyline
#-----------------------------------------------

import shapefile

# variables
path = "FolderPath"
polyline = "COASTLINE.shp" 
polygon = "COASTLINE_Polygon.shp"

# load files
# polyline
pl = shapefile.Reader(path+polyline)
# polygon (to reshaped)
plg = shapefile.Reader(path+polygon)


# get x,y range for one section(490) in pl
s_pl = pl.shape(490)
maxx = s_pl.points[0][0]
maxy = s_pl.points[0][1]
minx = s_pl.points[0][0]
miny = s_pl.points[1][1]
for i in range(len(s_pl.points)):
        x = s_pl.points[i][0]
        y = s_pl.points[i][1]
        if x > maxx:
                maxx = x
        if minx > x:
                minx = x
        if y > maxy:
                maxy = y
        if miny > y:
                miny = y


# delete objID of points from polygon, in the range of maxx, minx, maxy, miny
s_plg = plg.shape(0)
for i in range(0,len(s_plg.points)):
        x = s_plg.points[i][0]
        y = s_plg.points[i][1]
        if x < maxx and x > minx and y < maxy and y > miny:
                print("Delete ID = " + str(i))
                del s_plg.points[i]


# append the pl points
s_plg.points.append(s_pl.points)
