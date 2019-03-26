# Algorithme du plus court chemin: Dijkstra

## Généralité

Dans un graphe orienté pondéré ne présentant pas de boucle où la somme des 
chemins empruntés serait négative; trouve le plus petit chemin d'une source
à une cible.

## Principe

- Initialiser le poids de tous les sommets à `+inf` sauf la source que l'on 
initialise à `0`

- Initialiser la liste des noeuds ouverts à tous les noeuds du graphe

- Tant qu'il reste des noeuds ouverts:

    - Séléctionner le noeud avec le plus petit poids
    
    - L'enlever de la liste des noeuds ouverts
    
    - Pour chaque noeuds fils du noeud choisi:
    
        - Si le chemin est plus optimal en venant du noeud actuel:
        
            - Mettre à jour le poids du noeud fils
            
            - Marquer l'ancêtre du noeud fils comme le noeud actuel

- Mettre chemin à liste vide

- Mettre noeud actuel à `target`

- Tant que le noeud actuel n'est pas `target`:

    - Ajouter le noeud actuel au chemin parcouru
    
    - Mettre le noeud actuel à l'ancêtre du noeud actuel
    
- Ajouter le noeud `source` au chemin

- Retourner chemin inversé pour avoir le sens `source` -> `target`

## Liens et ressources

- [Article de Edsger W. Dijkstra](http://www.cs.utexas.edu/users/EWD/ewd03xx/EWD316.PDF)
   (avec l'article original sur le plus court chemin)
   
- [Page Wikipedia sur l'algorithme de Dijkstra](https://fr.wikipedia.org/wiki/Algorithme_de_Dijkstra)