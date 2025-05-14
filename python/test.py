import sqlite3
from game_logic.Player import *
from game_logic.Pokemon import *
    
if __name__ == "__main__":
    player = Player()
    choice = input("[00]Do you want to create a new account? (y/n): ")
    username = input("[01]Enter your username: ")
    mdp = input("Enter your password: ")
    if choice == "y":
        player.register(username, mdp, random.randint(1, 1300))
    else:
        player.login(username, mdp)
    equipe = player.get_equipe()
    for i in range(len(equipe)):
        print(f"[{i + 1}] {equipe[i].pokemon_name} ({equipe[i].get_moves()})")
    item = player.get_item()
    for i in range(len(item)):
        print(f"[{i + 1}] {item[i][0]} ({item[i][1]})")


# Impact de la capture
# Impact des balls
# Les balls viennent multiplier le taux de rareté défini par le code du jeu. 

# Pokéball : 1
# Superball : 2
# Hyperball : 3
# Ultraball : 5 sur les Chimères, x0.25 sur le reste
# Masterball : 255 (ne peut échouer)
# Impact des PV
# Les PV restants influent énormément sur le calcul. La formule est basée sur : (2 - PV RESTANT / PV MAX) * 4.

 

# Impact du niveau
# Le niveau influe par un petit multiplicateur qui ajoute ou retire quelques pourcents. La formule est basée sur : 1 + ((100 - NIVEAU) / 100) / 4.

 

# Impact de la brillance
# La brillance ajoute 10% de chance aux Pokémon d'être capturés

 

# Impact aléatoire
# Une variable aléatoire existe et augmente ou diminue de 10% les chances de capture. 

 

# Impact du Pokédex
# L'impact du nombre de Pokémon vus dans le Pokédex a toujours été présent et est conservé des anciennes versions. Voici les taux influés : 

# Moins de 75 : 2
# Entre 75 et 150 : 1
# Entre 150 et 300 : 0.95
# Entre 300 et 500 : 0.88
# Plus de 500 : 0.8
# Impact des Pokémon
# Voici le fonctionnement de ces taux de capture : 

# Seul dans sa ligné (ni évo, ni pré-évo) : 3
# 1er niveau de la lignée : 4
# 2nd niveau de la lignée : 2
# Evolution finale de la lignée : 1
# Légendaire : 0.25
# Cas impossible à capturer (Méga-Evolution, etc) : 0
# Certains Pokémon peuvent déroger à cette règle, nous avons juste mis les cas principaux. 

 

# Formule
# Proba = 1 * {Pokemon} * {Ball} * {Shiney} * {Niveau} * {PV} * {Pokédex} * {Random}


# -------------------------------------------------------------------------------------------------
# https://www.pokepedia.fr/Exp%C3%A9rience
# Formules statiques
# Cette formule est utilisée dans les quatre premières générations. Relativement simple à appliquer, elle prend en compte le niveau du Pokémon vaincu, son expérience de base ainsi que le partage entre plusieurs participants au combat.

# E
# X
# P
# =
# a
# ×
# t
# ×
# b
# ×
# e
# ×
# N
# 7
# ×
# s

# Dans la sixième génération, la formule est modifiée pour prendre en compte l'affection du Pokémon, sa capacité à évoluer ainsi que les bonus d'expérience temporaires (comme les O-Auras).

# E
# X
# P
# =
# a
# ×
# t
# ×
# b
# ×
# e
# ×
# N
# ×
# p
# ×
# f
# ×
# v
# 7
# ×
# s

# Formules adaptatives
# Cette formule plus complexe tient compte du niveau du Pokémon recevant l'expérience. Un même Pokémon vaincu rapporte plus d'expérience aux Pokémon ayant un niveau plus faible. À l'inverse, les Pokémon de niveau plus élevé reçoivent moins d'expérience. Plus la différence de niveau est grande, plus l'effet est conséquent.

# Uniquement dans la cinquième génération, la formule utilisée est la suivante :

# E
# X
# P
# =
# (
# a
# ×
# b
# ×
# N
# 5
# ×
# s
# ×
# (
# 2
# ×
# N
# +
# 1
# 0
# N
# +
# N
# p
# +
# 1
# 0
# )
# 2
# ,
# 5
# +
# 1
# )
# ×
# t
# ×
# e
# ×
# p

