-- Base de datos para Módulo Notas Crédito y Débito DIAN
-- Compatible con MySQL 5.7+

CREATE DATABASE IF NOT EXISTS facturacion_dian 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE facturacion_dian;

-- Tabla principal de notas crédito y débito
CREATE TABLE IF NOT EXISTS notas_credito_debito (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(50) NOT NULL UNIQUE COMMENT 'Número consecutivo de la nota',
    prefijo VARCHAR(10) DEFAULT NULL COMMENT 'Prefijo autorizado por DIAN',
    tipo ENUM('credito', 'debito') NOT NULL COMMENT 'Tipo de nota',
    fecha_emision DATE NOT NULL COMMENT 'Fecha de emisión',
    hora_emision TIME NOT NULL COMMENT 'Hora de emisión',
    fecha_vencimiento DATE DEFAULT NULL COMMENT 'Fecha de vencimiento si aplica',
    
    -- Datos de la factura de referencia
    factura_referencia VARCHAR(50) NOT NULL COMMENT 'Número de factura que se modifica',
    factura_cufe VARCHAR(200) DEFAULT NULL COMMENT 'CUFE de la factura de referencia',
    
    -- Concepto de la nota
    codigo_concepto VARCHAR(10) NOT NULL COMMENT 'Código del concepto según DIAN',
    descripcion_concepto TEXT COMMENT 'Descripción del concepto o motivo',
    
    -- Valores monetarios
    valor_base DECIMAL(15,2) NOT NULL DEFAULT 0.00 COMMENT 'Valor base antes de impuestos',
    porcentaje_iva DECIMAL(5,2) NOT NULL DEFAULT 0.00 COMMENT 'Porcentaje de IVA aplicado',
    valor_iva DECIMAL(15,2) NOT NULL DEFAULT 0.00 COMMENT 'Valor del IVA',
    otros_impuestos DECIMAL(15,2) DEFAULT 0.00 COMMENT 'Otros impuestos si aplican',
    valor_total DECIMAL(15,2) NOT NULL DEFAULT 0.00 COMMENT 'Valor total de la nota',
    
    -- Datos técnicos DIAN
    cufe VARCHAR(200) DEFAULT NULL COMMENT 'Código Único de Facturación Electrónica',
    cude VARCHAR(200) DEFAULT NULL COMMENT 'Código Único de Documento Electrónico',
    qr_code TEXT DEFAULT NULL COMMENT 'Código QR generado',
    xml_content LONGTEXT DEFAULT NULL COMMENT 'Contenido XML del documento',
    pdf_path VARCHAR(500) DEFAULT NULL COMMENT 'Ruta del archivo PDF generado',
    
    -- Control de estado
    estado ENUM('borrador', 'generado', 'enviado', 'aceptado', 'rechazado') DEFAULT 'borrador',
    fecha_envio_dian DATETIME DEFAULT NULL COMMENT 'Fecha de envío a DIAN',
    respuesta_dian TEXT DEFAULT NULL COMMENT 'Respuesta de la DIAN',
    
    -- Auditoría
    usuario_creacion VARCHAR(100) DEFAULT NULL COMMENT 'Usuario que creó el registro',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(100) DEFAULT NULL,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_numero (numero),
    INDEX idx_tipo (tipo),
    INDEX idx_fecha_emision (fecha_emision),
    INDEX idx_factura_referencia (factura_referencia),
    INDEX idx_estado (estado),
    INDEX idx_cufe (cufe),
    INDEX idx_fecha_creacion (fecha_creacion)
) ENGINE=InnoDB COMMENT='Tabla principal para notas crédito y débito DIAN';

-- Tabla de conceptos permitidos según DIAN
CREATE TABLE IF NOT EXISTS conceptos_notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(10) NOT NULL,
    tipo_nota ENUM('credito', 'debito') NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    
    UNIQUE KEY uk_codigo_tipo (codigo, tipo_nota)
) ENGINE=InnoDB COMMENT='Conceptos permitidos para notas según DIAN';

-- Insertar conceptos de nota crédito según DIAN
INSERT INTO conceptos_notas (codigo, tipo_nota, descripcion) VALUES
('1', 'credito', 'Devolución parcial de los bienes'),
('2', 'credito', 'Anulación de la operación'),
('3', 'credito', 'Rebaja total aplicada'),
('4', 'credito', 'Descuento total aplicado'),
('5', 'credito', 'Rescisión de la operación'),
('6', 'credito', 'Otros');

