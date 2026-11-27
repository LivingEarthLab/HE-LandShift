<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.28.0-Firenze" styleCategories="Symbology" hasScaleBasedVisibilityFlag="0" maxScale="0" minScale="1e+08">
  <pipe>
    <rasterrenderer type="paletted" band="1" opacity="1" alphaBand="-1" nodataColor="">
      <rasterTransparency/>
      <colorPalette>
        <paletteEntry value="0" label="High deficit (&lt; 0.5)" color="#d73027" alpha="255"/>
        <paletteEntry value="1" label="Moderate deficit (0.5 – 1.0)" color="#fc8d59" alpha="255"/>
        <paletteEntry value="2" label="Balanced (1.0 – 1.5)" color="#fee090" alpha="255"/>
        <paletteEntry value="3" label="Surplus (&gt; 1.5)" color="#91bfdb" alpha="255"/>
      </colorPalette>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0" gamma="1"/>
    <huesaturation colorizeBlue="128" colorizeGreen="128" colorizeOn="0" colorizeRed="255" colorizeStrength="100" grayscaleMode="0" invertColors="0" saturation="0"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
