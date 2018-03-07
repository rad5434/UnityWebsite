# UnityWebsite
This repo contains code for the website that we built to connect with the Unity Game Engine and a local computer. The purpose of the website was to show how computer generated sketches that are trained based on human generated sketches, work in a "real world" simulation. We also show that over time, if we keep testing on newer boats and update the training data using the boats that were succesful in the Unity environment, we will be able to generate boats that are always successful. The website is still under construction as a result, some things may not work at times. We stream Unity from AppStream 2.0 of AWS which is expensive so we turn it on only during demos. If you want to see the complete working of the website, click on the "Website Tutorial" button on the top right corner of the website.

Following is the description of what each file does:
1) Website.py - Has flask framework that was used to host the website
2) static/js - Contains the p5 library that we modified. Also contains the sketch.js file that is used by the website to draw and send/recieve data
3) UnityDB.py - Has a Flask server and 2 MongoDB databases to share data between Unity and the website
4) mongodb.py - Contains the Flask server and MongoDB database that shares data between the local computer and the website
