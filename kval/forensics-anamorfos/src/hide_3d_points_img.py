import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2
from pykdtree.kdtree import KDTree

def poinst_to_img(points):
    img = cv2.imread("colors.png")[:,:,::-1]
    img = cv2.resize(img,(img.shape[1]*2,img.shape[0]*2))
    plt.imshow(img)
    plt.show()

    height,width, _ = img.shape

    points3d = np.uint8(points)
    points3d = points3d[points3d.mean(axis=-1).argsort()]

    kd = KDTree(points3d)

    rgb = img.reshape((-1,3))
    dist,idx = kd.query(rgb, k=1)
    new_rgb = points3d[idx]
    new_rgb[np.random.choice(width*height,len(points3d),replace=False)] = points3d
    new_rgb = new_rgb.reshape((height,width,3))
    plt.imshow(new_rgb)
    plt.show()

    cv2.imwrite("chall.png", new_rgb[:,:,::-1])