# Depuis la septième génération, la formule est ajustée pour prendre en compte l'affection et les bonus temporaires. De plus, le paramètre a disparaît : cela implique que le même Pokémon, qu'il soit sauvage ou capturé par un Dresseur, rapporte désormais la même quantité d'expérience.

# E
# X
# P
# =
# (
# b
# ×
# N
# ×
# f
# ×
# v
# 5
# ×
# s
# ×
# (
# 2
# ×
# N
# +
# 1
# 0
# N
# +
# N
# p
# +
# 1
# 0
# )
# 2
# ,
# 5
# )
# ×
# t
# ×
# e
# ×
# p
# ×
# c

# Description des paramètres
# N est le niveau du Pokémon vaincu (ou capturé, à partir de la sixième génération).
# b est l'expérience de base rapportée par le Pokémon vaincu. Cette valeur change selon les espèces et selon les jeux.
# Np est le niveau du Pokémon recevant l'expérience.
# a vaut :
# 1,5 si le Pokémon vaincu est capturé par un Dresseur ;
# 1 s'il s'agit d'un Pokémon sauvage.
# t vaut :
# 1 si le Pokémon recevant l'expérience n'est pas échangé ;
# 1,5 si le Pokémon recevant l'expérience est échangé ;
# (Depuis la 4e génération) 1,7 si le Pokémon recevant l'expérience est échangé et issu d'un jeu d'une langue différente.
# e vaut :
# 1,5 si le Pokémon recevant l'expérience tient un Œuf Chance ;
# 1 sinon.
# s décrit le partage de l'expérience entre plusieurs Pokémon et l'utilisation du Multi Exp :
# Première génération :
# Si le Multi Exp n'est pas dans l'inventaire, s équivaut au nombre de participants non K.O. ;
# Si le Multi Exp est dans l'inventaire :
# Pour les Pokémon ayant participé au combat, s équivaut à 2 × nombre de participants non K.O. ;
# Pour toute l'équipe, s équivaut à 2 × nombre de participants non K.O. × nombre de Pokémon dans l'équipe.
# De la deuxième à la cinquième génération :
# Si aucun Pokémon de l'équipe ne tient de Multi Exp, s équivaut au nombre de participants non K.O. ;
# Si au moins un Pokémon tient un Multi Exp :
# Pour les Pokémon ayant participé au combat, s équivaut à 2 × nombre de participants non K.O. ;
# Pour les Pokémon qui tiennent un Multi Exp, s équivaut à 2 × nombre de Pokémon tenant un Multi Exp.
# À partir de la sixième génération :
# Pour les Pokémon ayant participé au combat, s vaut 1 ;
# Pour les Pokémon n'ayant pas participé au combat et si le Multi Exp est activé, s vaut 2.
# Note : Dans Pokémon Épée et Bouclier, l'objet Multi Exp n'existe pas à proprement parler, mais son effet est activé de manière permanente.
# p décrit le boost d'expérience temporaire produit par certains objets.
# Si aucun boost n'est actif, p vaut 1.
# Dans la cinquième génération, utilisez les Offri-Auras suivantes :
# Aura Expérience +++, S ou MAX : 2 ;
# Aura Expérience ++ : 1,5 ;
# Aura Expérience + : 1,2 ;
# Aura Expérience - : 0,8 ;
# Aura Expérience -- : 0,66 ;
# Aura Expérience --- : 0,5.
# Dans la sixième génération, utilisez les O-Auras suivantes :
# Aura Expérience N. 3 : 2 ;
# Aura Expérience N. 2 : 1,5 ;
# Aura Expérience N. 1 : 1,2.
# Dans Pokémon Ultra-Soleil et Ultra-Lune, utilisez une Motism'Aura Moti-Exp : p vaut alors 1,5.
# f décrit le bonus lié à l'affection du Pokémon :
# Si le Pokémon recevant l'expérience a un niveau d'affection assez élevé, f vaut 1,2 ;
# Sinon, f vaut 1.
# v décrit un bonus spécifique aux Pokémon capables d'évoluer par niveau :
# Si le Pokémon recevant l'expérience peut évoluer par niveau et s'il a un niveau supérieur ou égal au niveau requis pour évoluer, v vaut 1,5 ;
# Sinon, v vaut 1.
# c vaut :
# (Depuis Pokémon Épée et Bouclier) 1,5 si le Charme Exp est dans l'inventaire ;
# 1 sinon.
# Remarques
# Jusqu'à la cinquième génération, les quantités d'expérience sont calculées puis attribuées à partir de chaque Pokémon vaincu séparément. Dans le cas où un Pokémon éliminerait plusieurs ennemis en un coup lors d'un Combat Duo, il peut arriver que le Pokémon reçoive de l'expérience pour le premier K.O., monte de niveau puis reçoive à nouveau de l'expérience pour le second K.O. Cette montée de niveau a un impact sur le calcul pour le second K.O. dans les jeux utilisant une formule adaptative, car elle tient compte du nouveau niveau.

