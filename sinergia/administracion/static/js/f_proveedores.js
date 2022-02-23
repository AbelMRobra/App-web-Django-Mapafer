async function service_crear_proveedor() {
    const url = `${document.getElementById("host").value}api/api_proveedores/`;
    sweet_alert("Procesando ..", "warning");
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${document.getElementById("token").value}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'razon_social' : document.getElementById("razon_social").value,
            'fantasia' : document.getElementById("fantasia").value,
            'cuit' : document.getElementById("cuit").value,
            'banco' : document.getElementById("banco").value,
            'n_cuenta' : document.getElementById("n_cuenta").value,
            'cbu' : document.getElementById("cbu").value,
            'direccion' : document.getElementById("direccion").value,
            'ciudad' : document.getElementById("ciudad").value,
            'provincia' : document.getElementById("provincia").value,

        })

    });

    var response = await respuesta.json();
    var status = await respuesta.status;
    return validar_respuesta_creacion(response, status)
}

async function service_editar_proveedor(id) {
    const url = `${document.getElementById("host").value}api/api_proveedores/${id}/`;
    sweet_alert("Procesando ..", "warning");
    var respuesta = await fetch(url ,{
        method: "PATCH",
        headers: {
            'X-CSRFToken' : `${document.getElementById("token").value}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'razon_social' : document.getElementById("razon_social").value,
            'fantasia' : document.getElementById("fantasia").value,
            'cuit' : document.getElementById("cuit").value,
            'banco' : document.getElementById("banco").value,
            'n_cuenta' : document.getElementById("n_cuenta").value,
            'cbu' : document.getElementById("cbu").value,
            'direccion' : document.getElementById("direccion").value,
            'ciudad' : document.getElementById("ciudad").value,
            'provincia' : document.getElementById("provincia").value,

        })

    });

    var response = await respuesta.json();
    var status = await respuesta.status;
    return validar_respuesta_creacion(response, status)
}

function validar_respuesta_creacion(response, status){
    
    if (status >= 200 && status <300){
        sweet_alert("Todo listo!", "success")
    } else {
        console.log(response)
        sweet_alert(response.message, "error")
    }
}

function change_monto_pago(saldo){

    var select = document.getElementById('select')
    var id_deuda = select.value

    var input_id = document.getElementById(id_deuda)
    var valor = input_id.value

    console.log(valor)

    var monto = document.getElementById('monto')
    monto.value = valor
}