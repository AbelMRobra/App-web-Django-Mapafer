window.onload = service_user_datos_prestamo();


async function service_user_datos_prestamo(){
    const url = `${document.getElementById("host").value}api/api_prestamos/consulta_user/`;
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${document.getElementById("token").value}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'id' : document.getElementById("user_id").value,
        })

    });

    var response = await respuesta.json();
    var status = await respuesta.status;
    return validar_respuesta_consulta_user(response, status)
}

function validar_respuesta_consulta_user(response, status){

    if (status >= 200 && status <300){

        var monto = document.getElementById("monto")
        monto.innerHTML = `$ ${Intl.NumberFormat().format(response.monto_prestamo)}`

        var cuotas = document.getElementById("cuotas")
        cuotas.innerHTML = `${response.cantidad_pendientes}/${response.cantidad_cuotas}`

        var monto_proxima_cuota = document.getElementById("monto_proxima_cuota")
        monto_proxima_cuota.innerHTML = `$ ${Intl.NumberFormat().format(response.monto_proxima_cuota)}`

        var proximo_vencimiento = document.getElementById("proximo_vencimiento")
        proximo_vencimiento.innerHTML = `${response.proximo_vencimiento}`


    } else {

        sweet_alert("No aceptado", "warning")
 
    }
}
