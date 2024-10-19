# Cartographic Production - Campo Grande, Lisbon
**Institution**: Faculdade de Ciências da Universidade de Lisboa
**Course**: Cartographic Production  
**Project Date**: 2021
**Project Language**: Portuguese

## Project Overview
The main project objective was to produce a detailed 1:5000 scale map of the Campo Grande region in Lisbon using stereorestitution and 3D glasses in **PhotoMOD**. The project leveraged georeferenced imagery from the previous Photogrammetry class. The data was drawn with XYZ coordinates in PhotoMOD and later exported to **QGIS** for final adjustments and presentation. The final map adhered to the **Level of Detail 2 (NdD2)** standard established by the **Portuguese Directorate General for the Territory (DGT)**.

Additionally, a small Python code was developed to generate an **Orthophoto** using LiDAR data and aerial photography.

## Skills and Tools Used
- **Software**: PhotoMOD, QGIS, PostgreSQL, Python
- **Techniques**: Stereorestitution, georeferencing, map symbolization, orthophoto generation
- **Standards**: NdD2 (Level of Detail 2 by DGT)

## Key Results
- A **1:5000 scale map** of the Campo Grande region, complete with a detailed legend, accurate to NdD2 standards.
- Verification of data through PostgreSQL queries to ensure correct labeling and geometry attributes.
- A Python script to generate an orthophoto from aerial LiDAR and photography data.

### Key Features:
- Stereorestitution of XYZ data using 3D glasses in PhotoMOD.
- Final map presented with a legend and symbolization in QGIS.
- Orthophoto generation with a custom Python script.

## Project Structure
- `/map`: Final map in PDF or image format
- `/orthophoto`: Python script for orthophoto generation
- `/SQL_queries`: SQL validation
- `/presentation`: Slides used to present the project
- `/images`: Additional images of the project

---

The final map and orthophoto can be viewed in the `/map` folder, and the Python script used for generating the orthophoto can be found in the `/orthophoto` folder.
