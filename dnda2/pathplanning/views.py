from django.shortcuts import render
from django.http import HttpResponse
import joblib
from math import radians,tan
from pyproj import Proj
import numpy as np
import numpy as np 
from math import radians , tan
from pyproj import Proj
from matplotlib.path import Path
def pathplanning(request):
    import json
    if request.method=='POST':
        cordinates = request.POST
        cordinates1 = dict(cordinates)
        ovrelaping = float(cordinates1.get('overlaping')[0])
        ar=cordinates1.get('ar')
        split_ar = ar[0].split(":")
        width = int(split_ar[0])
        height = int(split_ar[1])
        aspwct_ratio = width/height
        altitude=int(cordinates1.get('height')[0])
        algo=cordinates1.get('Algo')[0]
        cr=[]
        for key,value in cordinates1.items():
            if key.startswith('cordinates'):
                cr.append(value)
        cor = []
        for i in cr:
            lat = float(i[0])
            lan = float(i[1])
            d = [lat,lan]
            cor.append(d)
        lng=[]
        lat=[]
        for i in range(len(cor)):
            lng.append(cor[i][0])
            lat.append(cor[i][1])
        pp = Proj(proj='utm',zone=42,ellps='WGS84', preserve_units=False)
        x,y = pp(lng,lat)
        al = radians(90)
        cell_y_o = (2*altitude*tan(al/2))/(1+aspwct_ratio**2)**0.5
        cell_x_o = aspwct_ratio*((2*altitude*tan(al/2))/(1+aspwct_ratio**2)**0.5)
        x_size = (1-ovrelaping)*cell_x_o
        y_size = (1-ovrelaping)*cell_y_o
        x_max = np.max(x)
        y_max = np.max(y)
        x_min = np.min(x)
        y_min = np.min(y)
        x_limit = int(np.ceil((x_max-x_min) / x_size)) 
        y_limit = int(np.ceil((y_max-y_min) / y_size)) 
        cells_maps = np.zeros((x_limit, y_limit), dtype=bool)
        grids = []
        grids_center=[]
        cor_map_its_center={}
        path = Path(np.column_stack([x, y]))
        for i in range(x_limit):
            for j in range(y_limit):
                x0, y0 = x_min + i * x_size, y_min + j * y_size
                if path.contains_point([x0, y0]) and path.contains_point([x0, y0 + y_size]) and path.contains_point([x0 + x_size, y0 + y_size]) and path.contains_point([x0 + x_size, y0]):
                    grid = np.array([[x0, y0], [x0, y0 + y_size], [x0 + x_size, y0 + y_size], [x0 + x_size, y0]])
                    grids.append(grid)
                    cells_maps[i][j] = 1
                    x_center = (x0+x0+x_size)/2
                    y_center = (y0+y0+y_size)/2
                    key = f"{i},{j}"
                    cor_map_its_center[key]=[x_center,y_center]
                else:
                    grids.append(0)
                    cells_maps[i][j] = 0

        graph_of_area = {}
        for i in range(x_limit):
            for j in range(y_limit):
                if cells_maps[i][j]:
                    node_id = f"{i},{j}"
                    neighbor_id = []
                    if i > 0 and cells_maps[i-1][j]:
                        neighbor_id.append(f"{i-1},{j}")
                    if i < x_limit-1 and cells_maps[i+1][j]:
                        neighbor_id.append(f"{i+1},{j}")
                    if j > 0 and cells_maps[i][j-1]:
                        neighbor_id.append(f"{i},{j-1}")
                    if j < y_limit-1 and cells_maps[i][j+1]:
                        neighbor_id.append(f"{i},{j+1}")
                    graph_of_area[node_id]=neighbor_id
        visited = set()
        path = []
        if algo=='DFS':
            def dfs(visited, graph, node):
                if node not in visited:
                    path.append(node)
                    visited.add(node)
                    for neighbour in graph[node]:
                        dfs(visited, graph, neighbour)
            s=list(graph_of_area.keys())
            dfs(visited, graph_of_area, s[0])
            path2=[]
            for i in path:
                cord = cor_map_its_center[i]
                path2.append(cord)
            lng = []
            lat = []
            final_path_with_lat_lng = []
            for i in range(len(path2)):
                x,y = path2[i]
                lat_lng = pp(x,y,inverse=True)
                final_path_with_lat_lng.append(lat_lng)
        if algo=="BFS":
            def bfs_zigzag(graph, start):
                if start not in graph:
                    return []
                result = []
                queue = [(start, 0)]
                v = set([start])
                while queue:
                    node, level = queue.pop(0)
                    if len(result) <= level:
                        result.append([])
                    if level % 2 == 0:
                        result[level].append(node)
                    else:
                        result[level].insert(0, node)
                    for n in graph[node]:
                        if n not in v:
                            v.add(n)
                            queue.append((n, level + 1))
                            graph[n].append(node)
                return result
            s=list(graph_of_area.keys())
            zz=bfs_zigzag(graph_of_area, s[0])
            zz_f=[]
            for i in range(len(zz)):   
                zz2 = zz[i]
                for j in range(len(zz2)):
                    zz_f.append(zz2[j])
            path3=[]
            for i in zz_f:
                cord = cor_map_its_center[i]
                path3.append(cord)
            lng = []
            lat = []
            final_path_with_lat_lng = []
            for i in range(len(path3)):
                x,y = path3[i]
                lat_lng = pp(x,y,inverse=True)
                final_path_with_lat_lng.append(lat_lng)       
    import json
    path_geojson = {
    "type": "Feature",
    "geometry": {
        "type": "LineString",
        "coordinates": final_path_with_lat_lng
    },
    "properties": {}
}
    path_geojson_str = json.dumps(path_geojson)
    return HttpResponse(path_geojson_str)
def pathplanning_NFZ(request):
    import json
    if request.method=='POST':
        cordinates = request.POST
        cordinates1 = dict(cordinates)
        print(cordinates1)
        ovrelaping = float(cordinates1.get('overlaping')[0])
        ar=cordinates1.get('ar')
        split_ar = ar[0].split(":")
        width = int(split_ar[0])
        height = int(split_ar[1])
        aspwct_ratio = width/height
        altitude=int(cordinates1.get('height')[0])
        algo=cordinates1.get('Algo')[0]
        cr=[]
        for key,value in cordinates1.items():
            if key.startswith('cordinates'):
                cr.append(value)
        cor = []
        for i in cr:
            lat = float(i[0])
            lan = float(i[1])
            d = [lat,lan]
            cor.append(d)
        for key,value in cordinates1.items():
            if key.startswith('cordinates'):
                cr.append(value)
        cor = []
        for i in cr:
            lat = float(i[0])
            lan = float(i[1])
            d = [lat,lan]
            cor.append(d)
        
        final_path_with_lat_lng = "done"
    import json
    path_geojson = {
    "type": "Feature",
    "geometry": {
        "type": "LineString",
        "coordinates": final_path_with_lat_lng
    },
    "properties": {}
}
    path_geojson_str = json.dumps(path_geojson)
    return HttpResponse(path_geojson_str)