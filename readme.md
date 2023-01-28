The project aims to prepare the algorithm to register 2 point clouds of the similar object by means any registration algorithm or filters in libpointmatcher library. 

The folder contains 3 files: 
1. main.py -  Th working code file for the task, all the implementation can be seen in the To do section where the main() is called upon to load all the files of the test case and runs the model for point cloud registration.
2. results.txt - The best results can be seen in the results.txt file for each point cloud class. A evaluation method to compare the error between transformation matrix an the ground truth is proposed as in this ex :

'bag': (0.0015420208909381781, 0.5306024551391602).

The prior value shows the error , the later shows the computation time to run the algorith.

The error is computed by the means squared difference algorithm. The lower the value, more close the transformation matrix is to the ground truth. 
Observation: As evident in the results file 5/10 test cases passed completely with error values even less than 0.1. Also rest of the error values are less than 1 except "threemonitor" and "threechair". It is because the scanned 'sfm' and 'kinect' files are fairly unordered and individual filters cannot be applied to modify the test case files.


3. readme.txt - in it.
4. data- test files.

How to run:

1. install required dependencies 
2. Add path of file from data folder
3. run the code
4. Output - Error and computation time
            Transformation matrix



![image](https://user-images.githubusercontent.com/87424679/215289401-021f9700-98c2-434d-9f7b-935fb18c700e.png)
