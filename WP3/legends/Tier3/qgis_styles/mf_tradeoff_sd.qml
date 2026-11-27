<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.28.0-Firenze" styleCategories="Symbology" hasScaleBasedVisibilityFlag="0" maxScale="0" minScale="1e+08">
  <pipe>
    <rasterrenderer type="singlebandpseudocolor" band="1" opacity="1" alphaBand="-1" nodataColor="" classificationMin="0.0" classificationMax="0.4">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader clip="0" colorRampType="INTERPOLATED" classificationMode="1" minimumValue="0.0" maximumValue="0.4" labelPrecision="4">
          <item alpha="255" value="0.0" label="0" color="#fcfdbf"/>
          <item alpha="255" value="0.1" label="0.1" color="#fc8961"/>
          <item alpha="255" value="0.2" label="0.2" color="#b73779"/>
          <item alpha="255" value="0.30000000000000004" label="0.3" color="#51127c"/>
          <item alpha="255" value="0.4" label="0.4" color="#000004"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0" gamma="1"/>
    <huesaturation colorizeBlue="128" colorizeGreen="128" colorizeOn="0" colorizeRed="255" colorizeStrength="100" grayscaleMode="0" invertColors="0" saturation="0"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
