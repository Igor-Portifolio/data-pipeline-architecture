CREATE TABLE staging__bairros_{{UF}} AS
SELECT DISTINCT
  bairro
FROM staging__base
WHERE uf = '{{UF}}'
  AND bairro IS NOT NULL;
