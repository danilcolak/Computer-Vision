import PIL
import PIL.Image
import numpy as np
from tkinter import filedialog
import scipy.stats as st

def  main():

    img = readPILimg()
    arr = PIL2np(img)
    filter1 = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    filter_select=input("Which filter do you want to apply? filter1/ Gaussian / mulgaus : \n")
    if(filter_select == "filter1"):
        im_out = convolve(arr, filter1)
        new_img = np2PIL(im_out)
        new_img.show()
    if(filter_select == "Gaussian" or filter_select == "gaussian" ):
        x=input("Give a sigma value:\n")
        im_out = convolve(arr,gaussian_kernel_converter((4*int(x))+1,int(x)))
        new_img = np2PIL(im_out)
        new_img.show()
    if(filter_select=="mulgaus"):
        print("Give 2 sigma values (more than 0) Ex: Sigma1=2 Sigma2=5\n")
        sigma1=input("First sigma value:\n")
        sigma2=input("Second sigma value:\n")
        sigma1img = convolve(arr, gaussian_kernel_converter((4 * int(sigma1)) + 1, int(sigma1)))
        sigma2img = convolve(arr, gaussian_kernel_converter((4 * int(sigma2)) + 1, int(sigma2)))
        new_img = np2PIL(sigma2img)
        new_img.show()
        multimg = convolve(sigma1img, gaussian_kernel_converter((4 * (int(sigma2)-int(sigma1))) + 1, int(sigma2)-int(sigma1)))
        mulnew_img=np2PIL(multimg)
        mulnew_img.show()
        
def readPILimg():
    file_path_string = filedialog.askopenfilename()
    img = PIL.Image.open(file_path_string )
    img.show()
    img_gray = color2gray(img)
    img_gray.show()
    return img_gray

def color2gray(img):
    img_gray = img.convert('L')
    return img_gray

def PIL2np(img):
    nrows = img.size[0]
    ncols = img.size[1]
    print("nrows, ncols : ", nrows,ncols)
    imgarray = np.array(img.convert("L"))
    return imgarray

def np2PIL(im):
    print("size of arr: ",im.shape)
    img = PIL.Image.fromarray(np.uint8(im))
    return img


def gaussian_kernel_converter(kernlen,nsig):
    interval = (2*nsig+1.)/(kernlen)
    x = np.linspace(-nsig-interval/2., nsig+interval/2., kernlen+1)
    kern1d = np.diff(st.norm.cdf(x))
    kernel_raw = np.sqrt(np.outer(kern1d, kern1d))
    kernel = kernel_raw/kernel_raw.sum()
    return kernel


def convolve(im,filter):
    (nrows, ncols) = im.shape
    (k1,k2) = filter.shape
    k1h = (k1 -1) / 2
    k2h = (k2 -1) / 2
    print(k1h)
    print(k2h)

    im_out = np.zeros(shape = im.shape)
    print("image size , filter size ", nrows, ncols, k1, k2)
    for i in range(int(k1h), nrows - int(k1h)):
        for j in range(int(k2h), ncols - int(k2h)):
            sum = 0.
            for l in range(int(-k1h), int(k1h)+1):
                for m in range(int(-k2h), int(k2h)+1):
                    sum += im[i - l][j - m] * filter[l][m]
            im_out[i][j] = sum
    return im_out

if __name__=='__main__':
    main()
