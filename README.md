# qgis-extract-html-attributes

A PyQGIS script to extract feature attributes encoded in an HTML string into the attribute table of a vector layer.

## Setup

**Requirements**

- QGIS 3.x
- python 3.6

**Dependencies**

- Install [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) `sudo pip3 install beautifulsoup4` 

## Usage

The script is customized to work with GeoRSS vector layers from [Bhuvan GeoServer](http://bhuvannuis.nrsc.gov.in/bhuvan/web/?wicket:bookmarkablePage=:org.geoserver.web.demo.MapPreviewPage) where the feature attributes are stored in the `description` field as an HTML list.

```
description = <h4>city_hq</h4><ul class="textattributes">
  <li><strong><span class="atr-name">name</span>:</strong> <span class="atr-value">Fatehgarh</span></li>
  <li><strong><span class="atr-name">level_</span>:</strong> <span class="atr-value">3.00000000000</span></li></ul>
```

1. Open the GeoRSS XML and save the layer as a GeoJSON
2. Select the GeoJSON layer in the layer list
3. Open `Plugins > Python Console`and run the script from the code editor
4. Open the layer attribute table to verify the parsed HTML values

For other sources, customize the `parse_HTML_attributes` functions
