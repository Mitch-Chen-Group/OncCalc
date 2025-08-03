import os
import numpy as np
import nibabel as nb
import gc

#We want to loop through the predicted images and check their intersection with the heart segmentation in heart_seg
total_segmentator = "TotalSegmentaor output folder"#totalsegmentator output folder
prediction = "OncCalc segmentation masks output folder" #inference output folder
true = "Ground truth segmentation masks folder" #true segmentation folder
image = "CT images folder" #image folder

#creates two documents comparing outcome for each image 

for file in os.listdir(prediction):
    try:
    # we need to find the corresponding file in total segmentator and this file 
        total_seg = file.split(".")[0]+ "_0000.nii.gz"
        print(f"\nprediction images is {file}, total seg is {total_seg}")
        #load total segmentator mask and predicted mask as arrays
        total_seg_data = nb.load(os.path.join(total_segmentator, total_seg)).get_fdata()
        predicted_data = nb.load(os.path.join(prediction, file)).get_fdata()
        
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
    
    #now we want to calculated dice scores with intracardiac_p and true segmentation
    #we load the file for the true segmentation    
        true_file = "true_seg_" + file
        #print(f"true mask file is {true_file}")
        true_seg_data = nb.load(os.path.join(true, true_file)).get_fdata()
    #get all voxels where the true mask is labelled
        tx,ty,tz = np.where(np.round(true_seg_data)==1)
        union = set()
        true_size = 0        
        for (i,j,k) in zip(tx,ty,tz):
            if (i,j,k) not in aorta_seg:
                union.add((i,j,k))
                true_size+=1
            
        for (i,j,k) in intracardiac_p:
            union.add((i,j,k))
        print("union:" + str(len(union)))
    #calculate the overlap by |A|+|P|-|A u P|= |A n P|
        overlap =  predicted_size + true_size - len(union)
        
        if len(union)==0:
    #avoid dividing by zero error
            print("both masks are empty")
            continue
        dice = (2* overlap)/(predicted_size + true_size)
        print(f"overlap is {overlap}, p size: {predicted_size}, t size: {true_size} and dice is {dice}")
    #  with open("post_tsegmentator_dice.txt", 'a') as outfile:
    #     outfile.write(f"new dice score for {file} is {dice}\n")
    except:
        if file.split("-")[0]!="zero":
            print(f"could not find {file}")
            continue
    #we are going to calculate the predicted CAC scores    
    #tells us the voxel dimensions in mm ->multiply these and multiply by the number of voxels
    img = nb.load(os.path.join(image, total_seg))
    img_data = img.get_fdata()
    x,y,z = img.header.get_zooms()
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
    #calculate true cac scores
    count_1 = count_2 = count_3 = count_4 =0
    if file.split("-")[0]!="zero":
        for x,y,z in zip(tx,ty,tz):
            if (x,y,z) not in aorta_seg:
                if 200> img_data[x,y,z] >= 130:
                    count_1 += 1
                elif 300> img_data[x,y,z] >= 200:
                    count_2 +=1
                elif 400> img_data[x,y,z] >= 300:
                    count_3 +=1
                elif img_data[x,y,z] >= 400:
                    count_4 += 1
    t_score1 = (1* count_1 + 2 *count_2 +  3 * count_3 + 4 * count_4) * volume
    
    print(f" true cac is {t_score1} and predicted is {p_score}")
    with open("post_tsegmentator_cac400.txt", "a") as outfile:
        # xor operator to compare if predicted and true scores fall on same side of threshold
        # outcome is 1 is both are below threshold or both are above threshold
        outcome = 1 ^ ((p_score>=400) ^ (t_score1>=400))
        outfile.write(f"image is {total_seg}, true cac: {t_score1}, predicted cac:{p_score}, outcome: {outcome}\n")
    with open("post_tsegmentator_cac100.txt", "a") as outfile2:
        # xor operator to compare if predicted and true scores fall on same side of threshold
        # outcome is 1 is both are below threshold or both are above threshold
        outcome = 1 ^ ((p_score>=100) ^ (t_score1>=100))
        outfile2.write(f"image is {total_seg}, true cac: {t_score1}, predicted cac:{p_score}, outcome: {outcome}\n")

