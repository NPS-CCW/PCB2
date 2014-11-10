PCB2
=============

Workflow and scripts to support printed circuit board (PCB) milling with the Roland MDX-40A and PC-Board Cam software.

##Goal

We are trying to produce quick prototype single and double layer printed PCBs using a CNC mill and software provided by http://www.pdi3d.com/.

##Workflow

1. Produce a PCB design in Eagle.
2. Load the NPS-DAZL design rules.
3. Run Eagle DRC and correct any errors.  This will ensure the signals, pads and vias in the design meet dimensional constraints that can be cut on the mill.
4. Run Eagle 'Cam Processor' and produce files for the signal layers and drills/holes.
5. Launch PC-Board Cam and load the .gtl file output from the Cam Processor.
6. There is a scaling error in the drill locations coming out of Eagle.  Run the drill scaling command line script on the drill file output from Eagle.  This will rescale the drill and hole locations to match the dimensions of the signal layer.
7. Load the modified drill file into PC-Board Cam.
8. When you load the holes they will not line up with the pads in the signal layer.  Use the reference pads tool (bright pink circle targe in the toolbar) to align the two files.
9. For single sided boards consider flipping the file in PC-Board Cam.  This will allow you to install components on the substrate side of the board with through-hole components being soldered on the copper side.  Makes for much neater and easier to solder boards.
10. When things look good use the Maching > Mill... option in PC-Board Cam to output a G-Code file.  This G-Code file is the instruction set that will run on the Roland MDX-40A (or any other CNC mill).
11. BUT...the output from PC-Board Cam has integer values that will cause errors.  Feed rates and X, Y and Z axis coordinates cannot be integer values(i.e. F60 X20 will cause and error).  Integer valued quantities must include a trailing zero(i.e. F60.0 X20.0).  
12. Run the post-processing script on the output file to to correct all these coordinates.
