#-----------------------------------------------
#Reshape-Polygon-by-Polyline
#-----------------------------------------------

import shapefile
import math

# variables
path = "G:/Github/5uperReshape/test_file/"
polyline = "COASTLINE_clip.shp"
polygon = "COASTLINE_Polygon.shp"
new_polygon = "COASTLINE_Polygon_New.shp"

# load files
# polyline
pl = shapefile.Reader(path + polyline)
# polygon (to reshaped)
plg = shapefile.Editor(path + polygon)

pl_shapes = pl.shapes()         # returns a list of shape objects describing the geometry of each shape record
pl_size = len(pl_shapes)                # polyline numbers in pl

tolerance = 20


for s in range(0, pl_size):
        print(s, "{0:.2f}".format(s / pl_size * 100) + "%")             # print the working process
        s_pl = pl_shapes[s]             # for the polyline in pl
        pl_start = (s_pl.points[0][0], s_pl.points[0][1])               # for the start point (x, y) of  the polyline
        pl_end = (s_pl.points[-1][0], s_pl.points[-1][1])               # for the end point (x, y) of the polyline

        #test polyline is ring, todo list
        if pl_start != pl_end:          # do the works, except polyline is a ring
                s_plg = plg.shape(0)            # return shape record of polygon
                pl_start_closest = 0            # the number of start point of the polyline
                pl_end_closest = len(s_plg.points)              # the number of end point of the polyline
                pl_start_closest_distance = math.inf            # set distance as an infinity number, for the closest start point between polyline and polygon
                pl_end_closest_distance = math.inf               # set distance as an infinity number, for the closest end point between polyline and polygon

                
                s_plg_parts = s_plg.parts               # group collections of points into shapes for polygon, take first point of each part as index
                s_plg_parts2 = list(s_plg_parts[1:]) + [len(s_plg.points)]              

                partIndex = 0         
                partIndex2 = 0
                for i in range(0, len(s_plg_parts)):
                        for j in range(s_plg_parts[i], s_plg_parts2[i]): 
                                
                                distance_start = math.hypot(s_plg.points[j][0] - pl_start[0], s_plg.points[j][1] - pl_start[1])         # get the distance between each point(polygon) & start point(polyline)
                                distance_end = math.hypot(s_plg.points[j][0] - pl_end[0], s_plg.points[j][1] - pl_end[1])               # get the distance between each point(polygon) & end point(polyline)

                                if distance_start < pl_start_closest_distance and distance_start < tolerance:           # get the point in polygon with minimum distance to start point in polyline
                                        pl_start_closest = j            # record number of the closest point                                                                                                                     
                                        pl_start_closest_distance = distance_start
                                        partIndex = i + 1          

                                if distance_end < pl_end_closest_distance and distance_end < tolerance:         # get the point in polygon with minimum distance to end point in polyline
                                        pl_end_closest = j              # record number of the closest point
                                        pl_end_closest_distance = distance_end
                                        partIndex2 = i + 1


                if partIndex == partIndex2 and pl_start_closest_distance != math.inf and pl_end_closest_distance != math.inf:           # get the points in polygon, which are not in the range of  polyline
                        s_plg.points = s_plg.points[0:pl_start_closest] + s_pl.points + s_plg.points[pl_end_closest+1:]                 # insert the s_pl.point into s_plg.plg
                        partOffset = pl_end_closest - pl_start_closest + 1 - len(s_pl.points)                                                                                         
                        for i in range(partIndex, len(s_plg_parts)):            #
                                s_plg_parts[i] = s_plg_parts[i] - partOffset

plg.save(path + new_polygon)
