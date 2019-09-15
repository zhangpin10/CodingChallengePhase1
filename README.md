# Code and Demo Instruction

## Demo.py: 
### main demo file. It demos the procedures of data parser pipeline and data loader pipeline. 

- 1. User can just run Demo.py.

- 2. The parsed dicom data and contour masks will be save into a data.h5 file after running the code.

- 3. Two log files will be generated for the two pipelines with the names of “parser.log” and “loader.log”. In the parser.log file, the dataset with contour files but failed in parsing with be recorded.

- 4. The verification images will be generated for all saved samples under the “visual_result‘’ folder. 

     A parser verification image is an overlapping image of dicom data, mask and contour. Its name starting with prefix “parser_”. Two examples are shown below: 

     A loader verification image is an overlapping image of dicom data and a mask since we only load image and mask during the loading procedure. The image name starts with prefix “loader_”. Two examples are shown below:

![parser_SCD0000101-59.png](https://github.com/zhangpin10/CodingChallengePhase1/blob/master/visual_results/loader_SCD0000101-59.png)
