## **For paper "Automated Cardiovascular Risk Assessment in Non-Small Cell Lung Cancer Patients on Routine Low Dose Chest CT using an Optimised nnU-Net Framework"**

This is the code repository supporting the paper manuscript submitted to European Radiology (2025).

1) The model architecture is based on nnU-Net developed by Isensee et al. (2020) [paper](https://www.nature.com/articles/s41592-020-01008-z).
2) Use of TotalSegmentator (nnU-Net-based multi-organ segmentation tool) is made in the pipeline, by Wasserthal et al. (2023) [paper](https://pubs.rsna.org/doi/10.1148/ryai.230024).

Instructions to use the model are as follows:
### Setting Up
  * Clone this repository with `git clone https://github.com/Mitch-Chen-Group/OncCalc`
  * Create a new folder called `nnUNetDataset` with two subfolders named `nnUNet_raw` and `nnUNet_results`.
  * In each of these subfolders create a dataset folder using the naming convention: Dataset[DATASET_NAME_OR_ID]_organ-name (DATASET_NAME_OR_ID corresponds to a three digit identification ie: 001 and organ-name is substitued with the organ, we will used Dataset001_Coronary as example).
  * `nnUNet_raw/Dataset001_Coronary` is where you store your folder of raw images in the required file format and naming convention [image_number]_0000.nii.gz ie `145_0000.nii.gz`.
  * Please familiarise yourself with the dataset format used by nnUNet with the following [link](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/setting_up_paths.md)
  
### Segmentation
  * Firstly, Install nnUNet2 by following the [link](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/installation_instructions.md).
    * Make sure that you install pytorch correctly according to your hardware specifications.
    * For nnUNetv2 use the installation process under the use case of "...out-of-the-box segmentation algorithm or for running inference with pretrained models"
  * Before downloading the model you need to run` git lfs install ` to be able to clone large folders.
    * You then need to navigate to the `nnUNet_raw/Dataset001_Coronary` directory in your computer.
    * Download the model files [here](https://huggingface.co/Yinka-anifowose/OncCalc/tree/main) You must be in the  `nnUNet_results/Dataset001_Coronary` directory.
    * run the following command to get the model files in the directory `mv OncCalc/* . && rm -r OncCalc`
 
  * Adjust your environment variables according to the following [page](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/set_environment_variables.md):
  * Run the following command: `nnUNetv2_predict -i INPUT_FOLDER -o OUTPUT_FOLDER -d DATASET_NAME_OR_ID -c 3d_fullres `:
    * where `INPUT_FOLDER` is `../nnUNet_raw/Dataset001_Coronary` and `OUTPUT_FOLDER` is where you want the segmentation masks to be saved.
    * `Dataset_NAME_OR_ID` in our example is 1 (corresponding to 001)

### TotalSegmentator post-processing and CAC score calculation
  * run the command `
    conda env create -f environment.yml` in the terminal to create the virtual environment with the required depencies.
  * To activate the environment run `conda activate medical-imaging-env`. Keep in mind that you need to always activate the virtual environment to use the pipeline.
  
  * Navigate to the cloned repository and run the following command in terminal of the cloned repository:
   ```
   python OncCalc_pipeline.py --image [PATH_TO_FOLDER_CONTAINING_CT_IMAGES] --mask [PATH_TO_FOLDER_CONTAINING_NNUNET_INFERENCE]
   ```
  * This command runs the `OncCalc_pipeline.py` script and will create a text document assigning cardiovacular risk to each CT image according to your naming/id.
  * You can deactive the environment with `conda deactivate`.



      

