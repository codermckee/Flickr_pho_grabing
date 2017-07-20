# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 18:21:28 2017

@author: Administrator
"""

import json
import flickrapi

path = 'C:\\Users\\Administrator\\Desktop\\flickr\\'

#得到一片区域中的所有坐标
def get_area_coor(lat_min,lat_max,lon_min,lon_max):
    area = []
    while lat_min < lat_max:
        lon = lon_min
        while lon < lon_max:
            coor = (lat_min,lon)
            area.append(coor)
            lon += 0.1
        lat_min += 0.1
    return area
#得到给定城市中的所有坐标
def load_city_coor(city,citys):
    city_area = []
    for line in citys:
        if '\xef\xbb\xbf' in line:
            line = line.replace('\xef\xbb\xbf','')
        str_line = line.split()
        if city == str_line[0]:
            city_area = get_area_coor(float(str_line[1]),float(str_line[2]),float(str_line[3]),float(str_line[4]))
    city_file.close()
    return city_area
        
#保存图片url
def save_photo(photos,file_name):
    save_file = file(path+file_name, 'a+')
    for i in range(len(photos)):
        save_file.write(json.dumps(photos[i]['url_z']))
        save_file.write('\n')
    save_file.close()
    
#得到图片信息    
def get_photo_info(city,coor,file_name):
    page_index = 1
    pages = 2
    file_name = city + '_' +coordinate + '.txt'
    print file_name
    try:
        while page_index <= pages:
            photo_info = flickr.photos.search(page = page_index, tags = 'building', per_page = 10, radius =3, lat = coor[0], lon = coor[1], extras = 'geo, url_z')
            print 'grabing the info of '+ city + ' where coor : ' + str(coor[0])[:5] + '_' + str(coor[1])[:5] + ' current_page :' + str(page_index)
            dict_photo = json.loads(photo_info)
            pages = int(dict_photo['photos']['pages'])
            photos = dict_photo['photos']['photo']
            save_photo(photos,file_name)
            page_index += 1
    except Exception as e:
        print 'error !!!save_photos里的url_x可能未更改！'
        print e
    return photos


api_key = '5b3bf647e7b5ad46255ba8b8ebad6a4e'
api_secret = 'dc6af0c6dad6c128'
flickr = flickrapi.FlickrAPI(api_key, api_secret,format='json')
import  requests #下载图片需要
#1. 首先得到城市坐标
city_file = open('city_list.txt')
citys = city_file.readlines()
city = raw_input('please input the city you wanna download from:')
city_coor = load_city_coor(city,citys)
for coor in city_coor:
    coordinate = str(coor[0])[:5] + '_' + str(coor[1])[:5]
    file_name = city + '_' + coordinate + '.txt'
    photos = get_photo_info(city,coor,file_name)
    #下载图片
    x=0
    handle1=open(path+file_name,'r')
    for line in handle1:
      img_url = line[line.find('h'):-1]
      img = requests.get(img_url)
      f = open(file_name[:-3] + str(x) + 'test.jpg','ab') #存储图片，多媒体文件需要参数b（二进制文件）  
      f.write(img.content) #多媒体存储content
      x += 1
      f.close()
    handle1.close()
    
    
