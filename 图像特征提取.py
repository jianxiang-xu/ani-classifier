from PIL import Image
import os
import numpy as np
import csv
def load_images_from_folder(folder):
    images=[]
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.png','.jpg','.jpeg')):
            img=Image.open(os.path.join(folder,filename))
            images.append(img)
    return images
def multiple_img_features(img):
    gray_img=img.convert('L')
    factor = 64
    HI, HE = [0] * factor, [0] * factor
    N,M = img.size
    for x in range(N):
        for y in range(M):
            ind = int((gray_img.getpixel((x, y)) / 255) * (factor - 1))
            if (x == 0 or y == 0 or x + 1 == N or y + 1 == M):
                HE[ind] += 1
            else:
                if (gray_img.getpixel((x, y)) == gray_img.getpixel((x, y - 1)) and
                        gray_img.getpixel((x, y)) == gray_img.getpixel((x, y + 1)) and
                        gray_img.getpixel((x, y)) == gray_img.getpixel((x - 1, y)) and
                        gray_img.getpixel((x, y)) == gray_img.getpixel((x + 1, y))):
                    HI[ind] += 1
                else:
                    HE[ind] += 1
    return HI + HE

def get_image_feature_vector(image, positive):
    BIC_results = multiple_img_features(image)

    if positive == 0:
        BIC_results = np.append(BIC_results, 0)
        feature_set = BIC_results
    if positive == 1:
        BIC_results = np.append(BIC_results, 1)
        feature_set = BIC_results

    return feature_set

def get_all_image_feature_vectors(images, positive):
    feature_sets = []

    for image in images:
        feature_set = get_image_feature_vector(image, positive)
        feature_sets.append(feature_set)

    return feature_sets

def create_csv_output(filename, zerodir, onedir):
    # Load images
    zero_images = load_images_from_folder(zerodir)
    one_images = load_images_from_folder(onedir)

    # Get feature vectors of images
    zero_feature_vectors = get_all_image_feature_vectors(zero_images, 0)
    one_feature_vectors = get_all_image_feature_vectors(one_images, 1)

    # Input feature vectors into a CSV file
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(zero_feature_vectors)
        writer.writerows(one_feature_vectors)

# import cv2
# import numpy as np

# img=Image.open(r"C:\Users\xujia\Saved Games\BLACKSOULSⅡCHN\BLACKSOULSⅡCHN\Graphics\Pictures\7-1.png")
# print(multiple_img_features(img))


create_csv_output(r"C:\Users\xujia\feature_vectors.txt",r"C:\Users\xujia\downloaded_images_charactor",r"C:\Users\xujia\downloaded_images_person")
#print(load_images_from_folder(r"C:\Users\xujia\downloaded_images_charactor"))
