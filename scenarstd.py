import parametres as param
#ls=param.dictSources
#lf=param.dictFacteurs
surfContiMin = 10000 #m2 surface minimale des continua
routesSearchRadius = 100

facteursIgnition="ignition.tab=7" #cela veut dire que la table ingnition.tab doit contenir 7 facteurs (a des fins de verification)


# facteursEclosion = (
# ("fVe", "Effet du facteur agregation de la vegetation sur l'eclosion" ,1, ls["vege"], [(0,0), (1,1), (2,5), (3,4)] ),					#0: non combustible, 1: agregation faible, 2:agregation moyenne, 3:agregation forte
# ("fBe", "Effet du facteur densite du bati sur l'eclosion", 0.3, ls["bati"], [(0,5), (1,4), (2,3), (3,2), (4,1), (5,0)] ),		#0: hors interface, 1: bati isole, 2:bati diffus, 3:bati agrege dense, 4:bati agrege tres dense, 5:bati continu
# ("fNe", "Effet du facteur classe d'occupation du sol sur l'eclosion",0.2, ls["typeocsol"], [(0,0), (1,1), (2,4), (3,5)] ),					#0:zones incombsutibles, 1:zones combustibles artificialisees, 2:zones agricoles, 3:zones naturelles
# ("fDEBe", "Effet du facteur niveau de debroussaillement sur l'eclosion", 1, ls["nivdeb"], [(0,5), (1,4), (2,3), (3,2), (4,1), (5,0)] ),	#0 non deb, 1:faible debroussaille, 2:insuffi debroussaille, 3:moyen, 4:fort, 5:max
# ("fPe", "Effet du facteur pente sur l'eclosion", 0.8, ls["pente"], [[-1,2,0],[2,5,1],[5,15,2], [15,30,3],[30,45,4], [45, 100, 5]] ),		#Classes de pentes (directement sur la carte des pente en degre
# ("fASPe", "Effet du facteur orientation sur l'eclosion", 0.4, ls["ori"], [[-1,0,2],[0,45,1],[45,135,2], [135,225,4],[225,315,3], [315, 360, 1]]  ),		#ASPECT : uniquement frais/chaud 0:plat, 1:Nord, 2:Est, 3:WEST, 4:SUD 
# ("fVENTe", "Effet du facteur vent sur l'eclosion", 0.9, ls["vent"], "" ),	#InitialiseVent, produit directement un raster de type facteur : Classes de VENT local (vitesse max * angle vente/pente : voir module d'initialisation de la variable) 
# )
facteursEclosion="eclosion.tab=7"

# facteursIntensite = (
# ("fVipl", "Effet du facteur agregation de la vegetation sur l'intensite" ,1, ls["vege"], [(0,0), (1,1), (2,5), (3,4)] ),						#0: non combustible, 1: agregation faible, 2:agregation moyenne, 3:agregation forte
# ("fBipl", "Effet du facteur densite du bati sur l'l'intensite", 0.3, ls["bati"], [(0,5), (1,4), (2,3), (3,2), (4,1), (5,0)] ),				#0: hors interface, 1: bati isole, 2:bati diffus, 3:bati agrege dense, 4:bati agrege tres dense, 5:bati continu
# ("fNipl", "Effet du facteur classe d'occupation du sol sur l'intensite",0.2, ls["typeocsol"], [(0,0), (1,1), (2,4), (3,5)] ),					#0:zones incombsutibles, 1:zones combustibles artificialisees, 2:zones agricoles, 3:zones naturelles
# ("fDEBipl", "Effet du facteur niveau de debroussaillement sur l'intensite", 1, ls["nivdeb"], [(0,5), (1,4), (2,3), (3,2), (4,1), (5,0)] ),	#0 non deb, 1:faible debroussaille, 2:insuffi debroussaille, 3:moyen, 4:fort, 5:max
# ("fPipl", "Effet du facteur pente sur l'intensite", 0.9, ls["pente"], [[-1,2,0],[2,5,1],[5,15,2], [15,30,3],[30,45,4], [45, 100, 5]] ),		#Classes de pentes (directement sur la carte des pente en degre
# ("fASPipl", "Effet du facteur orientation sur l'intensite", 0.5, ls["ori"], [[-1,0,2],[0,45,1],[45,135,2], [135,225,4],[225,315,3], [315, 360, 1]]  ),		#ASPECT : uniquement frais/chaud 0:plat, 1:Nord, 2:Est, 3:WEST, 4:SUD 
# ("fVENTipl", "Effet du facteur vent sur l'intensite", 1, ls["vent"], "" ),																	#InitialiseVent, produit directement un raster de type facteur, entre 0 et 1 : Classes de VENT local (vitesse max * angle vente/pente : voir module d'initialisation de la variable) 
# )
facteursIntensite="intensite.tab=7"

