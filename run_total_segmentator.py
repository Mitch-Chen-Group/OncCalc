#TotalSegmentator -i ct.nii.gz -o segmentations
#TotalSegmentator -i EurRad_data\0_0000.nii.gz -o totalsegmentations -ta heart --fast
import nibabel as nib
from totalsegmentator.python_api import totalsegmentator
import os


#@profile
#def segment(**kwargs):
 #   return totalsegmentator(**kwargs)
    # option 1: provide input and output as file paths
    
if __name__ == '__main__':
        
    input_path = "EurRad_data"
    output_path = "totalsegmentations"
    output_set = set()
    for f in os.listdir(output_path):
        output_set.add(f)
    for file in os.listdir(input_path):
        if file in output_set: 
            continue
        new_path = os.path.join(input_path, file) 
        # option 2: provide input and output as nifti image objects
        input_img = nib.load(new_path)
        print(f"new : {file}")
        try:
            output_img = totalsegmentator(input_img, fast=True)
            print(f" post prediction {file}")
            new_output = os.path.join(output_path, file)
            print(new_output)
            nib.save(output_img, new_output)
        except:
            print("skipped due to error")
            continue
        