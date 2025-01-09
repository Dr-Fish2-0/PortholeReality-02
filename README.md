# PortholeReality-02
Calibration and rendering scripts for Porthole Reality. Unfortunately, "Windowed Reality," was too close to ,"Windows Reality," so I had some rebranding

Start in Main.py. This contains the script that handles socket communication.

KeypointDetector is responsible for detecting bright points on an image

StereoscopicCamera handles stereo images

Triangulation performs the actual triangulation of the stereo points

CameraCalibration is not ran in realtime and is solely used for getting the matrices needed for position triangulation

EditProjectionMatrix.cs is the code used by Unity3D to match the viewers perspective
