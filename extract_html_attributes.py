from qgis.PyQt.QtCore import QVariant
from bs4 import BeautifulSoup
import ast

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
    
def parse_string_type(string):
    "Return the appropriate field attribute type to use from the string value"
    try:
        eval_string = ast.literal_eval(string)
    
    except ValueError:
        return QVariant.String
    except SyntaxError:
        return QVariant.String
    else:
        if type(eval_string) in [int, long,  bool]:
            return QVariant.Int
        if type(eval_string) in [float]:
            return QVariant.Double
        else:
            return QVariant.String

# Work on the actively selected layer
layer = iface.activeLayer()

# Sample 20 features in the layer to find the new fields to add to the layer attribute table
new_fields = {}
# Determine list of features: if a selection exists or take all features in the layer
if layer.selectedFeatureCount() and layer.selectedFeatureCount() < 20:
    feature_list = layer.selectedFeatures() 
else:
    feature_list = layer.getFeatures(QgsFeatureRequest().setLimit(20))
    
for feature in feature_list: 
    new_fields.update(parse_HTML_attributes(feature))


try:
    with edit(layer):
        
        # Add the new string fields to the layer attribute table
        for key in new_fields:
            layer.addAttribute(QgsField(key, parse_string_type(new_fields[key])))
            print('Added new field', key, parse_string_type(new_fields[key]))
        
        # Build a list of features to update from the active selection
        feature_list = layer.selectedFeatures() or layer.getFeatures(QgsFeatureRequest())
        
        # Update the new attributes with the parsed HTML attributes
        for feature in feature_list:
            parsed_HTML_attributes = parse_HTML_attributes(feature)
            for key in parsed_HTML_attributes:
               feature[key] = parsed_HTML_attributes[key]
            layer.updateFeature(feature)
        print('Features updated')
        
except AssertionError:
    print('Please convert the layer into a QGIS editable format. Geopackage is recommended for fastest result')