#somme des aleas d'eclosion sur le meme continuum
# facteursPropagationSubie = (
# ("fVp", "Effet du facteur agregation de la vegetation sur l'eclosion" ,1, ls["vege"], [(0,0), (1,1), (2,5), (3,4)] ),					#0: non combustible, 1: agregation faible, 2:agregation moyenne, 3:agregation forte
# ("fBp", "Effet du facteur densite du bati sur l'eclosion", 0.3, ls["bati"], [(0,5), (1,4), (2,3), (3,2), (4,1), (5,0)] ),		#0: hors interface, 1: bati isole, 2:bati diffus, 3:bati agrege dense, 4:bati agrege tres dense, 5:bati continu
# ("fNp", "Effet du facteur classe d'occupation du sol sur l'eclosion",0.2, ls["typeocsol"], [(0,0), (1,1), (2,4), (3,5)] ),					#0:zones incombsutibles, 1:zones combustibles artificialisees, 2:zones agricoles, 3:zones naturelles
# ("fDEBp", "Effet du facteur niveau de debroussaillement sur l'eclosion", 0.7, ls["nivdeb"], [(0,5), (1,4), (2,3), (3,2), (4,1), (5,0)] ),	#0 non deb, 1:faible debroussaille, 2:insuffi debroussaille, 3:moyen, 4:fort, 5:max
# ("fPp", "Effet du facteur pente sur l'eclosion", 0.9, ls["pente"], [[-1,2,0],[2,5,1],[5,15,2], [15,30,3],[30,45,4], [45, 100, 5]] ),		#Classes de pentes (directement sur la carte des pente en degre
# ("fASPp", "Effet du facteur orientation sur l'eclosion", 0.5, ls["ori"], [[-1,0,2],[0,45,1],[45,135,2], [135,225,4],[225,315,3], [315, 360, 1]]  ),		#ASPECT : uniquement frais/chaud 0:plat, 1:Nord, 2:Est, 3:WEST, 4:SUD 
# ("fVENTp", "Effet du facteur vent sur l'eclosion", 1, ls["vent"], "" ),	#InitialiseVent, produit directement un raster de type facteur, entre 0 et 1 : Classes de VENT local (vitesse max * angle vente/pente : voir module d'initialisation de la variable) 
# )
facteursPropagationSubie="propagationSubie.tab=7"

