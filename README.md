# Code and Demo Instruction

## Demo.py
### main demo file. It demos the procedures of data parser pipeline and data loader pipeline. 

- 1. User can just run Demo.py.

- 2. The parsed dicom data and contour masks will be save into a data.h5 file after executing the code.

- 3. Two log files will be generated for the two pipelines with the names of “parser.log” and “loader.log”. In the "parser.log file", the dataset (with contour files) failed in parsing will be recorded.

- 4. The verification images will be generated for all saved samples under the “visual_result" folder. 

     A parser verification image is an overlapping image of dicom data, mask and contour. Its name starts with prefix “parser_”. 

     A loader verification image is an overlapping image of dicom data and a mask since we only load images and masks during the loading procedure. The image name starts with prefix “loader_”. 
     
     Two examples are shown below:

<p align="center">
  <img src=https://github.com/zhangpin10/CodingChallengePhase1/blob/master/visual_results/parser_SCD0000101-59.png width="430" title="parser_SCD0000101-59.png">
  <img src=https://github.com/zhangpin10/CodingChallengePhase1/blob/master/visual_results/loader_SCD0000101-59.png width="430" alt="loader_SCD0000101-59.png">
</p>

                   parser_SCD0000101-59.png                                  loader_SCD0000101-59.png



## run_unit_test.py
### unit test file. It runs unit tests for two functions: DataParser::parse_sample() and DataParser::save_sample() 

- 1. User can just run run_unit_test.py.

- 2. The code will generate results for the two examples listed in /unit_test/link.csv.

- 3. The results of the two samples will be saved under /unit_test/results.

- 4. The baseline of the two examples (under /unit_test/baseline) will be loaded and compared with the generated results. The unit test output will be printed on the console. 

## Classes 
#### Data_parser.py contains the class DataParser for dicom and contour parsing.
#### Data_loader.py contains the class BatchIterator for batch generating.
#### Verification_plotter.py contains the class OverlappingPlot for verification image generation.





# Questions and Answers

## Part 1

#### 1.How did you verify that you are parsing the contours correctly?

   The verification images were generated for all saved samples under the “visual_result‘’ folder. The images are overlapping images of dicom data, masks and contours. The correctness can be verified visually.

   Besides, unit tests were also added for two core parsing and saving functions to make sure future changes won’t affect the correctness. 
    
    
#### 2. What changes did you make to the code, if any, in order to integrate it into our production code base? 
 
   Change 1：In _parse_dicom_file(), I found the dicom files may not have rescaleIntercept and rescaleSlope attribute. I double checked using their dicom tag [0x0028, 0x1052] and [0x0028, 0x1053]. I still did not find the attributes. Therefore, I changed the code to try to read these tags first. If it fails, I set slope as 1 and intercept as 0 which means there is no change to the image data.

   Change 2: In _parse_contour_file(), I added "try ... except..." since some of the contour files failed the reading procedure. "None" will return if the reading fails

## Part 2

#### 1.Did you change anything from the pipelines built in Parts 1 to better streamline the pipeline built in Part 2? If so, what? If not, is there anything that you can imagine changing in the future?

   Yes. In the future, we may want to add, replace or even remove some samples from the parsing result we generated. We do not want to re-scan the whole database again and again. Therefore, I changed my pipleline and added the following functionalities:
- We can just run the same code on new dataset. The new samples will be added to the .h5 file.
- We can also run the same code to replace the exsiting dataset in the .h5 file with changed contouror dicom data.
- We can remove samples given the sample path as long as it follows the same naming rules. The function is data_parser::delete_sample()

#### 2.How do you/did you verify that the pipeline was working correctly?

   The verification images were generated for each batch under “visual_result" folder. The correctness can be verified visually. The images are overlapping images of dicom data and mask since we only load images and masks during the loading procedure. The image name starts with prefix “loader_”.

#### 3.Given the pipeline you have built, can you see any deficiencies that you would change if you had more time? If not, can you think of any improvements/enhancements to the pipeline that you could build in?

   I think we can improve the pipeline from following aspects:
- We can add data augmentation in the loading pipeline. For example, the we can add noise to the images or deform the image and contours. In this way, we can generate non-repeat training samples on the run.
- We can add some mechanism to keep some of the used training samples in the buffer and mix them with later training samples. Doing this can avoid the potential problem that later training samples may dominant the training procedure and make the model not fit for the early trained samples.

