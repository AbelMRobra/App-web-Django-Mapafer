


async function consulta_datos_prestamo() {

    id_prestamo = document.getElementById("nuevo_prestamo").value;
    const url = `${document.getElementById("host").value}api/api_prestamos/${id_prestamo}/datos_prestamo_actual/`;
    
    var respuesta = await fetch(url ,{
        method: "GET",
        headers: {
            'X-CSRFToken' : `${document.getElementById("token").value}`,
            'Content-Type': 'application/json',
        },

    });

    var response = await respuesta.json();
    var status = await respuesta.status;
    return validar_respuesta_consulta(response, status)
}

function validar_respuesta_consulta(response, status){
    
    if (status >= 200 && status <300){

        modificar_template_consulta(response);
    } else {
        sweet_alert("Problema de conexión", "warning")
    }
}


function modificar_template_consulta(response){

    console.log(response)

    var cuota = document.getElementById(`cliente`);
    cuota.style = "display: contents"
    cuota.innerHTML = `${response.cliente}`

    var cuota = document.getElementById(`cuota`);
    cuota.style = "display: contents"
    cuota.innerHTML = `Cuota: $ ${response.cuota}`

    var pagado = document.getElementById(`pagado`);
    pagado.style = "display: contents"
    pagado.innerHTML = `Pagado: $ ${response.pagado}`

    var saldo = document.getElementById(`saldo`);
    saldo.style = "display: contents"
    saldo.innerHTML = `Saldo: $ ${response.saldo}`
}


async function agregar_pago() {

    const url = `${document.getElementById("host").value}api/api_pagos/`;

    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${document.getElementById("token").value}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'prestamo' : document.getElementById("nuevo_prestamo").value,
            'fecha' : document.getElementById("nuevo_fecha").value,
            'monto' : document.getElementById("nuevo_monto").value,

        })
        });

    var response = await respuesta.json();
    var status = await respuesta.status;
    return validar_respuesta(response, status)
}

function validar_respuesta(response, status){
    
    if (status >= 200 && status <300){

        sweet_alert("Pago ingresado", "success");
        consulta_datos_prestamo();
        modificar_template_create();
    } else {
        sweet_alert("Hubo un problema!", "warning")
    }
}


function modificar_template_create(response){
    console.log(response);
}

async  function datos_para_editar(id_pago){

    const url = `${document.getElementById("host").value}api/api_pagos/${id_pago}/`;

    var respuesta = await fetch(url ,{
        method: "GET",
        headers: {
            'X-CSRFToken' : `${document.getElementById("token").value}`,
            'Content-Type': 'application/json',
        },

        });

    var response = await respuesta.json();
    var status = await respuesta.status;
    return validar_respuesta_editacion(response, status)

}

function validar_respuesta_editacion(response, status){
    
    if (status >= 200 && status <300){

        modificar_modal(response);
 
    } else {
        sweet_alert("Sin conexión", "warning")
    }
}

function modificar_modal(response){

    console.log(response)

    var pago_modal = document.getElementById("pago_modal")
    pago_modal.value = response.id

    var prestamo_modal = document.getElementById("prestamo_modal")
    prestamo_modal.value = response.prestamo

    var monto_modal = document.getElementById("monto_modal")
    monto_modal.value = response.monto

    var fecha_modal = document.getElementById("fecha_modal")
    fecha_modal.value = response.fecha
}

async  function editar_pago(){

    const url = `${document.getElementById("host").value}api/api_pagos/${document.getElementById("pago_modal").value}/`;

    var respuesta = await fetch(url ,{
        method: "PUT",
        headers: {
            'X-CSRFToken' : `${document.getElementById("token").value}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'prestamo' : document.getElementById("prestamo_modal").value,
            'fecha' : document.getElementById("fecha_modal").value,
            'monto' : document.getElementById("monto_modal").value,

        })

        });

    var response = await respuesta.json();
    var status = await respuesta.status;
    return validar_respuesta_editar(response, status)

}

function validar_respuesta_editar(response, status){
    
    if (status >= 200 && status <300){

        sweet_alert("Modificado", "success");
        modificar_tabla_editar(response);
 
    } else {
        sweet_alert("Hubo un problema!", "warning")
    }
}

function modificar_tabla_editar(response){

    var pago = document.getElementById(`pago_${response.id}`)
    pago.innerHTML = `$ ${response.monto}`

}

async  function borrar_pago(){

    var id_pago = document.getElementById("pago_modal").value

    const url = `${document.getElementById("host").value}api/api_pagos/${id_pago}/`;

    var respuesta = await fetch(url ,{
        method: "DELETE",
        headers: {
            'X-CSRFToken' : `${document.getElementById("token").value}`,
            'Content-Type': 'application/json',
        },

        });

    var status = await respuesta.status;
    return validar_respuesta_delete(id_pago, status)

}

function validar_respuesta_delete(id_pago, status){
    
    if (status >= 200 && status <300){

        sweet_alert("Pago eliminado", "success");
        modificar_tabla_delete(id_pago);
 
    } else {
        sweet_alert("Hubo un problema!", "warning")
    }
}

function modificar_tabla_delete(id_pago){

    console.log("Estoy en la parte de eliminar")
    var fila = document.getElementById(`fila_${id_pago}`)
    console.log(fila)
    fila.removeAttribute("class")
    fila.style = "display: none;"
    $('#ModalBorrar').modal('toggle')

}

// Queda pendiente la modificación del template cuando se crea y cambiar la fecha al editar
