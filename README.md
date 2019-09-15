# Code and Demo Instruction

## Demo.py: 
### main demo file. It demos the procedures of data parser pipeline and data loader pipeline. 

- 1. User can just run Demo.py.

- 2. The parsed dicom data and contour masks will be save into a data.h5 file after executing the code.

- 3. Two log files will be generated for the two pipelines with the names of “parser.log” and “loader.log”. In the "parser.log file", the dataset (with contour files) failed in parsing will be recorded.

- 4. The verification images will be generated for all saved samples under the “visual_result" folder. 

     A parser verification image is an overlapping image of dicom data, mask and contour. Its name starts with prefix “parser_”. 

     A loader verification image is an overlapping image of dicom data and a mask since we only load images and masks during the loading procedure. The image name starts with prefix “loader_”. 
     
     Two examples are shown below:

<p align="center">
  <img src=https://github.com/zhangpin10/CodingChallengePhase1/blob/master/visual_results/parser_SCD0000101-59.png width="400" title="parser_SCD0000101-59.png">
  <img src=https://github.com/zhangpin10/CodingChallengePhase1/blob/master/visual_results/loader_SCD0000101-59.png width="400" alt="loader_SCD0000101-59.png">
</p>

                  parser_SCD0000101-59.png              loader_SCD0000101-59.png
## Demo.py: 
### main demo file. It demos the procedures of data parser pipeline and data loader pipeline. 

- 1. User can just run Demo.py.

- 2. The parsed dicom data and contour masks will be save into a data.h5 file after executing the code.

- 3. Two log files will be generated for the two pipelines with the names of “parser.log” and “loader.log”. In the "parser.log file", the dataset (with contour files) failed in parsing will be recorded.

- 4. The verification images will be generated for all saved samples under the “visual_result" folder. 

     A parser verification image is an overlapping image of dicom data, mask and contour. Its name starts with prefix “parser_”. 

     A loader verification image is an overlapping image of dicom data and a mask since we only load images and masks during the loading procedure. The image name starts with prefix “loader_”. 
