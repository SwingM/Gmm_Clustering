 # -*- coding: utf-8 -*-
from PCV.tools import imtools
import pickle
from pylab import *
from PIL import Image
from PCV.tools import pca
import os.path
import glob
import shutil
import scipy.misc

def write_txt (path_file_name, str_data):
    with open(path_file_name, 'a', encoding="utf-8") as f:
        f.write(str_data)

def convertjpg(jpgfile, outdir, width, height):
    if not os.listdir(outdir):
        shutil.rmtree(outdir)
        os.mkdir(outdir)
    img = Image.open(jpgfile)
    try:
        new_img = img.resize((width, height), Image.BILINEAR)
        if (new_img.mode!= 'RGB'):
            new_img.convert('RGB')
        new_img.save(os.path.join(outdir, os.path.basename(jpgfile).split('.')[0]) + '.jpg')
    except Exception as e:
        print(e)

def convertjpg(order,jpgfile,outdir,width=128,height=128):
    if not os.listdir(outdir):
        shutil.rmtree(outdir)
        os.mkdir(outdir)
    img = Image.open(jpgfile)
    try:
        new_img = img.resize((width,height),Image.BILINEAR)
        if (new_img.mode!= 'RGB'):
            new_img.convert('RGB')
        new_img.save(outdir + "reshaped_" + os.path.basename(jpgfile)[:-4] + '.jpg')
        haxlist = str(order) + ' -> ' + os.path.basename(jpgfile) + " -> " + "reshaped_" + os.path.basename(jpgfile)[:-4] + '.jpg' + "\n"
        write_txt(path_file_name, haxlist)

    except Exception as e:
        print(e)

def reshapeimg(source1,source2,width=128, height=128):
    t = 0
    for jpgfile in glob.glob(source1):
        convertjpg(t,jpgfile, source2, width, height)
        t = t + 1
    return source2

def gmm(source, kinds, width=128, height=128):
    # Uses sparse pca codepath.
    imlist = imtools.get_imlist(source)
    # img lists and  their sizes
    im = array(Image.open(imlist[0]))  # open one image to get the size
    m, n = im.shape[:2]  # get the size of the images
    imnbr = len(imlist)  # get the number of images
    print("The number of images is %d" % imnbr)

    # Create matrix to store all flattened images
    immatrix = array([array(Image.open(imname)).flatten() for imname in imlist], 'f')

    # PCA降维
    V, S, immean = pca.pca(immatrix)

    # save mean and main ingredient
    # f = open('./a_pca_modes.pkl', 'wb')
    f = open('./model_save/a_pca_modes.pkl', 'wb')
    pickle.dump(immean, f)
    pickle.dump(V, f)
    f.close()

    # get list of images
    imlist = imtools.get_imlist('./img_re/')
    imnbr = len(imlist)

    # load model file
    with open('./model_save/a_pca_modes.pkl', 'rb') as f:
        immean = pickle.load(f)
        V = pickle.load(f)
    # create matrix to store all flattened images
    immatrix = array([array(Image.open(im)).flatten() for im in imlist], 'f')

    # project on the 40 first PCs
    immean = immean.flatten()
    projected = array([dot(V[:40], immatrix[i] - immean) for i in range(imnbr)])

    # GMM
    from sklearn.mixture import GaussianMixture as GMM



    gmm = GMM(n_components=kinds).fit(projected)  # set the number of centers to kinds
    labels = gmm.predict(projected)

    # plot pics
    for k in range(kinds):

        # create root
        isExists = os.path.exists("save/" + str(k) + "/")

        if not isExists:
            os.makedirs("save/" + str(k) + "/")
        else:
            shutil.rmtree("save/" + str(k) + "/")
            os.makedirs("save/" + str(k) + "/")


        ind = where(labels == k)[0]
        figure()
        gray()
        print(np.sum(labels == k))
        for i in range(minimum(len(ind), 60)):
            # subplot(8, 10, i + 1)
            # imshow(immatrix[ind[i]].reshape((width, height, 3)) / 255)

            scipy.misc.imsave("save/" + str(k) + "/" + str(ind[i])+'.jpg', immatrix[ind[i]].reshape((width, height, 3)) / 255)

            # axis('off')
    # show()


path_file_name = 'logs.txt'
if __name__ == '__main__':
    # source1 is the source of original images with jpg as name.
    # source2 is the source of reshaped images.
    # gmm required inputs of reshaped images and numbers of kinds.

    if not os.path.exists(path_file_name):
        with open(path_file_name, 'w') as f:
            print(f)
    else:
        os.remove(path_file_name)
        with open(path_file_name, 'w') as f:
            print(f)

    re_source = reshapeimg('./img/*.png','./img_re/', 256, 256)
    gmm(re_source,5,256, 256)

