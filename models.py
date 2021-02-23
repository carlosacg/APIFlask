from app import db

class Pagos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fechaPago = db.Column(db.Date)
    documentoIdentificacionArrendatario = db.Column(db.Integer)
    codigoInmueble = db.Column(db.String(255))
    valorPagado = db.Column(db.Integer)

    def __init__(self,fechaPago,documentoIdentificacionArrendatario,codigoInmueble,valorPagado):
        self.fechaPago = fechaPago
        self.documentoIdentificacionArrendatario = documentoIdentificacionArrendatario
        self.codigoInmueble = codigoInmueble
        self.valorPagado = valorPagado