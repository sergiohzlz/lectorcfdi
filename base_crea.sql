DROP TABLE cfdis;


CREATE TABLE cfdis (
    uuid             varchar(32) primary key,
    emisor_nombre    text,
    emisor_rfc       varchar(15) not null,
    receptor_nombre  text,
    receptor_rfc     varchar(15) not null,
    fecha            date,
    tipo_cambio      float default 1,
    total            float default 0,
    subtotal         float default 0, 
    traslado_iva     float default 0,
    traslado_ieps    float default 0,
    traslado_isr     float default 0,
    retencion_iva    float default 0,
    retencion_isr    float default 0,
    cfdi_moneda      varchar(3),
    cfdi_tipo        varchar(7), 
    cfdi_fecha_t     date,                     --fecha timbrado
    cfdi_sello       text,                     --sello cfdi
    cfdi_cert        text,                     --certificado cfdi
    cfdi_version     varchar(3)                --version cfdi
);
