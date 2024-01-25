DROP TABLE IF EXISTS ligne_panier, ligne_commande, meuble, commande, type_meuble, materiau, etat, utilisateur;

CREATE TABLE utilisateur(
    id_utilisateur INT,
    login VARCHAR(128),
    email VARCHAR(50),
    nom VARCHAR(50),
    password VARCHAR(250),
    role VARCHAR(50),
    PRIMARY KEY(id_utilisateur)
);

CREATE TABLE etat(
    id_etat INT,
    libelle VARCHAR(50),
    PRIMARY KEY(id_etat)
);

CREATE TABLE materiau(
    id_materiau INT,
    libelle_materiau VARCHAR(128),
    PRIMARY KEY(id_materiau)
);

CREATE TABLE type_meuble(
    id_type INT,
    libelle_type VARCHAR(50),
    PRIMARY KEY(id_type)
);

CREATE TABLE commande(
    id_commande INT,
    date_achat DATETIME,
    utilisateur_id INT NOT NULL,
    etat_id INT NOT NULL,
    PRIMARY KEY(id_commande),
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY(etat_id) REFERENCES etat(id_etat)
);

CREATE TABLE meuble( 
    id_meuble INT,
    nom_meuble VARCHAR(50),
    largeur DECIMAL(15,2),
    hauteur DECIMAL(15,2),
    prix_meuble DECIMAL(15,2),
    fournisseur VARCHAR(50),
    marque VARCHAR(50),
    image_meuble VARCHAR(128),
    type_meuble_id INT NOT NULL,
    materiau_id INT NOT NULL,
    PRIMARY KEY(id_meuble),
    FOREIGN KEY(type_meuble_id) REFERENCES type_meuble(id_type),
    FOREIGN KEY(materiau_id) REFERENCES materiau(id_materiau)
);

CREATE TABLE ligne_commande( 
    id_ligne_commande INT,
    prix DECIMAL(15,2),
    quantite INT,
    commande_id INT NOT NULL,
    meuble_id INT NOT NULL,
    PRIMARY KEY(id_ligne_commande),
    FOREIGN KEY(commande_id) REFERENCES commande(id_commande),
    FOREIGN KEY(meuble_id) REFERENCES meuble(id_meuble)
);

CREATE TABLE ligne_panier( 
    id_ligne_panier INT,
    quantite INT NOT NULL,
    date_ajout DATETIME,
    meuble_id INT NOT NULL,
    utilisateur_id INT NOT NULL,
    PRIMARY KEY(id_ligne_panier),
    FOREIGN KEY(meuble_id) REFERENCES meuble(id_meuble),
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur)
);

/*
INSERT INTO utilisateur VALUES ();

INSERT INTO etat VALUES ();

INSERT INTO materiau VALUES ();
*/
INSERT INTO type_meuble VALUES  (1, "Canapé"),
                                (2, "Fauteuil"),
                                (3, "Meuble de Gaming"),
                                (4, "Étagères")
;
/*
INSERT INTO commande VALUES ();

INSERT INTO meuble VALUES ();

INSERT INTO ligne_commande VALUES ();

INSERT INTO ligne_panier VALUES ();
*/