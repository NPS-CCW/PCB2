PCB2
=============

Workflow and scripts to support printed circuit board (PCB) milling with the Roland MDX-40A and PC-Board Cam software.

##Goal

We are trying to quickly prototype single and double layer PCBs using a CNC mill and software tools.  This repo uses a tool chain composed of:
 - Eagle (Version 7.0.0 Lite)
 - PC-Board Cam (Version 8/10/2014)
 - Roland VPanel for MDX-40A
 - Custom Python scripts written for by DAZL makers.

##Preparation

**MDX-40A**

1. Turn on the MDX-40A and open V-panel.  Some configutration is required before commencing to work through the tool chain.
2. Ensure that coordinate system G54 is selected.
3. Load the 1/64" square end mill and set the zero height using the touch sensor.
4. 

**Workpiece**

1. Clean the copper surfaces of the PCB blank using sandpaper.   You want to remove any oxidation prior to milling.
2. Optionally, you can tin the surface to make soldering easier after milling.
3. Secure the workpiece in the jig.

##Workflow

1. Produce a PCB design in Eagle.
2. Load the NPS-DAZL design rules.
3. Run Eagle DRC and correct any errors.  This will ensure the signals, pads and vias in the design meet dimensional constraints that can be cut on the mill.
4. Run Eagle 'Cam Processor' and produce files for the signal layers and drills/holes.
5. Launch PC-Board Cam and load the .gtl file output from the Cam Processor.  Ensure there are no "Disabled" tracks that show up as brown signal paths.  To "Re-activate" these tracks right click and select "Re-enable Track net".  Small pads often go unnoticed as disabled at this stage so look closely.
6. For single sided boards consider flipping the file in PC-Board Cam.  This will allow you to install components on the substrate side of the board with through-hole components being soldered on the copper side.  Makes for much neater and easier to solder boards.
7. There is a scaling error in the drill locations coming out of Eagle.  Run the drill scaling command line script on the drill file output from Eagle.  This will rescale the drill and hole locations to match the dimensions of the signal layer.
8. Load the modified drill file into PC-Board Cam.  This is not trivial.  If you are asked to reduce the size of some drills to match their pads, choose "No".  If you are asked if this is a valid import, choose, "Yes".
9. To align the drills and holes to the signal layer select Display > Drills in the menu bar.  Then use the rotation commands in PC-Board Cam to get the drill and hole orientation rotated the same as the signal layer. 
10. Next you will notice that the holes do not lay over their corresponding pads in the signal layer.  Use the reference pads tool (bright pink circle targe in the toolbar) to align the two files.
11. Create the milling paths by reselecting the signal layer (usually layer #1) and clicking on Machine > Calculate Contours.  this step will take a moment to complete.  I find that I need to select Resolution > Medium in the pop-up window in order to cut paths betwen all the small signals using the 1/64 tool.
12. Hit the "Reframe" button to size the PCB based off the elements in your design.
13. Create a zero reference in the bottom left corner of the PCB by hovering over the "Reframe" button and then selecting the "Origin" tool.  Click "Plot Manually" and then click the bottom left corner of the reframed card.
14. In PC-Board Cam select Parameters > Selected Tools.  Ensure that the options match the tools image in this repo.
15. In PC-Board Cam select Parameters > Output data format.  Ensure the configuration option match the output image in this repo.  Then select your output filename and location next to the "Create File" radio button.  For standardization I usually use the following filenames
 - Signal layer: `signal.txt`
 - Drills with #65 bit: `65_drill.txt`
 - Drills with #58 bit: `58_drill.txt`
 - Drills with #44 bit: `44_drill.txt`
 - Outline and circular boring on large holes: `cutline.txt`
16. When things look good use the Maching > Mill... option in PC-Board Cam to output a G-Code file.  You should ensure the radio button in the bottom of this pop-up window is selected for "XY-zero point White Cross".  The G-Code file from this step is the instruction set that will run on the Roland MDX-40A (or any other CNC mill). BUT...the output from PC-Board Cam has integer values that will cause errors on the MDX-40A.  Feed rates and X, Y and Z axis coordinates cannot be integer values(i.e. F60 X20 will cause and error).  Integer valued quantities must include a trailing zero(i.e. F60.0 X20.0).  
17. Run the post-processing script on the output file to to correct all these coordinates.
18. Load the correct cutting tool into the mill, and reset the zero for the following conditions:
 - Any mill.  The mills are depth controlled and of variable length.  The zero must be reset for each mill that is loaded.
 - First drill bit.  Subsequent drill bits do not require the zero to be reset if they are all loaded where the depth ring is snugly against the collet.
19. Load the script and the correct cutter into the mill and output the program through the mill using V-panel.
20. Repeate this process from step 15 for each milling/drilling operation.
