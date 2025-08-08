## **For paper "Automated Cardiovascular Risk Assessment in Non-Small Cell Lung Cancer Patients on Routine Low Dose Chest CT using an Optimised nnU-Net Framework"**

This is work which is based on the nnUNet architecture developed by the team at the Applied computer vision lab(ACVL) and the TotalSegmentator tool. 

Please refer to the paper by Fabian Isensee which can be found [here](https://www.nature.com/articles/s41592-020-01008-z).

Instructions to use the model are as follows:
### Setting Up
  * run the command `
    conda env create -f environment.yml` in the terminal to create the virtual environment with the required depencies.
  * To activate the environment run `conda activate medical-imaging-env`. Keep in mind that you need to always activate the virtual environment to use the pipeline.
  * Deactive the environment with `conda deactivate`

### SEGMENTATION
  * Firstly, Install nnUNet2 by following the [link](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/installation_instructions.md).
  * Create a new folder called `nnUNetDataset` with two subfolders named `nnUNet_raw` and `nnUNet_results`.
  * In each of these subfolders create a dataset folder using the naming convention: Dataset[DATASET_NAME_OR_ID]_organ-name (DATASET_NAME_OR_ID corresponds to a three digit identification ie: 001 and organ-name is substitued with the organ, we will used Dataset001_Coronary as example).
  * Download the model files [here](https://huggingface.co/Yinka-anifowose/OncCalc/tree/main) into the `nnUNet_results/Dataset001_Coronary` folder.
  * Please familiarise yourself with the dataset format used by nnUNet with the following [link](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/setting_up_paths.md)
    * `nnUNet_raw/Dataset001_Coronary` is where you store your raw images in the required file format and naming convention [image_number]_0000.nii.gz ie `145_0000.nii.gz`.
  * Adjust your environment variables according to the following [page](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/set_environment_variables.md):
    * Note that you do not need a `nnUNet_preprocessed` variable as the images from `nnUNet_raw` will be preprocessed by nnUNet during inference.
  * Run the following command: `nnUNetv2_predict -i INPUT_FOLDER -o OUTPUT_FOLDER -d DATASET_NAME_OR_ID -c 3d_fullres `:
    * where `INPUT_FOLDER` is `../nnUNet_raw/Dataset001_Coronary` and `OUTPUT_FOLDER` is where you want the segmentation masks to be saved.
    * `Dataset_NAME_OR_ID` in our example is 1 (corresponding to 001)
### TotalSegmentator post-processing and CAC score calculation
  * Clone this repository with `git clone https://github.com/Mitch-Chen-Group/OncCalc`
  * Run the following command in terminal of the cloned repository:
   ```
   python OncCalc_pipeline.py --image [PATH_TO_FOLDER_CONTAINING_CT_IMAGES] --mask [PATH_TO_FOLDER_CONTAINING_NNUNET_INFERENCE]
   ```
  * This will create a text document assigning cardiovacular risk to each CT image according to your naming/id.
      

