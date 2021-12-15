from PIL import Image
import os.path
import glob
import shutil

def convertjpg(order,jpgfile,outdir,width=128,height=128):
    img=Image.open(jpgfile)
    try:
        new_img=img.resize((width,height),Image.BILINEAR)
        # new_img.save(os.path.join(outdir,,os.path.basename(jpgfile)[:-4]) + '.jpg')
        new_img.save(outdir + "reshaped_" + os.path.basename(jpgfile)[:-4] + '.jpg')

        haxlist = os.path.basename(jpgfile) + " -> " + "reshaped_" + os.path.basename(jpgfile)[:-4] + '.jpg' + "\n"
        write_txt(path_file_name, haxlist)

    except Exception as e:
        print(e)

def write_txt (path_file_name, str_data):


    with open(path_file_name, 'a', encoding="utf-8") as f:
        f.write(str_data)


if __name__ == "__main__":
    path_file_name = 'logs.txt'
    if not os.path.exists(path_file_name):
        with open(path_file_name, 'w') as f:
            print(f)
    else:
        os.remove(path_file_name)
        with open(path_file_name, 'w') as f:
            print(f)
    t = 0
    for jpgfile in glob.glob("D:/Projects/实验室任务/第十六周留档/Gmm聚类/img/*.png"):
        convertjpg(t,jpgfile, "D:/Projects/实验室任务/第十六周留档/Gmm聚类/img_re/")
        t = t+1

    # ****************************************************************** #
    # save the corresponding relations between original file and reshaped one.
    # logs.txt format:
    # original_name.jpg -> reshaped_name.jpg
    # example:
    # 1.jpg -> reshaped_1.jpg
