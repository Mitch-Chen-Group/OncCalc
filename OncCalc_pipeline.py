import os
import numpy as np
import nibabel as nb
import gc
from totalsegmentator.python_api import totalsegmentator
import argparse



    
if __name__ == '__main__':
        
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="Input path to folder containing image files")
    parser.add_argument("--mask", help="Input path to folder containing inference files")
    #parser.add_argument("--o", help="Please input path to image folder")
    args=parser.parse_args()
    
    #define take in the image folder and segmentation folder paths
    input_path = args.image
    mask_path = args.mask
   # output_path = args.I
    
    for file in os.listdir(input_path):
        new_path = os.path.join(input_path, file) 
        # load an image for 
        input_img = nb.load(new_path)
        print(f"new : {file}")
        try:
            #run the total segmentator pipeline
            total_seg_img = totalsegmentator(input_img, fast=True)
            print(f" post prediction {file}")
            
            #TotalSegmentator output data
            #print(type(total_seg_img))
            #print(total_seg_img.header)
            
            total_seg_data = total_seg_img.get_fdata()
            print("\n")
            print("data accessed")
            #get the inference file name according to the nnUNet format
            predicted_name = file.split("_0000")[0] + ".nii.gz"
            print(predicted_name)
            predicted_image = nb.load(os.path.join(mask_path, predicted_name))
            
            predicted_data = predicted_image.get_fdata()
            #find all voxels that correspond to aorta in total segmentator mask: A
            aortax, aortay, aortaz = np.where(np.round(total_seg_data)==52)
            
            #find all voxels that correspond to coronary calcification in predicted mask: P
            px,py,pz = np.where(np.round(predicted_data)==1)
            predict_size = len(px)
            
            #find all predicted voxels that are in the aorta: |P n A| and remove them from P
            aorta_seg = set()
            intracardiac_p = set()
            for (i,j,k) in zip(aortax, aortay, aortaz):
                aorta_seg.add((i,j,k))
            for (i,j,k) in zip(px, py, pz):
                if (i,j,k) not in aorta_seg:
                    intracardiac_p.add((i,j,k))
            predicted_size = len(intracardiac_p)
           
            #we are going to calculate the predicted CAC scores    
            #tells us the voxel dimensions in mm ->multiply these and multiply by the number of voxels
            img_data = input_img.get_fdata()
            x,y,z = input_img.header.get_zooms()
            volume =  x * y * z
            
            #density is scored 1 for 130–199 HU, 2 for 200–299 HU, 3 for 300–399 HU, 
            # and 4 for 400 HU and greater
            count_1 = count_2 = count_3 = count_4 =0
            #calculate predicted cac score
            for x,y,z in intracardiac_p:
                #calc.append(img_data[x,y,z])
                if 200> img_data[x,y,z] >= 130:
                    count_1 += 1
                elif 300> img_data[x,y,z] >= 200:
                    count_2 +=1
                elif 400> img_data[x,y,z] >= 300:
                    count_3 +=1
                elif img_data[x,y,z] >= 400:
                    count_4 += 1
            p_score = (1* count_1 + 2 *count_2 +  3 * count_3 + 4 * count_4) * volume
            
            #writes risk score to text document based on CAC threshold
            print(f"predicted cac is {p_score}")
            with open("CVD_risk400.txt", "a") as outfile:
                outcome = "high risk" if p_score>=400 else "low risk"
                outfile.write(f"image is {file} , predicted cac:{p_score}, outcome: {outcome}\n")
            with open("CVD_risk100.txt", "a") as outfile2:
                outcome = "high risk" if p_score>=100 else "low risk" 
                outfile2.write(f"image is {file}, predicted cac:{p_score}, outcome: {outcome}\n")
        except:
            print("Image could not be processed, continuing")
            
