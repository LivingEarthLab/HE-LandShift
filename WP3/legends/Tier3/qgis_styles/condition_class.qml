<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.28.0-Firenze" styleCategories="Symbology" hasScaleBasedVisibilityFlag="0" maxScale="0" minScale="1e+08">
  <pipe>
    <rasterrenderer type="paletted" band="1" opacity="1" alphaBand="-1" nodataColor="">
      <rasterTransparency/>
      <colorPalette>
        <paletteEntry value="0" label="Not assessed" color="#d9d9d9" alpha="255"/>
        <paletteEntry value="1" label="Degraded (score 1–2)" color="#d73027" alpha="255"/>
        <paletteEntry value="2" label="Moderate (score 3)" color="#fee08b" alpha="255"/>
        <paletteEntry value="3" label="Good (score 4–5)" color="#2ca25f" alpha="255"/>
      </colorPalette>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0" gamma="1"/>
    <huesaturation colorizeBlue="128" colorizeGreen="128" colorizeOn="0" colorizeRed="255" colorizeStrength="100" grayscaleMode="0" invertColors="0" saturation="0"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
