
#intaller scikit-image
def copyTifFile(fichier, out="./"):
	return copyFilesSet(fichier, out, ["tif", "tiff", "tfw"])

def renameTifFile(fichier, out):
	return renameFileSet(fichier, out, ["tif", "tiff", "tfw"])
	
def affiche(image):
	im=io.imread(image)
	plt.title(image)
	plt.imshow(im, cmap=plt.cm.gray)
	plt.show()

def normalisation(inraster):

	MIN = np.amin(inraster)
	MAX = np.amax(inraster)
	print("NORMALISATION: Min="+str(MIN)+" max="+str(MAX))
	if ( float(MIN) == 0 and float(MAX) == 1):
		return inraster
	return ( (inraster - float(MIN)) / ( float(MAX) - float(MIN) ))

def normalisationTiff(intiff, outtiff):
	rast = litFichierTiff(intiff)[0]
	nrast = normalisation(rast)
	genereTiff(nrast, outtiff, modeletif=intiff)
	print("OUTPUT = "+outtiff)

def chercheTiff(fichier):
	return chercheFichierTiff(fichier)

def litValeursRaster(raster, nodata=-9999):
	rast=raster[raster!=nodata]
	min=np.amin(rast)
	max=np.amax(rast)
	moy=np.average(rast)
	print("MIN="+str(min)+"   MAX="+str(max)+"  MOY="+str(moy))
	return( (min, max, moy))


def filtreCirculaire(dim):
	weights = np.ones((dim, dim))
	centre = (dim - 1) / 2
	for i in range(dim):
		for j in range(dim):
			if ( sqrt( abs(i-centre)*abs(i-centre) + abs(j-centre) * abs(j-centre) ) > (centre) ):
				weights[i, j] = 0
	print(weights)
	return (weights)


def rasteriseShapeFile(fichier, inras, outras, field):

	if not isfile(fichier):
		print("Fichier shapefile "+fichier+" manquant : STOP")
		exit(0)
		
	if (not estChamp(fichier, field)):
		print(field+" n'est pas un champ de "+fichier+"  STOP")
		exit(0)

	if not isfile(inras):
		print("Fichier raster "+inras+" manquant : STOP")
		exit(0)
		
	print("ATTENTION VERIFIER LES FICHIERS SHAPE ! IL EST PREFERABLE QU'ILS NE SOIENT PAS 'MULTIPART'")
	print("IL PEUT AUSSI RESTER DE L'INFORMATION INVISIBLE ISSUE D'ANCIENS CROISEMENTS (OU SUPPRESSION DE POLYGONES) PAR EXEMPLE")
	print("ATTENTION AUX SHAPE AVEC DES TROUS ! IL RISQUE D'AFFECTER DES VALEURS ARBITRAIRES")
	print("VERIFIER SOIGNEUSEMENT LE RASTER EN SORTIE")

	if not (raw_input("Continuer (y/n) ?") == "y"):
		exit(0)
	
	burned = np.zeros(shape=(1,1,1))
	if (compareShapeFileEtRasterExtend(fichier, inras)):
	
		fi=inras.split("/")[-1]
		chem=inras.split(fi)[0]

		tmprast=chem+"tmp.tif"
		if isfile(tmprast) :
			supprime(tmprast)
			
		print("RASTERISATION")
		with rasterio.open(inras) as src:
			kwargs = src.meta.copy()
			kwargs.update({
				'nodata':-9999,
				'dtype':'float64',   #on force le type pour produire un raster de poids
	#			'driver': 'GTiff',
	#			'compress': 'lzw'
			})
			
			with rasterio.open(tmprast, 'w', **kwargs) as dst:
				with fiona.open(fichier, "r") as shapefile:
					out_arr = src.read(1)
					# # this is where we create a generator of geom, value pairs to use in rasterizing
					
					formes = ( (feature["geometry"], float(feature["properties"][field]) ) for feature in shapefile ) #c'est float, car il s'agit du raster de poids !!!! (reel)
					burned = features.rasterize(shapes=formes, fill=-9999, default_value=-9999, out=out_arr, transform=src.transform)
					shapefile.close()
					
				sortie = np.zeros(shape=(1,dst.meta['height'],dst.meta['width']))
				sortie[0] = burned
				dst.write(sortie)
				dst.close()

			src.close()
			
		masq = masque(fichier, tmprast, outras)
		if isfile(outras):
			if isfile(tmprast):
				supprime(tmprast)
		
		return masq

	return None

