START TRANSACTION;

INSERT INTO `CURRENCY` (`CURRENCY_CODE`, `CURRENCY_NAME`, `TYPE`) VALUES
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