# Depuis la sixième génération, dans une situation équivalente, les quantités d'expérience pour chaque K.O. sont toutes calculées et additionnées avant d'être attribuées.

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#https://www.pokepedia.fr/Calcul_des_d%C3%A9g%C3%A2ts

# Données nécessaires
# Plusieurs données entrent en jeu dans la détermination des dégâts subis lors d'une attaque :

# le niveau (Niv) du Pokémon attaquant ;
# la statistique d'Attaque ou Attaque Spéciale (Att) du Pokémon attaquant ;
# la puissance de base (Pui) de la capacité utilisée, avec d'éventuels coefficients modificateurs comme la brûlure, la météo, Mur Lumière, Coup d'Main ou Peau Féérique.
# Si la capacité utilisée est une capacité Z, cette valeur est donc la valeur de la puissance de la capacité Z ;
# la statistique de Défense ou Défense Spéciale (Def) du Pokémon défenseur.
# Les statistiques qui entrent en jeu dans le calcul dépendent de la catégorie (physique ou spéciale) de la capacité.

# De plus, un coefficient multiplicateur (CM) s'applique et résulte de la multiplication des paramètres suivants :

# le STAB ;
# l'efficacité du type de la capacité ;
# un éventuel coup critique ;
# d'éventuels paramètres, comme un objet tenu, un talent, un climat ...
# un nombre généré aléatoirement compris entre 0.85 et 1.
# Formule mathématique
# La formule suivante permet de déterminer le nombre de PV perdus :

# P
# V
# p
# e
# r
# d
# u
# s
# =
# ⌊
# (
# ⌊
# ⌊
# ⌊
# N
# i
# v
# ×
# 0
# .
# 4
# +
# 2
# ⌋
# ×
# A
# t
# t
# ×
# P
# u
# i
# D
# e
# f
# ⌋
# 5
# 0
# ⌋
# +
# 2
# )
# ×
# C
# M
# ⌋

# À noter que chaque multiplication ou division est soumise à une partie entière[1]. Elles ont été omises dans l'exemple ci-après par souci de lisibilité.

# Exemple
# Un Zekrom de niveau 100 ayant 396 en Attaque utilise Éclair Croix, capacité de puissance 100 de catégorie Physique. La cible est un Reshiram ayant 299 en Défense. Aucun Pokémon n'a boosté l'une de ces stats auparavant, ni tient d'objet influant sur la capacité ou sa puissance. Leurs statistiques sont donc multipliées par 1, et la capacité n'a pas engendré de coup critique. Mais comme Éclair Croix est de même type que l'un des deux types de Zekrom (type Électrik), alors elle bénéficie du STAB, mais elle n'est pas très efficace sur Reshiram dû à la résistance du type Dragon au type Électrik. Le nombre maximal possible de PV perdus est donc :

# P
# V
# p
# e
# r
# d
# u
# s
# =
# ⌊
# (
# (
# 1
# 0
# 0
# ×
# 0
# .
# 4
# +
# 2
# )
# ×
# 3
# 9
# 6
# ×
# 1
# ×
# 1
# 0
# 0
# 2
# 9
# 9
# ×
# 1
# ×
# 5
# 0
# +
# 2
# )
# ×
# 1
# .
# 5
# ×
# 0
# .
# 5
# ×
# 1
# ⌋
# =
# 8
# 4
#  PV

# Dans ces conditions, Reshiram perd 84 PV.

