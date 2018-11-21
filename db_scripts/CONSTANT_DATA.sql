START TRANSACTION;

INSERT INTO `CURRENCY` (`CODE`, `NAME`, `TYPE`) VALUES
('PLN', 'Polski złoty', 'fiat'),
('USD', 'Dolar amerykański', 'fiat'),
('GBP', 'Funt brytyjski', 'fiat'),
('BTC', 'Bitcoin', 'crypto'),
('ETH', 'Ethereum', 'crypto'),
('XRP', 'Ripple', 'crypto'),
('CHF', 'Frank szwajcarski', 'fiat'),
('BCH', 'Bitcoin Cash', 'crypto'),
('EOS', 'EOS', 'crypto'),
('EUR', 'Euro', 'fiat'),
('SEK', 'Korona szwedzka', 'fiat'),
('DKK', 'Korona duńska', 'fiat');

COMMIT;