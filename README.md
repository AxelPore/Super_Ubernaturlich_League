# Super_Ubernaturlich_League

---

# Présentation

```
Super Ubernaturlich League (ou SUL) est un jeu multijoueur reprenant le principe du jeu Pokemon.

Les joueurs seront donc sur une même map, un même monde dans lequel ils pourront explorer le monde, trouver des créatures, les combattre et les capturer afin d'en faire des membres de leur équipe et combattre d'autres joueurs dans le cadre de duels, de tournois ou de league.

Une VM servira de serveur pour héberger et gérer tous les joueurs et leurs interactions dans un temps proche du temps réel, une autre VM servira de monitoring afin de stocker les données essentielles des joueurs pour qu'ils conservent leur progression après avoir quitté le jeu, enfin une autre VM servira de back-up aux 2 autres VMs afin de prévenir de potentielles erreurs du serveur ou de la corruption des données, il s'occupera donc automatiquement de la maintenance dans des horaires où peu ou pas de joueurs seront connéctés (entre 3 AM et 5 AM) afin de ne pas couper et perturber les joueurs.

Afin de gérer plusieurs joueurs en simultanés et proche d'un temps réel, le serveur et le client utiliseront de l'asynchrone pour communiquer et échanger des informations, mais également pour communiquer avec la VM de stockage de données et monitoring et le jeu sera codé en python avec la librairie Pygame.

De plus, afin de faciliter l'instalation du client pour les joueurs, indépendemment de leurs versions et pour éviter les soucis de "it works on my machine", tout sera converti en une ou plusieurs image Docker qui pourront ainsi toutes être lancés avec une seule ligne de commande.

Ce projet est assuré par Killian Guillemot en B2 filière informatique et Axel Pore en B2 filière informatique.
```

---