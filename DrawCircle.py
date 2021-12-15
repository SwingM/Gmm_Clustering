import numpy as np
import os
import math
import random
from PIL import Image




def draw(x,y,t):
    least = math.floor(min(127-x,x-0,127-y,y-0))
    size = random.randint(1, max(127-x,x-0,127-y,y-0))
    a = np.zeros([128,128])
    for i in range (max(0,x-size),min(127,x+size)):
        for j in range (max(0,y-size),min(127,y+size)):
            len = pow(((x-i)*(x-i)+(y-j)*(y-j)),0.5)
            a[i,j] = 255 - (255/size)*len/size

    im = Image.fromarray(a)
    im.convert('RGB').save('D:/Projects/实验室任务/第十六周留档/Gmm聚类//img/'+ str(t) + ".png", format='png')

def drawc(x,y,t):
    size = random.randint(1, 50)
    a = np.zeros([128,128])
    for i in range (max(0,x-size),min(127,x+size)):
        for j in range (max(0,y-size),min(127,y+size)):
            len = pow(((x-i)*(x-i)+(y-j)*(y-j)),0.5)
            if(len <= size):
                a[i,j]= len/size * 255

    im = Image.fromarray(a)
    im.convert('RGB').save('D:/Projects/实验室任务/第十六周留档/Gmm聚类//img/'+ str(t) + ".png", format='png')

def drawcj(x,y,t):
    size = random.randint(1, 50)
    a = np.zeros([128,128])
    for i in range (max(0,x-size),min(127,x+size)):
        for j in range (max(0,y-size),min(127,y+size)):
            len = pow(((x-i)*(x-i)+(y-j)*(y-j)),0.5)
            if(len <= size):
                a[i,j]= max(255 - len/size * 255,0)

    im = Image.fromarray(a)
    im.convert('RGB').save('D:/Projects/实验室任务/第十六周留档/Gmm聚类//img/'+ str(t) + ".png", format='png')


if __name__ == "__main__":
    '''
    for i in range(250):
        x = random.randint(0,127)
        y = random.randint(0,127)
        draw(x,y,i)
    '''
    for i in range(1, 50):
        x = random.randint(50,77)
        y = random.randint(50,77)
        drawc(x,y,i)
    for i in range(51,100):
        x = random.randint(50, 77)
        y = random.randint(50, 77)
        drawcj(x, y, i)

