from app import app
from models import *
from flask import request, Response, jsonify
from datetime import datetime

@app.route('/api/pagos', methods=['GET'])
def obtener_pagos():
    data = []
    payments_lis = Pagos.query.all()
    for pago in payments_lis:
        data.append({
            "documentoIdentificacionArrendatario":pago.documentoIdentificacionArrendatario,
            "codigoInmueble":pago.codigoInmueble,
            "valorPagado":pago.valorPagado,
            "fechaPago":datetime.strftime(pago.fechaPago,'%d/%m/%Y')
        })
    return jsonify(data),200

@app.route('/api/pagos', methods=['POST'])
def crear_pago():
    params = request.json
    documentoIdentificacionArrendatario = params.get('documentoIdentificacionArrendatario',False)
    codigoInmueble = params.get('codigoInmueble',False)
    valorPagado = params.get('valorPagado',False)
    fechaPago = params.get('fechaPago',False)
    mensaje = "gracias por pagar tu arriendo"

    try:
        fechaPago = datetime.strptime(fechaPago, '%d/%m/%Y')
        if fechaPago.day % 2 == 0:
            return Response("lo siento pero no se puede recibir el pago por decreto de administración",status=400)
    except:
        return Response("Formato de fecha incorrecto",status=400)

    try: 
        documentoIdentificacionArrendatario = int(documentoIdentificacionArrendatario)
    except:
        return Response("Formato de documento de identificacion incorrecto",status=400)
    
    try: 
        valorPagado = float(valorPagado)
        if not (valorPagado and valorPagado >= 1 and valorPagado <=1000000):
            return Response("El campo valorPagado debe estar entre 1 y 1000000",status=400)
    except:
        return Response("Formato de documento de valor pagado incorrecto",status=400)

    try:           
        if not codigoInmueble:
            return Response("El campo codigoInmueble es obligatorio",status=400)
        
        nuevo_pago = Pagos(fechaPago,documentoIdentificacionArrendatario,codigoInmueble,valorPagado)
        db.session.add(nuevo_pago)
        db.session.commit()
        if valorPagado == 1000000:
            mensaje='gracias por pagar todo tu arriendo'
        else:
            total_pagos_acumulados = 0
            lista_pagos_mes = Pagos.query.filter_by(
                documentoIdentificacionArrendatario=documentoIdentificacionArrendatario,
                codigoInmueble=codigoInmueble
                )
            for pago_acumulado in lista_pagos_mes:
                if pago_acumulado.fechaPago.month == fechaPago.month:
                    total_pagos_acumulados += pago_acumulado.valorPagado
            if total_pagos_acumulados >= 1000000:
                mensaje='gracias por pagar todo tu arriendo'
            else:
                mensaje='gracias por tu abono, sin embargo recuerda que te hace falta pagar ${diferencia}'.format(diferencia=1000000-total_pagos_acumulados)
        return Response(mensaje,status=200)
    except Exception as e:
        return Response(str(e),status=400)