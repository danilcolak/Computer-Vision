from tkinter import filedialog
import PIL.Image
import PIL
import numpy as np




def main():
    file_path_string = filedialog.askopenfilename() # we can select our image from wanted directory
    img = PIL.Image.open(file_path_string)
    img.show()
    img,img1 = PIL2np(img)
    I_x ,I_y= np.gradient(img)
    Ixx = I_x ** 2
    Ixy = I_y * I_x
    Iyy = I_y ** 2
    final_image=np2PIL(harris_responce(img1,Ixx,Iyy,Ixy,3))
    final_image.show()


def PIL2np(img):  # we created the gray version of image and also measured the size of the image
    nrows = img.size[0]
    ncols = img.size[1]
    print("nrows, ncols : ", nrows,ncols)
    imgarray1 = np.array(img.convert("RGB"))
    imgarray = np.array(img.convert("L"))
    return imgarray ,imgarray1

def np2PIL(im):
    #print("size of arr: ",im.shape)
    img = PIL.Image.fromarray(np.uint8(im))
    return img

def harris_responce(img,ixx,iyy,ixy,windowSize):                    # here we calculate sum of squares while shifting our window trough each pixel.The shifting operation
     height= img.shape[0]                                          # is applied according to the offset which is based on our window size
     width = img.shape[1]
     offset = int(windowSize/2)
     Ixx=ixx
     Iyy=iyy
     Ixy=ixy
     image_copy= img.copy()
     detected_corner= []

     k = 0.04
     for y in range(offset, height - offset):
         for x in range(offset, width - offset):
            Sxx = np.sum(Ixx[y - offset:y + 1 + offset, x - offset:x + 1 + offset])
            Syy = np.sum(Iyy[y - offset:y + 1 + offset, x - offset:x + 1 + offset])
            Sxy = np.sum(Ixy[y - offset:y + 1 + offset, x - offset:x + 1 + offset])
            det = (Sxx * Syy) - (Sxy ** 2)                    # Finding determinant value
            trace = Sxx + Syy
            r = det - k * (trace ** 2)
            if r > 0:
                detected_corner.append([x,y,r])
                image_copy.itemset((y, x, 0), 255)
                image_copy.itemset((y, x, 1), 0)
                image_copy.itemset((y, x, 2), 0)
     return image_copy


if __name__ == '__main__':
    main()