CREATE TABLE notas_credito (
    id INT AUTO_INCREMENT PRIMARY KEY,
    factura_id INT NOT NULL,
    motivo VARCHAR(255) NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    fecha_emision TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id) REFERENCES facturas(id)
);

CREATE TABLE notas_debito (
    id INT AUTO_INCREMENT PRIMARY KEY,
    factura_id INT NOT NULL,
    motivo VARCHAR(255) NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    fecha_emision TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id) REFERENCES facturas(id)
);