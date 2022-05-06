ws="/content/contenu/" #repete dans prepareDonneesLineaires
chemTables="/content/tablesscenarstd/"
scenario="scenarstd"

resol=10

refrast = ws+"zone.tif"
contours=ws+"contours.shp"
srcStd="BDTOPO"
igni="igni"
champPoids="w"
srcIgni=srcStd

raddebrou="debrou"+srcStd
radvf="Vf"+srcStd
radrte="Rte"+srcStd
radbati="Bati"+srcStd
champPoidsIgni=champPoids+"-"+igni   #w-igni

carteIgnition="ignition.tif"

ignitionsConstantes=["igniSurBati", "igniSurRoutes"]
