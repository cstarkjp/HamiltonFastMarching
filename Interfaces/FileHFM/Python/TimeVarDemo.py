#!/usr/bin/env python3


"""
    This file demonstrates:
    - differentiation of the value function w.r.t to the inverse speed 
        (often referred to as the cost). If speed has a single component,
        then the result of can be regarded as a geodesic density.
    - time dependent speed function.
      Here speed is faster in the beginning (level lines are closer)
    - second order accuracy
    
    Command line (optional) arguments :
    - Path to executable
    - domain size
"""

import math
import numbers;
import numpy as np;
import os;
import sys
from operator import mul
from functools import reduce
from subprocess import call
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import FileIO

n = 100 if len(sys.argv)<=2 else int(sys.argv[2])

input = {
"sndOrder": 1,
"model": "IsotropicBox2<Boundary::Closed>",
"dims": np.array([n, n]),
"gridScale": 1./n,
"seeds": np.array([[0.5, 0.5],[0.7,0.8]]),
"exportValues": 1,

#speed=1 while t<=0.2, and speed=2 after t>=0.3, and speed varies linearly in between.
#Obviously if len(speed_times)==n+1, then speed_0,...,speed_n must be provided.
"speed_times": np.array([0.2, 0.3]),
"speed_0": 1,
"speed_1": 2,

#Compute the first order expansion of the arrival time at this point 
# w.r.t cost (=1/speed), seen as a global map
"inspectSensitivity": np.array([[1./6, 1./6],[1./6,1./2],[0.67,0.6]])
}

# Set to the directory containing ExternLFM executables FileLFM2D and FileLFM3D
path=os.getcwd()
if len(sys.argv) >=2:
    os.chdir(sys.argv[1])

#Write parameter file to disk, execute program, import results
FileIO.RulesToRaw(input,"input")
call('./FileHFM_Isotropic')
result = FileIO.RawToRules()

# Restore working directory
os.chdir(path)

#print(result['geodesicLengths'])
#geodesics = np.vsplit(result['geodesics'],result['geodesicLengths'].cumsum()[:-1])

with PdfPages("Output/TimeVar_results.pdf") as pdf:
    side = np.linspace(0., 1., n)
    X,Y=np.meshgrid(side,side)

    plt.figure()
    plt.title('Value map')
    cp = plt.contourf(X, Y, result["values"])
    plt.colorbar(cp)
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()
    
    plt.figure()
    plt.title('valueVariations_0')
    cp = plt.contourf(X, Y, result["valueSensitivity_0"])
    pdf.savefig()
    plt.close()

    plt.figure()
    plt.title('valueVariations_1')
    cp = plt.contourf(X, Y, result["valueSensitivity_1"])
    pdf.savefig()
    plt.close()

    plt.figure()
    plt.title('valueVariations_2')
    cp = plt.contourf(X, Y, result["valueSensitivity_2"])
    pdf.savefig()
    plt.close()

 