#aleas d'eclosion local * somme des intensites locales sur le meme continuum
# facteursPropagationInduite = (
# ("fVi", "Effet du facteur agregation de la vegetation sur l'ignition", 1, ls["vege"], (0,0), (1,5), (2,5), (3,5) ),					#0: non combustible, 1: agregation faible, 2:agregation moyenne, 3:agregation forte
# ("fBi", "Effet du facteur densite du bati sur l'ignition", 0.8, ls["bati"], (0,0), (1,2), (2,3), (3,4), (4,5), (5,0) ),		#0: hors interface, 1: bati isole, 2:bati diffus, 3:bati agrege dense, 4:bati agrege tres dense, 5:bati continu
# ("fRi", "Effet du facteur (distance d'une route * importance de la route) sur l'ignition", 1, "route", (0,0), (1,1), (2,2), (3,3), (4,4), (5,5) ),		#classes de routes
# ("fNi", "Effet du facteur classe d'occupation du sol sur l'ignition", 0.3, "typeocsol", (0,0), (1,1), (2,5), (3,4) ),					#0:zones incombsutibles, 1:zones combustibles artificialisees, 2:zones agricoles, 3:zones naturelles
# ("fDEBi", "Effet du facteur niveau de debroussaillement sur l'ignition", 0.9, "nivdeb", (0,5), (1,4), (2,3), (3,2), (4,1), (5,0) ),	#0 non deb, 1:faible debroussaille, 2:insuffi debroussaille, 3:moyen, 4:fort, 5:max
# ("fVe", "Effet du facteur agregation de la vegetation sur l'eclosion" ,1, "vege", (0,0), (1,1), (2,5), (3,4) ),					#0: non combustible, 1: agregation faible, 2:agregation moyenne, 3:agregation forte
# ("fBe", "Effet du facteur densite du bati sur l'eclosion", 0.3, "bati", (0,5), (1,4), (2,3), (3,2), (4,1), (5,0) ),		#0: hors interface, 1: bati isole, 2:bati diffus, 3:bati agrege dense, 4:bati agrege tres dense, 5:bati continu
# ("fNe", "Effet du facteur classe d'occupation du sol sur l'eclosion",0.2, "typeocsol", (0,0), (1,1), (2,4), (3,5) ),					#0:zones incombsutibles, 1:zones combustibles artificialisees, 2:zones agricoles, 3:zones naturelles
# ("fDEBe", "Effet du facteur niveau de debroussaillement sur l'eclosion", 1, "nivdeb", (0,5), (1,4), (2,3), (3,2), (4,1), (5,0) ),	#0 non deb, 1:faible debroussaille, 2:insuffi debroussaille, 3:moyen, 4:fort, 5:max
# ("fPe", "Effet du facteur pente sur l'eclosion", 0.8, "pente", (0,0), (1,3), (2,4), (3,4), (4,5), (5,5) ),		#Classes de pentes (voir les macro d'initialisation pour la specificattion des classes
# ("fASPe", "Effet du facteur orientation sur l'eclosion", 0.4, "ori", (0,0), (1, 1), (2, 2), (3, 3), (4,5),  ),		#ASPECT : uniquement frais/chaud 0:plat, 1:Nord, 2:Est, 3:WEST, 4:SUD 
# ("fVENTe", "Effet du facteur vent sur l'eclosion", 0.9, "vent", (0,0), (1,2), (2,3), (3,4), (4,5), (5,5) ),	#Classes de VENT local (vitesse max * angle vente/pente : voir module d'initialisation de la variable) 
# ("fVp", "Effet du facteur agregation de la vegetation sur la propagation" ,1, "vege", (0,0), (1,1), (2,3), (3,5) ),					#0: non combustible, 1: agregation faible, 2:agregation moyenne, 3:agregation forte
# ("fBp", "Effet du facteur densite du bati sur la propagation", 0.4, "bati", (0,5), (1,4), (2,3), (3,2), (4,1), (5,0) ),		#0: hors interface, 1: bati isole, 2:bati diffus, 3:bati agrege dense, 4:bati agrege tres dense, 5:bati continu
# ("fNp", "Effet du facteur classe d'occupation du sol sur la propagation",0.6, "typeocsol", (0,0), (1,1), (2,3), (3,5) ),					#0:zones incombsutibles, 1:zones combustibles artificialisees, 2:zones agricoles, 3:zones naturelles
# ("fDEBp","Effet du facteur niveau de debroussaillement sur la propagation", 1, "nivdeb", (0,5), (1,4), (2,3), (3,2), (4,1), (5,0) ),	#0 non deb, 1:faible debroussaille, 2:insuffi debroussaille, 3:moyen, 4:fort, 5:max
# ("fPp", "Effet du facteur pente sur la propagation", 0.9, "pente", (0,0), (1,3), (2,4), (3,4), (4,5), (5,5) ),		#Classes de pentes (voir les macro d'initialisation pour la specificattion des classes
# ("fASPp","Effet du facteur orientation sur la propagation", 0.5, "ori", (0,0), (1, 1), (2, 2), (3, 3), (4,5),  ),		#ASPECT : uniquement frais/chaud 0:plat, 1:Nord, 2:Est, 3:WEST, 4:SUD 
# ("fVENTp", "Effet du facteur vent sur l'eclosion", 0.9, "vent", (0,0), (1,2), (2,3), (3,4), (4,5), (5,5) ),	#Classes de VENT local (vitesse max * angle vente/pente : voir module d'initialisation de la variable) 
# ("fVipl", "Effet du facteur agregation de la vegetation sur l'intensite potentielle locale", 1, "vege", (0,0), (1,1), (2,4), (3,5) ),					#0: non combustible, 1: agregation faible, 2:agregation moyenne, 3:agregation forte
# ("fBipl", "Effet du facteur densite du bati sur l'intensite potentielle locale", 0.4, "bati", (0,5), (1,4), (2,3), (3,2), (4,1), (5,0) ),		#0: hors interface, 1: bati isole, 2:bati diffus, 3:bati agrege dense, 4:bati agrege tres dense, 5:bati continu
# ("fPipl","Effet du facteur pente sur l'intensite potentielle locale", 0.6, "pente", (0,0), (1,3), (2,4), (3,4), (4,5), (5,5) ),		#Classes de pentes (voir les macro d'initialisation pour la specificattion des classes
# ("fASPipl", "Effet du facteur orientation sur l'intensite potentielle locale", 0.5, "ori", (0,0), (1, 1), (2, 2), (3, 3), (4,5),  ),		#ASPECT : uniquement frais/chaud 0:plat, 1:Nord, 2:Est, 3:WEST, 4:SUD 
# ("fVENTipl", "Effet du facteur vent sur l'intensite potentielle locale", 0.8, "vent", (0,0), (1,2), (2,3), (3,4), (4,5), (5,5) ),	#Classes de VENT local (vitesse max * angle vente/pente : voir module d'initialisation de la variable) 
# ("fDEBipl", "Effet du facteur niveau de debroussaillement sur l'intensite potentielle locale", 0.8, "nivdeb", (0,5), (1,4), (2,3), (3,2), (4,1), (5,0) ),	#0 non deb, 1:faible debroussaille, 2:insuffi debroussaille, 3:moyen, 4:fort, 5:max
# ("fBelu", "?", 1, "elu", (0,0), (1,5), (2,4), (3,3), (4,1)  ),
# ("fBdeb", "?", 1, "deb", (0,0), (1,2), (2,3), (3,4), (4,5)  )
# )
facteursPropagationInduite="propagationInduite.tab=7"