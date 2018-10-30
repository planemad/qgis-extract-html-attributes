from qgis.PyQt.QtCore import QVariant
from bs4 import BeautifulSoup

# PyQGIS function to extract HTML attributes encoded in a string into seperate field
# Instructions to convert GeoRSS layers from Bhuvan GeoServer to GeoJSON. Customize the parse_HTML_attributes function for other sources  
# 1. Open the GeoRSS XML and save the layer as a GeoJSON
# 2. Select the GeoJSON layer in the layer list
# 3. Open `Plugins > Python Console`and run the script from the code editor
# 4. Open the layer attribute table to verify the parsed HTML values
# Processing can take around 1 minute for 5,000 features

def parse_HTML_attributes(feature):
    "Parse attributes encoded in a HTML string into a dictionary"
    parsed_attributes = {}
    
    # Locate the attribute with the HTML string
    attribute_HTML = BeautifulSoup(feature['description'])
    #print(attribute_HTML) # DEBUG
    
    # Loop through every list item to extract a key value pair
    for attribute_item in attribute_HTML.findAll('li'):
        parsed_attributes.update({attribute_item.find(class_='atr-name').text : attribute_item.find(class_='atr-value').text })
    
    return parsed_attributes

# Work on the actively selected layer
layer = iface.activeLayer()

with edit(layer):
    
    # Sample 20 features in the layer to find the new fields to add to the layer attribute table
    new_fields = {}
    for feature in layer.getFeatures(QgsFeatureRequest().setLimit(20)): 
        new_fields.update(parse_HTML_attributes(feature))
    
    # Add the new string fields to the layer attribute table
    for key in new_fields:
        layer.addAttribute(QgsField(key, QVariant.String))
        print('Added new field', key)
    
    # Update the new attributes with the parsed HTML attributes
    for idx, feature in enumerate(layer.getFeatures()):
        parsed_HTML_attributes = parse_HTML_attributes(feature)
        for key in parsed_HTML_attributes:
           feature[key] = parsed_HTML_attributes[key]
        layer.updateFeature(feature)
    print('Features updated')

 

