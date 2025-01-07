# PortholeReality-02
Calibration and rendering scripts for Porthole Reality. Unfortunately, "Windowed Reality," was too close to ,"Windows Reality," so I had some rebranding

\nStart in Main.py. This contains the script that handles socket communication.
\nKeypointDetector is responsible for detecting bright points on an image
\nStereoscopicCamera handles stereo images
\nTriangulation performs the actual triangulation of the stereo points

\n\nCameraCalibration is not ran in realtime and is solely used for getting the matrices needed for position triangulation
