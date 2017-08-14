DROP TABLE IF EXISTS contribuyentes;

CREATE TABLE contribuyentes (
    emisor_rfc      varchar(17) primary key,
    emisor_nombre   varchar(250),
    emisor_fecha    date,
    tipo            varchar(10),
    folio_fiscal    varchar(37),
    receptor_nombre varchar(250),
    receptor_rfc    varchar(17) not null,
    subtotal        float,
    ieps            float,
    iva             float,
    ret_iva         float,
    ret_isr         float,
    tc              float,
    total           float
);