def masque(fichier, inrast, outrast):
	if not isfile(fichier):
		print("Fichier shapefile "+fichier+" manquant : STOP")
		exit(0)

	if not isfile(inrast):
		print("Fichier raster "+inras+" manquant : STOP")
		exit(0)
		
	out_image = np.zeros(shape=(1,1,1))
	with rasterio.open(inrast) as src:
		kwargs = src.meta.copy()

		kwargs.update({
			'nodata':-9999,
			'dtype':'float64',
#			'driver': 'GTiff',
#			'compress': 'lzw'
		})
		
		with rasterio.open(outrast, 'w', **kwargs) as dst:
			with fiona.open(fichier, "r") as shapefile:
				print("MASQUAGE")
				formesTotales = [feature["geometry"] for feature in shapefile]
				out_image, out_transform = mask(src, shapes=formesTotales, crop=False)
				sortie = np.zeros(shape=(1,dst.meta['height'],dst.meta['width']))
				sortie[0] = out_image
				dst.write(sortie)
				src.close()
				shapefile.close()
				dst.close()
				rasttmp = out_image[ out_image <> dst.meta['nodata'] ]
				print("MASQUED : MIN="+str(np.amin(sortie[0]))+" MAX="+str(np.amax(sortie[0]))+" MOY="+str(np.average(sortie[0])))

	return out_image


def rasteriseShapeFileInitial(fichier, outrast, resol):

	if not isfile(fichier):
		print("Fichier shapefile "+fichier+" manquant : STOP")
		exit(0)


	burned = np.zeros(shape=(1,1,1))
	l93= "+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
	

	with fiona.open(fichier, "r") as shapefile:
		xUL=shapefile.bounds[0]
		yUL=shapefile.bounds[3]
		xLR=shapefile.bounds[2]
		yLR=shapefile.bounds[1]
		
		transforme =  Affine.translation(xUL - (resol / 2), yUL - (resol / 2) ) * Affine.scale(resol, - resol)
		H = int((yUL-yLR)/resol)
		W = int((xLR-xUL)/resol)
		if (H<=0 or W<=0):
			print("ATTENTION, valeur negative de H="+str(H)+" ou W="+str(W)+" : STOP")
			shapefile.close()
			exit(0)
			
		with rasterio.open(
			outrast,
			'w',
			driver='GTiff',
			height=H,
			width=W,
			count=1,
			dtype=rasterio.float64,
			crs=l93,
			transform=transforme,
			nodata=0
			) as dst:

			# # this is where we create a generator of geom, value pairs to use in rasterizing
			print("RASTERISATION")
			formes = ( (feature["geometry"], 1.0) for feature in shapefile )
			burned = features.rasterize(shapes=formes, fill=0, default_value=0, out_shape=(H,W), transform=transforme)

			sortie = np.zeros(shape=(1,dst.meta['height'],dst.meta['width']))
			sortie[0] = burned
			dst.write(sortie)
			
			shapefile.close()
			dst.close()

	return burned


	
def compareShapeFileEtRasterExtend(fichier, inras):
	if not isfile(fichier):
		print("Fichier shapefile "+fichier+" manquant : STOP")
		return False

	if not isfile(inras):
		print("Fichier raster "+inras+" manquant : STOP")
		return False

	with fiona.open(fichier, "r") as shapefile:
		with rasterio.open(inras) as src:

			if ( src.bounds.left>shapefile.bounds[2] or src.bounds.right < shapefile.bounds[0] or  src.bounds.top < shapefile.bounds[1] or src.bounds.bottom > shapefile.bounds[3]):
				print("Raster bounds    : "+str(src.bounds))
				print("Shapefile bounds : "+str(shapefile.bounds))
				print("Erreur : le raster de reference "+inras+" n'est pas recouvert par le shapefile "+fichier)
				shapefile.close()
				src.close()
				return False
				
			if ( src.bounds.left < shapefile.bounds[0] or src.bounds.right > shapefile.bounds[2] or  src.bounds.top > shapefile.bounds[3] or src.bounds.bottom < shapefile.bounds[1]):
				dx=0
				if (src.bounds.left - shapefile.bounds[0]) < 0 : 
					dx = shapefile.bounds[0] - src.bounds.left
				if (shapefile.bounds[2] - src.bounds.right) < 0 :
					dx += (src.bounds.right - shapefile.bounds[2])
				txdx = ( dx / float(src.bounds.right - src.bounds.left)) * 100.0
				dy=0
				if (src.bounds.top - shapefile.bounds[3]) > 0:
					dy=src.bounds.top - shapefile.bounds[3]
				if (src.bounds.bottom - shapefile.bounds[1]) < 0:
					dy+=(shapefile.bounds[1] - src.bounds.bottom)
				txdy = ( dy / float(src.bounds.top - src.bounds.bottom)) * 100.0
				
				print("Raster bounds    : "+str(src.bounds))
				print("Shapefile bounds : "+str(shapefile.bounds))
				print("Decalage en X :"+str(txdx)+"%  Decalage en Y :"+str(txdy)+"%")
				
				if not (raw_input("WARNING (outils.py:rasterize):  le raster de reference "+inras+" n'est que partiellement recouvert par le shapefile "+fichier+")! Continuer (y/n) ?") == "y"):
					shapefile.close()
					src.close()
					return False

			return True


def bufferRasterDistance(fichier, outfi, distance=50):
	fichier = chercheFichierTiff(fichier)
	tmpdist = radical(fichier)+"tmpdist.tif"
	print("Calcul du raster de distance total "+tmpdist)
	distanceGDAL(fichier, tmpdist)
	lst = litFichierTiff(tmpdist)
	raster = lst[0]
	outrast = np.zeros( shape = (lst[2], lst[1]) )
	outrast[ raster <= distance ] = raster[ raster <= distance ]
	outrast[ raster > distance ] = lst[10]
	genereTiff(outrast, outfi, listeparams = lst)

