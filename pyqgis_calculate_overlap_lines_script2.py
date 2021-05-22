import processing
from qgis.PyQt.QtCore import QVariant

# SET VARIABLES, FILE PATHS
overlay_layer = QgsProject.instance().mapLayersByName("route2")[0]
bottom_layer = QgsProject.instance().mapLayersByName("route1")[0]
overlap_undissolved = r'C:\Users\imper\Documents\python\calculate_overlap_lines\overlap.shp'
overlap_dissolved = r'C:\Users\imper\Documents\python\calculate_overlap_lines\overlap_dissolved.shp'

# CLIP OVERLAP
processing.run("native:clip", {'INPUT': bottom_layer, \
'OVERLAY': overlay_layer, \
'OUTPUT': overlap_undissolved})
#iface.addVectorLayer(overlap, '', 'ogr')

# DISSOLVE LAYERS
processing.run("native:dissolve", {'INPUT': overlap_undissolved, \
                                   'OUTPUT': overlap_dissolved})
iface.addVectorLayer(overlap_dissolved, '', 'ogr')

# CALCULATE LENGTH IN KM
layers = QgsProject.instance().mapLayers().values()
length_lyr_dict = {}
for layer in layers:
    features = layer.getFeatures()
    length_feat = []
    for f in features:
        geom = f.geometry()
        length = geom.length()/1000
        length_feat.append(length)
    length_lyr = sum(float(l) for l in length_feat)
    length_lyr_dict[layer.name()] = length_lyr
    print(str(layer.name()), ' is ', length_lyr, 'km long')

# ADD FIELDS
dissolved_lyr = QgsProject.instance().mapLayersByName('overlap_dissolved')[0]
pr = dissolved_lyr.dataProvider()
pr.addAttributes([QgsField("overlap_km", QVariant.Double, "double", 10, 3),
                  QgsField("ov_prc_r1", QVariant.Double, "double", 10, 3), 
                  QgsField("ov_prc_r2", QVariant.Double, "double", 10, 3)])
dissolved_lyr.updateFields()

# ADD ATTRIBUTES
with edit (dissolved_lyr):
    for f in dissolved_lyr.getFeatures():
        f['overlap_km'] = length_lyr_dict['overlap_dissolved']
        f['ov_prc_r1'] = (length_lyr_dict['overlap_dissolved']/length_lyr_dict['route1'])*100
        f['ov_prc_r2'] = (length_lyr_dict['overlap_dissolved']/length_lyr_dict['route2'])*100
    dissolved_lyr.updateFeature(f)
    print('Overlap percentage over route 1:', f['ov_prc_r1'], 'percent', '\n' \
          'Overlap percentage over route 2:', f['ov_prc_r2'], 'percent')