-- Insertar conceptos de nota débito según DIAN
INSERT INTO conceptos_notas (codigo, tipo_nota, descripcion) VALUES
('1', 'debito', 'Intereses'),
('2', 'debito', 'Gastos por cobrar'),
('3', 'debito', 'Cambio del valor'),
('4', 'debito', 'Otros');

-- Tabla de terceros (emisor y adquiriente)
CREATE TABLE IF NOT EXISTS terceros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_identificacion VARCHAR(10) NOT NULL COMMENT 'NIT, CC, CE, etc.',
    numero_identificacion VARCHAR(20) NOT NULL,
    digito_verificacion CHAR(1) DEFAULT NULL,
    razon_social VARCHAR(200) NOT NULL,
    nombre_comercial VARCHAR(200) DEFAULT NULL,
    
    -- Dirección
    direccion VARCHAR(200) DEFAULT NULL,
    ciudad VARCHAR(100) DEFAULT NULL,
    departamento VARCHAR(100) DEFAULT NULL,
    codigo_postal VARCHAR(10) DEFAULT NULL,
    pais VARCHAR(2) DEFAULT 'CO',
    
    -- Contacto
    telefono VARCHAR(20) DEFAULT NULL,
    email VARCHAR(100) DEFAULT NULL,
    
    -- Datos tributarios
    regimen_tributario VARCHAR(50) DEFAULT NULL,
    responsabilidades_fiscales TEXT DEFAULT NULL,
    
    -- Control
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_tipo_numero (tipo_identificacion, numero_identificacion),
    INDEX idx_numero_identificacion (numero_identificacion),
    INDEX idx_razon_social (razon_social)
) ENGINE=InnoDB COMMENT='Información de terceros (emisor y adquiriente)';

-- Tabla de numeración autorizada
CREATE TABLE IF NOT EXISTS numeracion_autorizada (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_documento ENUM('factura', 'nota_credito', 'nota_debito') NOT NULL,
    prefijo VARCHAR(10) DEFAULT NULL,
    resolucion_dian VARCHAR(50) NOT NULL,
    fecha_resolucion DATE NOT NULL,
    numero_desde BIGINT NOT NULL,
    numero_hasta BIGINT NOT NULL,
    numero_actual BIGINT NOT NULL DEFAULT 0,
    fecha_vigencia_desde DATE NOT NULL,
    fecha_vigencia_hasta DATE NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    
    INDEX idx_tipo_documento (tipo_documento),
    INDEX idx_vigencia (fecha_vigencia_desde, fecha_vigencia_hasta)
) ENGINE=InnoDB COMMENT='Numeración autorizada por la DIAN';

-- Tabla de configuración
CREATE TABLE IF NOT EXISTS configuracion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clave VARCHAR(100) NOT NULL UNIQUE,
    valor TEXT,
    descripcion VARCHAR(200),
    tipo_dato ENUM('string', 'number', 'boolean', 'json') DEFAULT 'string',
    categoria VARCHAR(50) DEFAULT 'general',
    
    INDEX idx_categoria (categoria)
) ENGINE=InnoDB COMMENT='Configuración general del sistema';

-- Insertar configuración básica
INSERT INTO configuracion (clave, valor, descripcion, categoria) VALUES
('empresa_nit', '', 'NIT de la empresa emisora', 'empresa'),
('empresa_razon_social', '', 'Razón social de la empresa', 'empresa'),
('empresa_direccion', '', 'Dirección de la empresa', 'empresa'),
('empresa_telefono', '', 'Teléfono de la empresa', 'empresa'),
('empresa_email', '', 'Email de la empresa', 'empresa'),
('dian_ambiente', 'habilitacion', 'Ambiente DIAN (habilitacion/produccion)', 'dian'),
('dian_pin_software', '', 'PIN del software registrado en DIAN', 'dian'),
('dian_id_software', '', 'ID del software registrado en DIAN', 'dian'),
('xml_path', './xml/', 'Ruta para almacenar archivos XML', 'sistema'),
('pdf_path', './pdf/', 'Ruta para almacenar archivos PDF', 'sistema');

