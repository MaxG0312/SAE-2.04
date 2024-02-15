DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS meuble;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS type_meuble;
DROP TABLE IF EXISTS materiau;
DROP TABLE IF EXISTS etat; 
DROP TABLE IF EXISTS utilisateur;


CREATE TABLE utilisateur(
   id_utilisateur INT AUTO_INCREMENT,
   login VARCHAR(128),
   email VARCHAR(50),
   nom VARCHAR(50),
   password VARCHAR(250),
   role VARCHAR(50),
   est_actif BOOLEAN,

   PRIMARY KEY(id_utilisateur)
);

CREATE TABLE etat(
   id_etat INT AUTO_INCREMENT,
   libelle VARCHAR(50),

   PRIMARY KEY(id_etat)
);

CREATE TABLE materiau(
   id_materiau INT AUTO_INCREMENT,
   libelle_materiau VARCHAR(128),

   PRIMARY KEY(id_materiau)
);

CREATE TABLE type_meuble(
   id_type INT AUTO_INCREMENT,
   libelle_type VARCHAR(50),

   PRIMARY KEY(id_type)
);

CREATE TABLE commande(
   id_commande INT AUTO_INCREMENT,
   utilisateur_id INT NOT NULL,
   etat_id INT NOT NULL,
   date_achat DATETIME,

   PRIMARY KEY(id_commande),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(etat_id) REFERENCES etat(id_etat)
);

CREATE TABLE meuble(
   id_meuble INT AUTO_INCREMENT,
   type_meuble_id INT NOT NULL,
   materiau_id INT NOT NULL,
   nom_meuble VARCHAR(50),
   stock INT,
   largeur INT,
   hauteur INT,
   prix_meuble DECIMAL(15,2),
   fournisseur VARCHAR(128),
   marque VARCHAR(50),
   image_meuble VARCHAR(128),
   
   PRIMARY KEY(id_meuble),
   FOREIGN KEY(type_meuble_id) REFERENCES type_meuble(id_type),
   FOREIGN KEY(materiau_id) REFERENCES materiau(id_materiau)
)CHARACTER SET 'utf8';

CREATE TABLE ligne_panier(
   utilisateur_id INT,
   meuble_id INT,
   quantite INT,
   date_ajout DATETIME,
   PRIMARY KEY(utilisateur_id, meuble_id),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(meuble_id) REFERENCES meuble(id_meuble)
);

CREATE TABLE ligne_commande(
   commande_id INT,
   meuble_id INT,
   prix DECIMAL(15,2),
   quantite INT,
   PRIMARY KEY(commande_id, meuble_id),
   FOREIGN KEY(commande_id) REFERENCES commande(id_commande),
   FOREIGN KEY(meuble_id) REFERENCES meuble(id_meuble)
);


-- Insertion des données
INSERT INTO materiau (libelle_materiau)
VALUES 
("Chêne"),
("Pin"),
("Châtaignier"),
("Acier");


INSERT INTO type_meuble(libelle_type)
VALUES  
("Canapé"),
("Fauteuil"),
("Commode"),
("Étagère");

INSERT INTO meuble (nom_meuble, largeur, hauteur, prix_meuble, fournisseur, marque, stock, image_meuble, type_meuble_id, materiau_id)
VALUES
("GRÖNLID", 442, 83, 1149, "IKEA", "IKEA", 10, "GRÖNLID.jpg", 1, 1),
("KIVIK", 603, 83, 1949, "IKEA", "IKEA", 10, "KIVIK.jpg", 1, 1),
("SMEDSTORP", 165, 88, 599, "IKEA", "IKEA", 10, "SMEDSTORP.jpg", 1, 1),
("SÖDERHAMN", 186, 83, 399, "IKEA", "IKEA", 10, "SÖDERHAMN.jpg", 1, 1),

("STRANDMON", 96, 101, 349, "IKEA", "IKEA", 10, "STRANDMON.jpg", 2, 2),
("EKTORP", 104, 88, 249, "IKEA", "IKEA", 10, "EKTORP.jpg", 2, 2),
("EKERÖ", 71, 73, 149, "IKEA", "IKEA", 10, "EKERÖ.jpg", 2, 4),
("POÄNG", 112, 100, 79.99, "IKEA", "IKEA", 10, "POÄNG.jpg", 2, 3),

("BESTÄ", 180, 65, 300, "IKEA", "IKEA", 10, "BESTA.jpg", 3, 1),
("GURSKEN", 120, 74, 265, "IKEA", "IKEA", 10, "GURSKEN.jpg", 3, 2),
("NORDLI", 180, 74, 415, "IKEA", "IKEA", 10, "NORDLI.jpg", 3, 3),
("RAST", 180, 74, 390, "IKEA", "IKEA", 10, "RAST.jpg", 3, 2),

("EKET", 35, 35, 20, "IKEA", "IKEA", 10, "EKET.jpg", 4, 1),
("EKET_GM", 105, 35, 120, "IKEA", "IKEA", 10, "EKET_GM.jpg", 4, 2),
("EKET_MM", 70, 35, 115, "IKEA", "IKEA", 10, "EKET_MM.jpg", 4, 3),
("KALLAX", 77, 147, 64.99, "IKEA", "IKEA", 10, "KALLAX.jpg", 4, 1);


INSERT INTO utilisateur (login, email, nom, password, role, est_actif)
VALUES 
("admin", "admin@admin.fr", "admin", "pbkdf2:sha512:600000$c2zg3GrrMJm7Upvp$2b76fc2c1e6f52114e55c304c7705c4f5a596996766d33af3de675e518b8c1677a02ffca8d9c2e75cf597df6a0f66c97ebf36c8b2c298d20601a4cb6c209b8ad", "ROLE_admin", 1),

("client", "client@client.fr", "client", "pbkdf2:sha512:600000$50gau35kDsh2EQxi$afbec681b7630fe8d9794536a5a4b0d1ffad75da85fe00dc4e4351122dd4d0dc73c84a2028a262108811228e0c7825897425256a6cafef8f25043fe9aca3ae90", "ROLE_client", 1),

("client2", "client2@client.fr", "client2", "pbkdf2:sha512:600000$AzVEd5kVoRwR6SPF$65db3d109a2f08d53c3fbdc72218cbdb34dce9a302badc04f491b1292c4a0725985ea085d3e360c101579898688a098e2a74076c2015ff38dab3bd8c57e68c01", "ROLE_client", 1);


INSERT INTO etat (libelle)
VALUES
('en cours de traitement'),
('expedié');
