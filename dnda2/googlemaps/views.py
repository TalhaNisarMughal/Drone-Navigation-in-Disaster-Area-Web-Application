from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.http import HttpResponse
import json
from . models import video
import cv2
import numpy as np
import os
from django.urls import reverse
import requests
from  .image_stitching import build_mosaic
def dashboard(request):
    return render (request,"videostraem/video.html")
def VideoUpload(request):
    if request.method == 'POST' and request.FILES['video']:
        video_file = request.FILES['video']
        area_name = request.POST.get('area-name')
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'videos'))
        print("FS->",fs)
        filename = fs.save(video_file.name, video_file)
        video_path = fs.url(filename)
        Video = video(AreaName = area_name , file_name = filename , file_path = video_path)
        Video.save()
        def frame_extractor(path,save_dir,current_frame,gap=50):
            temp=1
            vid = cv2.VideoCapture(path)
            while True:
                flag , frame = vid.read()
                if flag==False:
                    vid.release()
                    break
                else:
                    if(current_frame%gap==0):
                        cv2.imwrite(f"{save_dir}/{temp}.png",frame)
                        temp+=1
                current_frame+=1

        current_frame = 0
        path='.'+video_path+"/videos"
        segments = path.split('/')
        new_segments = [segments[0],  segments[1],segments[-1],segments[2]]
        new_path = '/'.join(new_segments)
        print(new_path)
        save_dir = os.path.join(settings.MEDIA_ROOT, 'dataset/'+area_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            save_dir = os.path.join(settings.MEDIA_ROOT, 'dataset/'+area_name)
        frame_extractor(new_path, save_dir, current_frame,gap=130)

        #---------------------------------
        raw_img_dir      = save_dir
        ftr_detector     = 'sift'
        num_keypoints    = 10000
        save_mosaic_dir = os.path.join(settings.MEDIA_ROOT, 'mosaic/'+area_name)
        flag_save        = True
        #----------------------------------
        input_images = os.listdir(raw_img_dir)
        temp = [(n,int(i.split(".")[0])) for n,i in enumerate(input_images)]
        temp.sort(key=lambda x:x[1])
        input_images = [input_images[i[0]] for i in temp]
        input_images_paths = []
        for i in input_images:
            name = i.split('.')[0]
            ext = i.split('.')[1]
            path = f"{raw_img_dir}/{name}.{ext}"
            input_images_paths.append(path) 
        map_path = build_mosaic(input_images_paths,save_mosaic_dir,area_name,num_keypoints,flag_save)
        print(map_path)
        return render(request,"googlemaps/map.html",{'success': True})
    return render(request,"googlemaps/map.html",{'success': 2})