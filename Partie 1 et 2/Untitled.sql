CREATE TABLE `Produits` (
  `id` integer PRIMARY KEY,
  `titre` varchar(255),
  `prix` decimal,
  `description` varchar(255),
  `categorie` varchar(255),
  `marque` varchar(255),
  `caracteristiques` text
);

CREATE TABLE `Utilisateurs` (
  `id` integer PRIMARY KEY,
  `identite` varchar(255),
  `coordonnees` varchar(255)
);

CREATE TABLE `Paniers` (
  `id` integer PRIMARY KEY,
  `utilisateur_id` integer,
  `produit_id` integer,
  `quantite` integer
);

ALTER TABLE `Paniers` ADD FOREIGN KEY (`utilisateur_id`) REFERENCES `Utilisateurs` (`id`);

ALTER TABLE `Paniers` ADD FOREIGN KEY (`produit_id`) REFERENCES `Produits` (`id`);

-- Disable foreign key checks for INSERT
SET FOREIGN_KEY_CHECKS = 0;

INSERT INTO `Produits` (`id`, `titre`, `prix`, `description`, `categorie`, `marque`, `caracteristiques`)
VALUES
  (0, 'Stylo', 1.5, 'Super stylo', 'Écriture', 'BIC', 'Incassable'),
  (1, 'Stylo 1', 1.5, 'Super stylo', 'Écriture', 'BIC', 'Incassable'),
  (2, 'Stylo 2', 1.5, 'Super stylo', 'Écriture', 'BIC', 'Incassable'),
  (3, 'Stylo 3', 1.5, 'Super stylo', 'Écriture', 'BIC', 'Incassable');
INSERT INTO `Utilisateurs` (`id`, `identite`, `coordonnees`)
VALUES
  (1, 'Dahae', 'Centre-ville'),
  (3, 'Felix', 'Centre-ville');
INSERT INTO `Paniers` (`utilisateur_id`, `produit_id`, `quantite`)
VALUES
  (1, 0, 2),
  (1, 2, 1),
  (3, 1, 3);

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;