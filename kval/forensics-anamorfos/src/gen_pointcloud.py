import open3d as o3d
import cv2
import numpy as np
import random

def rvec_to_mat(rvec):
    mat = np.zeros((4,4))
    R, _ = cv2.Rodrigues(np.float32(rvec))
    mat[:3,:3] = R
    mat[3,3] = 1
    return mat

img1 = cv2.imread("flag.png")
img1 = img1[100:-100]
img1 = cv2.resize(img1,(200,200))

img = np.uint8(np.random.uniform(0,1,(350,350,3))>0.3)*255
img[75:-75,75:-75] = img1

height,width,_ = img.shape

cam = np.zeros(3)

points = []

for x in range(width):
    for y in range(height):
        if img[y,x].mean()<100:
            pixel = np.array([x-width/2,y-height/2,200])
            points.append((pixel-cam)*random.uniform(1,3)+cam)

points = np.array(points)
points -= points.mean(axis=0)

pc = o3d.geometry.PointCloud()
pc.points = o3d.utility.Vector3dVector(np.array(points))
pc.transform(rvec_to_mat([1,0.5,1.5]))

points = np.asarray(pc.points)
points = points/200
points = points[points[:,0]<1]
points = points[points[:,0]>-1]
points = points[points[:,1]<1]
points = points[points[:,1]>-1]
points = points[points[:,2]<1]
points = points[points[:,2]>-1]

points = np.float32(np.uint8((points+1)/2*256))
points = np.concatenate([points, np.float32(np.uint8(np.random.uniform(0,255,(5000,3))))])

pc.points = o3d.utility.Vector3dVector(np.array(points))
pc.paint_uniform_color([0,0,0])

o3d.visualization.draw_geometries([pc])

from hide_3d_points_img import poinst_to_img

poinst_to_img(points)
print(len(points))
