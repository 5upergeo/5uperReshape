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

pl_shapes = pl.shapes()
pl_size = len(pl_shapes)

tolerance = 20
# print(plg.shape(0).parts)
for s in range(0, pl_size):
        print(s, "{0:.2f}".format(s / pl_size * 100) + "%")
        s_pl = pl_shapes[s]
        pl_start = (s_pl.points[0][0], s_pl.points[0][1])
        pl_end = (s_pl.points[-1][0], s_pl.points[-1][1])

        #test polyline is ring, todo list
        if pl_start != pl_end:
                s_plg = plg.shape(0)
                pl_start_closest = 0
                pl_end_closest = len(s_plg.points)
                pl_start_closest_distance = math.inf
                pl_end_closest_distance = math.inf

                # print(s_plg.parts)
                s_plg_parts = s_plg.parts
                s_plg_parts2 = list(s_plg_parts[1:]) + [len(s_plg.points)]

                partIndex = 0
                partIndex2 = 0
                for i in range(0, len(s_plg_parts)):
                        # print(s_plg_parts[i])
                        for j in range(s_plg_parts[i], s_plg_parts2[i]):
                                # print(j)
                                distance_start = math.hypot(s_plg.points[j][0] - pl_start[0], s_plg.points[j][1] - pl_start[1])
                                distance_end = math.hypot(s_plg.points[j][0] - pl_end[0], s_plg.points[j][1] - pl_end[1])

                                if distance_start < pl_start_closest_distance and distance_start < tolerance:
                                        pl_start_closest = j
                                        pl_start_closest_distance = distance_start
                                        partIndex = i + 1

                                if distance_end < pl_end_closest_distance and distance_end < tolerance:
                                        pl_end_closest = j
                                        pl_end_closest_distance = distance_end
                                        partIndex2 = i + 1

                # print(pl_start_closest)
                # print(pl_end_closest)

                if partIndex == partIndex2 and pl_start_closest_distance != math.inf and pl_end_closest_distance != math.inf:
                        s_plg.points = s_plg.points[0:pl_start_closest] + s_pl.points + s_plg.points[pl_end_closest+1:]
                        partOffset = pl_end_closest - pl_start_closest + 1 - len(s_pl.points)
                        for i in range(partIndex, len(s_plg_parts)):
                                s_plg_parts[i] = s_plg_parts[i] - partOffset

plg.save(path + new_polygon)