-- Tabla de log de eventos
CREATE TABLE IF NOT EXISTS log_eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    documento_id INT DEFAULT NULL,
    tipo_documento VARCHAR(20) DEFAULT NULL,
    evento VARCHAR(50) NOT NULL,
    descripcion TEXT,
    usuario VARCHAR(100) DEFAULT NULL,
    ip_address VARCHAR(45) DEFAULT NULL,
    fecha_evento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_documento (documento_id, tipo_documento),
    INDEX idx_evento (evento),
    INDEX idx_fecha (fecha_evento)
) ENGINE=InnoDB COMMENT='Log de eventos del sistema';

-- Vista para consultas rápidas de notas
CREATE VIEW vista_notas_resumen AS
SELECT 
    n.id,
    n.numero,
    n.prefijo,
    n.tipo,
    CASE 
        WHEN n.tipo = 'credito' THEN 'Nota Crédito'
        WHEN n.tipo = 'debito' THEN 'Nota Débito'
    END AS tipo_descripcion,
    n.fecha_emision,
    n.factura_referencia,
    c.descripcion as concepto_descripcion,
    n.valor_total,
    n.estado,
    CASE 
        WHEN n.estado = 'borrador' THEN 'Borrador'
        WHEN n.estado = 'generado' THEN 'Generado'
        WHEN n.estado = 'enviado' THEN 'Enviado'
        WHEN n.estado = 'aceptado' THEN 'Aceptado'
        WHEN n.estado = 'rechazado' THEN 'Rechazado'
    END AS estado_descripcion,
    n.cufe,
    n.fecha_creacion
FROM notas_credito_debito n
LEFT JOIN conceptos_notas c ON n.codigo_concepto = c.codigo AND n.tipo = c.tipo_nota
ORDER BY n.fecha_emision DESC, n.numero DESC;

-- Procedimiento para obtener siguiente número
DELIMITER //
CREATE PROCEDURE GetSiguienteNumero(
    IN p_tipo_documento VARCHAR(20),
    IN p_prefijo VARCHAR(10),
    OUT p_numero BIGINT
)
BEGIN
    DECLARE v_numero_actual BIGINT DEFAULT 0;
    DECLARE v_numero_hasta BIGINT DEFAULT 0;
    
    -- Obtener numeración actual
    SELECT numero_actual, numero_hasta 
    INTO v_numero_actual, v_numero_hasta
    FROM numeracion_autorizada 
    WHERE tipo_documento = p_tipo_documento 
      AND (prefijo = p_prefijo OR (prefijo IS NULL AND p_prefijo IS NULL))
      AND activo = TRUE
      AND CURDATE() BETWEEN fecha_vigencia_desde AND fecha_vigencia_hasta
    LIMIT 1;
    
    -- Verificar que no se exceda el rango autorizado
    IF v_numero_actual >= v_numero_hasta THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Se ha agotado la numeración autorizada';
    END IF;
    
    -- Incrementar número
    SET v_numero_actual = v_numero_actual + 1;
    
    -- Actualizar numeración
    UPDATE numeracion_autorizada 
    SET numero_actual = v_numero_actual
    WHERE tipo_documento = p_tipo_documento 
      AND (prefijo = p_prefijo OR (prefijo IS NULL AND p_prefijo IS NULL))
      AND activo = TRUE;
    
    SET p_numero = v_numero_actual;
END //
DELIMITER ;

-- Trigger para log de cambios
DELIMITER //
CREATE TRIGGER tr_notas_after_insert
AFTER INSERT ON notas_credito_debito
FOR EACH ROW
BEGIN
    INSERT INTO log_eventos (documento_id, tipo_documento, evento, descripcion)
    VALUES (NEW.id, NEW.tipo, 'CREACION', CONCAT('Nota ', NEW.tipo, ' creada: ', NEW.numero));
END //

CREATE TRIGGER tr_notas_after_update
AFTER UPDATE ON notas_credito_debito
FOR EACH ROW
BEGIN
    IF OLD.estado != NEW.estado THEN
        INSERT INTO log_eventos (documento_id, tipo_documento, evento, descripcion)
        VALUES (NEW.id, NEW.tipo, 'CAMBIO_ESTADO', 
                CONCAT('Estado cambiado de ', OLD.estado, ' a ', NEW.estado));
    END IF;
END //
DELIMITER ;

-- Crear usuario específico para la aplicación (opcional)
-- CREATE USER 'app_notas'@'localhost' IDENTIFIED BY 'password_seguro';
-- GRANT SELECT, INSERT, UPDATE ON facturacion_dian.* TO 'app_notas'@'localhost';
-- FLUSH PRIVILEGES;