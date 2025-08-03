import nibabel as nb
import numpy as np

source = "Segmentation mask of image"
filter = "TotalSegmentator output for same image"
img = "Actual image"


source_data = nb.load(source)
filter_data = nb.load(filter).get_fdata()
img_data = nb.load(img).get_fdata()

new_img = np.zeros(source_data.shape)
x,y,z = np.where(np.round(source_data.get_fdata())==1)
x2,y2,z2 = np.where(np.round(filter_data)==52)
filter_set= set()
for (i,j,k) in zip(x2,y2,z2):
    filter_set.add((i,j,k))
    
count_1 =count_2=count_3=count_4=0

for (i,j,k) in zip(x,y,z):
    if (i,j,k) not in filter_set:
        new_img[i,j,k]=1
        if 200> img_data[i,j,k] >= 130:
            count_1 += 1
        elif 300> img_data[i,j,k] >= 200:
            count_2 +=1
        elif 400> img_data[i,j,k] >= 300:
            count_3 +=1
        elif img_data[i,j,k] >= 400:
            count_4 += 1
a,b,c = source_data.header.get_zooms()
volume = a*b*c
p_score = (1* count_1 + 2 *count_2 +  3 * count_3 + 4 * count_4) * volume
print(source_data.affine, source_data.header)
new_img = nb.Nifti1Image(new_img, affine = source_data.affine,header = source_data.header)
nb.save(new_img, "post-processed_image_name")