# Cas particuliers
# Capacités OHKO
# Les capacités Abîme, Empal'Korne, Glaciation et Guillotine mettent toujours K.O. le Pokémon adverse lorsqu'elles réussissent. Cependant, elles ne touchent pas les Pokémon dont le type est immunisé au leur (Spectre pour Empal'Korne et Guillotine, Vol pour Abîme, Glace pour Glaciation depuis la septième génération).

# Fermeté, Ceinture Force et Bandeau
# Un Pokémon ayant le talent Fermeté, ou tenant une Ceinture Force conserve 1 PV s'il a son maximum de PV et est touché par une capacité supposée le mettre K.O. L'objet Bandeau permet aussi de conserver 1 PV, peu importe la quantité restante, mais avec un taux d'activation de 10%.

# Capacités à dégâts fixes
# Les capacités Sonicboom et Draco-Rage infligent un nombre fixe de dégâts (respectivement 20 et 40 PV). Cependant, elles ne touchent pas les Pokémon dont le type est immunisé au leur (Spectre pour Sonicboom et Fée pour Draco-Rage)*.

# Ombre Nocturne et Frappe Atlas
# Ces capacités, respectivement de Type Spectre et Combat, retirent des PV égaux au Niveau du lanceur à leur cible, sans tenir compte d'aucune statistique offensive ni défensive. Cependant, elle échoue sur les Pokémon immunisés aux capacités de leur Type (Normal pour Ombre Nocturne et Spectre pour Frappe Atlas).

# Capacités à puissance variable
# Certaines capacités voient leur caractéristique de puissance dépendre de critères déterminés lors de chaque utilisation, faisant que la puissance de la capacité n'est pas déterminée par une valeur fixe telle que vue plus haut. Sont dans ce cas :

# Vague Psy (varie entre 0.5× et 1.5× le niveau du lanceur) ;
# Gyroballe et Boule Élek (dépend de la Vitesse) ;
# Balayage, Nœud Herbe (dépend du poids de la cible) ;
# Tacle Feu et Tacle Lourd (dépend du poids du lanceur) ;
# Éruption et Giclédo (dépend des PV du lanceur) ;
# Croc Fatal, Essorage, Presse, Ire de la Nature, Cataclysme et Pression Extrême (dépend des PV de la cible) ;
# Frustration et Retour (dépend du bonheur du lanceur).
# Tricherie
# Tricherie utilise la statistique d'Attaque de la cible, et non celle du lanceur.

# Choc Psy, Frappe Psy et Lame Ointe
# Choc Psy, Frappe Psy et Lame Ointe, bien que spéciales, utilisent la statistique de Défense de la cible.

# Big Splash
# Big Splash utilise la statistique de Défense du lanceur au lieu de la statistique d'Attaque.

# --------------------------------------------------------------------------------------

#  https://www.pokepedia.fr/Statistique
# S
# t
# a
# t
# =
# ⌊
# ⌊
# (
# 2
# ×
# B
# a
# s
# e
# +
# I
# V
# +
# ⌊
# E
# V
# 4
# ⌋
# )
# ×
# N
# i
# v
# e
# a
# u
# 1
# 0
# 0
# +
# 5
# ⌋
# ×
# N
# a
# t
# u
# r
# e
# ⌋


# Voici la table pour l'Attaque, Défense, Attaque Spéciale, Défense Spéciale, et Vitesse :

# Diminution	Base	Augmentation
# Niveau	-6	-5	-4	-3	-2	-1	0	+1	+2	+3	+4	+5	+6
# Fraction	1/4	2/7	1/3	2/5	1/2	2/3	1	3/2	2	5/2	3	7/2	4
# Pourcentage	25 %	29 %	33 %	40 %	50 %	67 %	100 %	150 %	200 %	250 %	300 %	350 %	400 %
# Et voici celle pour Précision et Esquive :

# Diminution	Base	Augmentation
# Niveau	-6	-5	-4	-3	-2	-1	0	+1	+2	+3	+4	+5	+6
# Fraction	1/3	3/8	3/7	1/2	3/5	3/4	1	4/3	5/3	2	7/3	8/3	3
# Pourcentage	33 %	38 %	43 %	50 %	60 %	75 %	100 %	133 %	167 %	200 %	233 %	267 %	300 %


#https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_effort_value_yield_in_Generation_IX
