# Measure route overlap script in QGIS
This script measures the overlap between two lines by clipping the overlap and returning a line layer with a length field. It first snaps the two lines, clips the overlap, dissolves it, and adds a length field in meters.

There is no native tool that does this in QGIS if I'm not mistaken.

The tool is NOT made from scratch and can be made using the Graphical Modeler. However, this script was tweaked a bit to organize the forms and add more functionality soon.

### 1. Situation
This started from a task at work that required measuring the overlap between two transport routes. I didn't find any tool that did this and the only way to do it was to manually measure. I made a short PyQGIS script and then converted into a processing script later on.
![image](https://user-images.githubusercontent.com/63440740/119226802-8e50ef00-bb3d-11eb-9f4b-eb243b384e8a.png)

### 2. Screenshot of the processing script
![image](https://user-images.githubusercontent.com/63440740/119226872-d3752100-bb3d-11eb-8712-7f7441af9a35.png)

### 3. Result layer
Notice that the resulting layer is snapped completely to the reference layer. Snapping is needed before clipping to ensure the entire overlap is clipped and measured.
![image](https://user-images.githubusercontent.com/63440740/119226910-0ddebe00-bb3e-11eb-8f36-8aa0d74cad47.png)

### 4. Attribute table
![image](https://user-images.githubusercontent.com/63440740/119226923-1df69d80-bb3e-11eb-9d25-570b069dfd1b.png)

### 5. Improvements needed
1. The resulting layer should be named as `Overlap between line 1 and line 2`" instead of `Added geom info`,
2. the default `length` field should be named `length_km` and divide the value with 1000 to get the length in kilometers,
3. and add two fields named `ovp_perc1` and `ovp_perc2` which shows the overlap in percentage versus line 1 and line 2, respectively.
