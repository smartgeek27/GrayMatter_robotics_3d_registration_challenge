#!/usr/bin/env python3

#### DO NOT CHANGE THESE IMPORTS
import numpy
import time
import pathlib

####

#### TODO: ADD YOUR IMPORTS HERE
from pypointmatcher import pointmatcher as pm, pointmatchersupport as pms
####

 # TODO: Add your code here

# saving pointmatcher library and datapoints to variables.
PM = pm.PointMatcher
DP = PM.DataPoints
# parameters
Parameters = pms.Parametrizable.Parameters

# Defining registration model 

def model(data,ref):
    # extracting icp 
    icp = PM.ICP()
    params = Parameters()

    # Prepare reading filters to remove noise
    name = "MinDistDataPointsFilter"
    params["minDist"] = "1.0"
    minDist_read = PM.get().DataPointsFilterRegistrar.create(name, params)
    params.clear()

    name = "RandomSamplingDataPointsFilter"
    params["prob"] = "0.4"
    rand_read = PM.get().DataPointsFilterRegistrar.create(name, params)
    params.clear()

    # Preparing reference filters to remove noise
    name = "MinDistDataPointsFilter"
    params["minDist"] = "1.0"
    minDist_ref = PM.get().DataPointsFilterRegistrar.create(name, params)
    params.clear()

    name = "RandomSamplingDataPointsFilter"
    params["prob"] = "0.4"
    rand_ref = PM.get().DataPointsFilterRegistrar.create(name, params)
    params.clear()
    
    # defining matching algorithm

    name = "KDTreeMatcher"
    params["knn"] = "5"
    params["epsilon"] = "3"
    kdtree = PM.get().MatcherRegistrar.create(name, params)
    params.clear()
 
    # trimming outliers
    name = "TrimmedDistOutlierFilter"
    params["ratio"] = "0.9"
    trim = PM.get().OutlierFilterRegistrar.create(name, params)
    params.clear()

    # Error minimizing algorithm
    name = "PointToPointErrorMinimizer"
    pointToPoint = PM.get().ErrorMinimizerRegistrar.create(name)
    params.clear()

    # Defining iteration to perform transformation checker
    name = "CounterTransformationChecker"
    params["maxIterationCount"] = "150"
    maxIter = PM.get().TransformationCheckerRegistrar.create(name, params)
    params.clear()


    name = "DifferentialTransformationChecker"
    params["minDiffRotErr"] = "0.001"
    params["minDiffTransErr"] = "0.01"
    params["smoothLength"] = "4"
    diff = PM.get().TransformationCheckerRegistrar.create(name, params)
    params.clear()

    # inspecting NaN
    name = "NullInspector"
    nullInspect = PM.get().InspectorRegistrar.create(name)

    # Prepare transformation
    name = "RigidTransformation"
    rigid_trans = PM.get().TransformationRegistrar.create(name)
 
    # applying all the defined params and filters in the model.
    icp.readingDataPointsFilters.append(minDist_read)
    icp.readingDataPointsFilters.append(rand_read)
    icp.referenceDataPointsFilters.append(minDist_ref)
    icp.referenceDataPointsFilters.append(rand_ref)
    icp.matcher = kdtree
    icp.outlierFilters.append(trim)
    icp.errorMinimizer = pointToPoint
    icp.transformationCheckers.append(maxIter)
    icp.transformationCheckers.append(diff)
    icp.inspector = nullInspect
    icp.transformations.append(rigid_trans)
    # computing transformation matrix
    T = icp(data, ref)
    return T

###

# main function 
def main():
    data_list = ["bag", "basketball", "computercluster1", "corner2", "lab1", "sofalong", "sofawhole", "threechair","threemonitor"]

    # setting path location as there is only one file. No need to connect to parent class.
    repo_location = pathlib.Path(__file__).parent
    data_folder = repo_location / 'data'

    # creating dict to store error values
    Error={}
    for location in data_list:
        # accessing the files one by one.
        path_to_ply1 = data_folder / location / 'kinect.ply'
        path_to_ply2 = data_folder / location / 'sfm.ply'
        path_to_Tgt = data_folder / location / 'T_gt.txt'
        # timer
        start_time = time.time()
        # providing path and storing in numpy for ref and data.
        T_gt = numpy.loadtxt("../"+str(path_to_Tgt))
        data= DP(DP.load("../"+str(path_to_ply2)))
        ref=DP(DP.load(str("../"+str(path_to_ply1))))
        # calling the model
        T = model(data,ref)
        # calculating error values
        n=numpy.square(numpy.subtract(T, T_gt)).mean()
        # storing error values and compt time
        Error[location]=n,(time.time() - start_time)
    print(Error)


if __name__ == "__main__":
    main()
