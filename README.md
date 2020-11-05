# BlenderRenderTerrain
Guide to rendering large USGS DEM tiles using blender

If everything goes well, the output should look something like this:

![demo](demo.gif)

This project depends on:
* [Blender](https://www.blender.org/) for rendering
* [tin-terrain](https://github.com/heremaps/tin-terrain) for converting DEM .tif to 3D meshes
* [meshio](https://github.com/nschloe/meshio) for converting meshes from tin-terrain to more efficient file format
* [gdal](https://gdal.org/) for merging tiles
* [ffmpeg](https://ffmpeg.org/) for sequencing rendered images into video
