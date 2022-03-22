#!/usr/bin/env python3

#### DO NOT CHANGE THESE IMPORTS
import numpy
import time
import pathlib
####

#### TODO: ADD YOUR IMPORTS HERE
from pypointmatcher import pointmatcher as pm, pointmatchersupport as pms
####
PM = pm.PointMatcher
DP = PM.DataPoints
Parameters = pms.Parametrizable.Parameters

def model(data,ref):
    icp = PM.ICP()
    params = Parameters()
    # Prepare reading filters
    name = "MinDistDataPointsFilter"
    params["minDist"] = "1.0"
    minDist_read = PM.get().DataPointsFilterRegistrar.create(name, params)
    params.clear()

    name = "RandomSamplingDataPointsFilter"
    params["prob"] = "0.4"
    rand_read = PM.get().DataPointsFilterRegistrar.create(name, params)
    params.clear()

    # Prepare reference filters
    name = "MinDistDataPointsFilter"
    params["minDist"] = "1.0"
    minDist_ref = PM.get().DataPointsFilterRegistrar.create(name, params)
    params.clear()

    name = "RandomSamplingDataPointsFilter"
    params["prob"] = "0.4"
    rand_ref = PM.get().DataPointsFilterRegistrar.create(name, params)
    params.clear()

    name = "KDTreeMatcher"
    params["knn"] = "5"
    params["epsilon"] = "3"
    kdtree = PM.get().MatcherRegistrar.create(name, params)
    params.clear()

    name = "TrimmedDistOutlierFilter"
    params["ratio"] = "0.9"
    trim = PM.get().OutlierFilterRegistrar.create(name, params)
    params.clear()

    name = "PointToPointErrorMinimizer"
    pointToPoint = PM.get().ErrorMinimizerRegistrar.create(name)
    params.clear()


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

    name = "NullInspector"
    nullInspect = PM.get().InspectorRegistrar.create(name)

    # Prepare transformation
    name = "RigidTransformation"
    rigid_trans = PM.get().TransformationRegistrar.create(name)

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
    T = icp(data, ref)
    return T

def main():
    data_list = ["bag", "basketball", "computercluster1", "corner2", "lab1", "sofalong", "sofawhole", "threechair","threemonitor"]

    repo_location = pathlib.Path(__file__).parent
    data_folder = repo_location / 'data'


    Error={}
    for location in data_list:
        path_to_ply1 = data_folder / location / 'kinect.ply'
        path_to_ply2 = data_folder / location / 'sfm.ply'
        path_to_Tgt = data_folder / location / 'T_gt.txt'
        start_time = time.time()
        T_gt = numpy.loadtxt("../"+str(path_to_Tgt))
        # TODO: Add your code here
        data= DP(DP.load("../"+str(path_to_ply2)))
        print("../"+str(path_to_ply2))
        ref=DP(DP.load(str("../"+str(path_to_ply1))))
        T = model(data,ref)
        n=numpy.square(numpy.subtract(T, T_gt)).mean()
        Error[location]=n,(time.time() - start_time)
    print(Error)
if __name__ == "__main__":
    main()
