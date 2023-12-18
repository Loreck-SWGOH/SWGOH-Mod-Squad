-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

INSERT INTO Profiles(userID, joinDate)
VALUES
    (0, TO_DATE('01/01/2001', 'MM/DD/YYYY')),
    (1, TO_DATE('01/01/2001', 'MM/DD/YYYY'));

\COPY Campaigns FROM 'Campaigns.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.campaigns_id_seq',
                         (SELECT MAX(id)+1 FROM Campaigns),
                         false);

\COPY Events FROM 'Events.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.events_id_seq',
                         (SELECT MAX(id)+1 FROM Events),
                         false);

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

\COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.purchases_id_seq',
                         (SELECT MAX(id)+1 FROM Purchases),
                         false);
