SELECT
    nome_do_logradouro,
    numero,
    cep,
    data_de_transacao,
    area_construida_m2,
    acc_iptu,
    valor_de_transacao_declarado_pelo_contribuinte
FROM data
WHERE (? = '' OR nome_do_logradouro LIKE ?)
  AND (? = '' OR numero = ?)
ORDER BY data_de_transacao DESC
LIMIT 50;
