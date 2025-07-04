CREATE TABLE IF NOT EXISTS notas_credito_debito (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(50) NOT NULL UNIQUE,
    tipo ENUM('credito', 'debito') NOT NULL,
    fecha_emision DATE NOT NULL,
    hora_emision TIME NOT NULL,
    factura_referencia VARCHAR(50) NOT NULL,
    codigo_concepto VARCHAR(10) NOT NULL,
    descripcion_concepto TEXT,
    valor_base DECIMAL(15,2) NOT NULL,
    porcentaje_iva DECIMAL(5,2) NOT NULL,
    valor_iva DECIMAL(15,2) NOT NULL,
    porcentaje_retencion DECIMAL(5,2) DEFAULT 0.00,
    retencion_renta DECIMAL(15,2) DEFAULT 0.00,
    valor_total DECIMAL(15,2) NOT NULL,
    cufe VARCHAR(200),
    xml_content LONGTEXT,
    estado ENUM('borrador', 'generado', 'enviado') DEFAULT 'borrador',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Auditoría
    usuario_creacion VARCHAR(100) DEFAULT NULL COMMENT 'Usuario que creó el registro',
    fecha_creacion_usuario TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(100) DEFAULT NULL,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);