def maximumRasters(fichier1, fichier2, outfi):
	lst1 = litFichierTiff(fichier1)
	lst2 = litFichierTiff(fichier2)
	raster1 = lst1[0]
	raster2 = lst2[0]
	outrast = np.zeros( shape=(lst1[2], lst1[1]) )
	outrast = np.maximum(raster1, raster2)
	genereTiff(outrast, outfi, listeparams = lst1)

def miseAUn(fichier1, fichier2, outfi):
	lst1 = litFichierTiff(fichier1)
	lst2 = litFichierTiff(fichier2)
	rast1 = lst1[0]
	rast2 = lst2[0]
	outrast = np.zeros(shape=(lst1[2], lst1[1]))
	outrast = rast1
	outrast[ rast2 > 0 ] = 1
	genereTiff(outrast, outfi, modeletif=fichier1)

def metNoDataAZero(fichier, outfi, nodata=-9999):
	lst = litFichierTiff(fichier)
	rast = lst[0]
	outrast = np.zeros(shape=(lst[2], lst[1]))
	nodat=nodata
	try:
		nodat=float(lst[10])
		if (nodat != nodata):
			if not (raw_input("Confirmez nodata :"+str(nodata)+" (y/n)?")):
				exit(0)
	except:
		pass
	outrast=rast
	outrast[rast==nodat]=0
	genereTiff(outrast, outfi, modeletif=fichier)
	
def upDateTiffSup0(fichier, updatefi, outfi):
	lesInputs = rabotePartieCommuneRaster([fichier, updatefi])
	outrast=lesInputs[0][0]
	outrast[ (lesInputs[1][0]>0) ] = lesInputs[1][0][ (lesInputs[1][0] >0) ]
	xul=lesInputs[0][4]
	yul=lesInputs[0][5]
	resol=lesInputs[0][10]
	genereTiff(outrast, outfi, xul, yul, resol)
	
def upDateNotNoData(fichier, updatefi, outfi, nodata=-9999):
	lst = litFichierTiff(fichier)
	rast = lst[0]
	outrast = np.zeros(shape=(lst[2], lst[1]))
	lst2 = litFichierTiff(udatefi)
	urast=lst2[0]
	nodat=nodata
	try:
		nodat=float(lst2[10])
		if (nodat != nodata):
			if not (raw_input("Confirmez nodata :"+str(nodata)+" (y/n)?")):
				exit(0)
	except:
		pass
	outrast=rast
	outrast[urast!=nodat]=urast[urast!=nodat]
	genereTiff(outrast, outfi, modeletif=fichier)
	
#version avec les windoows
		# windows = src.block_windows(1)
		# with rasterio.open(outras, 'w', **kwargs) as dst:
			# with fiona.open(fichier, "r") as shapefile:
			
				# if ( src.bounds.left>shapefile.bounds[2] or src.bounds.right < shapefile.bounds[0] or  src.bounds.top < shapefile.bounds[1] or src.bounds.bottom > shapefile.bounds[3]):
					# print("Raster bounds    : "+str(src.bounds))
					# print("Shapefile bounds : "+str(shapefile.bounds))
					# print("Erreur : le raster de reference "+inras+" n'est pas recouvert par le shapefile "+fichier)
					# shapefile.close()
					# dst.close()
					# src.close()
					# exit(0)
				# if ( src.bounds.left < shapefile.bounds[0] or src.bounds.right > shapefile.bounds[2] or  src.bounds.top > shapefile.bounds[3] or src.bounds.bottom < shapefile.bounds[1]):
					# print("Raster bounds    : "+str(src.bounds))
					# print("Shapefile bounds : "+str(shapefile.bounds))
					# if not (raw_input("WARNING (outils.py:rasterize):  le raster de reference "+inras+" n'est que partiellement recouvert par le shapefile "+fichier+")! Continuer (y/n) ?") == "y"):
						# shapefile.close()
						# dst.close()
						# src.close()
						# exit(0)
						
				# print(dst.meta['dtype'])
				# print(type(int('13280')))
				# for idx, window in windows:					#windows est suelement une histoire de pixels (pas de georef)!
					# out_arr = src.read(1, window=window)
					# #this is where we create a generator of geom, value pairs to use in rasterizing
					# formes = ( (feature["geometry"], long(feature["properties"][field]) ) for feature in shapefile )
					# #shapes = ((geom,value) for geom, value in zip(shapefile["geometry"], shapefile[field]))		#pour acceder au field
					# burned = features.rasterize(shapes=formes, fill=0, out=out_arr, transform=src.transform)
					# #burned = features.rasterize(shapes=formes, fill=0, out_shape=osh, transform=src.transform)
					# #burned = features.rasterize(shapes=formes, fill=0, out_shape=osh, transform=src.transform)
					# print(src.transform)
					# print("Out array:")
					# #print(out_arr)
					# print("BURNED:")
					# #print(burned)
					# #dst.write_band(1, burned, window=window)

	#return burned