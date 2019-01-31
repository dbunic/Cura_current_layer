# Cura PostProcessingPlugin
# Author:   Darko Bunic
# Web:      www.redips.net	
# Date:     January 22, 2019

# Description:  This plugin inserts a line at the start of each layer,
#               M117 - displays printing current layer of total layers
#               It is possible to change "Printing" label - Printing 3/126
#		Based on script DisplayFilenameAndLayerOnLCD.py of Amanda de Castilho


from ..Script import Script

class PrintCurrentLayer(Script):
	def __init__(self):
		super().__init__()

	def getSettingDataString(self):
		return """{
			"name":"Print current layer",
			"key": "PrintCurrentLayer",
			"metadata": {},
			"version": 2,
			"settings":
			{
				"name":
				{
					"label": "text to display:",
					"description": "Enter text to display for each layer",
					"type": "str",
					"default_value": "Printing"
				}
			}
		}"""


	def execute(self, data):
		# if input field is set
		if self.getSettingValueByKey("name") != "":
			name = self.getSettingValueByKey("name")
		# otherwise set default label
		else:
			name = "Printing"
   		# prepare M117 line
		m117 = "M117 " + name + " "
		# layer number
		i = 1
		# initialize total layers
		totalLayers = ""
		#
		# loop through layers
		#
		for layer in data:
			# add current layer number
			displayText = m117 + str(i)
			# set layer index
			layerIndex = data.index(layer)
			# split layer to lines
			lines = layer.split("\n")
			#
			# loop goes through all lines
			#
			for line in lines:
				# set total layers number
				if line.startswith(';LAYER_COUNT:'):
					totalLayers = line[13:]
				# append M117 after LAYER line in GCODE
				elif line.startswith(";LAYER:"):
					lineIndex = lines.index(line)
					lines.insert(lineIndex + 1, displayText + "/" + totalLayers)
					i += 1
			# join lines
			final_lines = "\n".join(lines)
			# update layer
			data[layerIndex] = final_lines
		# return modified data
		return data

