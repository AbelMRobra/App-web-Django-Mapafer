

async function service_datos_prestamo(){
    const url = `${document.getElementById("host").value}api/api_prestamos/consulta_datos_crear_prestamo/`;
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${document.getElementById("token").value}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'tasa' : document.getElementById("select_formulario").value,
            'monto_incial' : document.getElementById("monto_inicial").value,
            'peridos_gracia' : document.getElementById("periodo_gracia").value,
            'regimen' : document.getElementById("regimen").value,
            'cantidad_cuotas' : document.getElementById("cuotas").value,
            'primera_cuota' : document.getElementById("primera_cuota").value
        })

    });

    var response = await respuesta.json();
    var status = await respuesta.status;
    return validar_respuesta_consulta_datos(response, status)
}
async function service_crear_prestamo(){

    sweet_alert("Procesando ..", "warning")

    const url = `${document.getElementById("host").value}api/api_prestamos/crear_prestamo/`;
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${document.getElementById("token").value}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'tasa' : document.getElementById("select_formulario").value,
            'monto_incial' : document.getElementById("monto_inicial").value,
            'peridos_gracia' : document.getElementById("periodo_gracia").value,
            'regimen' : document.getElementById("regimen").value,
            'cantidad_cuotas' : document.getElementById("cuotas").value,

            'cliente' : document.getElementById("cliente").value,
            'proveedor' : document.getElementById("proveedor").value,
            'presupuesto_cliente' : document.getElementById("presupuesto_cliente").value,
            'fecha' : document.getElementById("fecha").value,
            'primera_cuota' : document.getElementById("primera_cuota").value

        })

    });

    var response = await respuesta.json();
    var status = await respuesta.status;
    return validar_creacion(response, status)
}
async function service_datos_refinanciar(){

    try {
        sweet_alert("Consultando", "info")
        const url = `${document.getElementById("host").value}api/api_prestamos/consulta_datos_refinanciar_prestamo/`;
        var respuesta = await fetch(url ,{
            method: "POST",
            headers: {
                'X-CSRFToken' : `${document.getElementById("token").value}`,
                'Content-Type': 'application/json',
            },

            body: JSON.stringify({
                'credito' : document.getElementById("credito").value,
                'tasa_deuda' : document.getElementById("tasa_deuda").value,
                'tasa_saldo' : document.getElementById("tasa_saldo").value,
                'tasa' : document.getElementById("tasa").value,
                'monto_incial' : document.getElementById("monto_inicial").value,
                'monto_extra' : document.getElementById("monto_extra").value,
                'peridos_gracia' : document.getElementById("periodo_gracia").value,
                'regimen' : document.getElementById("regimen").value,
                'cantidad_cuotas' : document.getElementById("cuotas").value,
                'primera_cuota' : document.getElementById("primera_cuota").value
            })

        });

        var response = await respuesta.json();
        var status = await respuesta.status;
        return validar_respuesta_refinanciamiento(response, status)

    } catch (e) {
        console.log(e)
        sweet_alert("Error de Front", "error")
    }
    
}
async function service_crear_prestamo_refinanciado(){

    try {
        var loader = document.getElementById("loader_mapafer")
        loader.style = ' ';

        const url = `${document.getElementById("host").value}api/api_prestamos/crear_prestamo_refinanciado/`;
        var respuesta = await fetch(url ,{
            method: "POST",
            headers: {
                'X-CSRFToken' : `${document.getElementById("token").value}`,
                'Content-Type': 'application/json',
            },

            body: JSON.stringify({
                'credito': document.getElementById("credito").value,
                'tasa_deuda': document.getElementById("tasa_deuda").value,
                'tasa_saldo': document.getElementById("tasa_saldo").value,
                'tasa': document.getElementById("tasa").value,
                'monto_inicial': document.getElementById("monto_inicial").value,
                'monto_extra': document.getElementById("monto_extra").value,
                'peridos_gracia': document.getElementById("periodo_gracia").value,
                'regimen': document.getElementById("regimen").value,
                'cantidad_cuotas': document.getElementById("cuotas").value,
                'primera_cuota': document.getElementById("primera_cuota").value,
                'fecha': document.getElementById("fecha").value,
                'presupuesto_cliente': document.getElementById("presupuesto_cliente").value,
                'proveedor': document.getElementById("proveedor").value
            })

        });

        var response = await respuesta.json();
        var status = await respuesta.status;
        return validar_respuesta_creacion_refinanciada(response, status)
    } catch (e) {
        console.log(e)
        sweet_alert("Error de Front", "error")
    }
}
function validar_respuesta_creacion_refinanciada(response, status){

    if (status >= 200 && status <300){

        var loader = document.getElementById("loader_mapafer")
        loader.style = 'display: none;';

        var contenedor_prestamo = document.getElementById("contenedor_prestamo")
        contenedor_prestamo.style = 'display: none;';

        var boton_crear = document.getElementById("add2")
        boton_crear.style = 'display: none;';

        var contenedor_success = document.getElementById("contenedor_success")
        contenedor_success.style = ' ';

        sweet_alert("Prestamo creado", "success")

    } else {

        sweet_alert("No aceptado", "warning")
 
    }
}
function validar_respuesta_refinanciamiento(response, status){
    if (status >= 200 && status <300){
        sweet_alert("Calculado", "success")
        var monto_original = document.getElementById("monto_original")
        monto_original.innerHTML = `$ ${Intl.NumberFormat().format(response.monto_original)}`

        var deuda_original = document.getElementById("deuda_original")
        deuda_original.innerHTML = `Adeuda ${response.refinancimiento[0].CantidadDeuda} cuotas, un monto total de $ ${Intl.NumberFormat().format(response.refinancimiento[0].DeudaHistorica)} con interes son $ ${Intl.NumberFormat().format(response.refinancimiento[0].DeudaActual)}`

        var saldo_original = document.getElementById("saldo_original")
        saldo_original.innerHTML = `Pendiente ${response.refinancimiento[0].CantidadSaldo} cuotas, un monto total de $ ${Intl.NumberFormat().format(response.refinancimiento[0].SaldoHistorica)} con bonificaciones es son $ ${Intl.NumberFormat().format(response.refinancimiento[0].SaldoActual)}`
    
        var monto_minimo = document.getElementById("monto_inicial")
        console.log(monto_minimo.value)
        let valor_actual = response.refinancimiento[0].SaldoActual + response.refinancimiento[0].DeudaActual
        monto_minimo.value = valor_actual
        
        validar_respuesta_consulta_datos(response, status);
    } else {
        sweet_alert("Mala respuesta de la API", "error")
    }

}
function validar_respuesta_consulta_datos(response, status){

    if (status >= 200 && status <300){

        var monto_con_interes = document.getElementById("monto_con_interes")
        monto_con_interes.innerHTML = `$ ${Intl.NumberFormat().format(response.monto)}`

        var valor_cuota = document.getElementById("valor_cuota")
        valor_cuota.innerHTML = `$ ${Intl.NumberFormat().format(response.monto_cuota)}`

        if (document.getElementById("listado_cuotas")) {
            var listado = document.getElementById("listado_cuotas")
            listado.remove()
        }

        var contenedor = document.getElementById("contenedor_simulacion")
        var listado = document.createElement("ul")
        listado.id = "listado_cuotas"
        listado.className = "scrollbox mt-2"
        listado.style = "height: 60vh; overflow-y: auto;"
        contenedor.append(listado)

        for (let i=0; i <= response.simulacion.length -1; i++) {
            var cuota = document.createElement("h6")
            cuota.className = "mt-1"
            cuota.innerHTML = `Cuota Nº <b class="mr-2">${i+1}</b> <b class="text-info mr-2"> $ ${Intl.NumberFormat().format(response.monto_cuota)}</b> vence el <b class="text-primary ml-2"> ${response.simulacion[i]}</b>: `
            listado.appendChild(cuota)
        }

    } else {

        sweet_alert("No aceptado", "warning")
 
    }
}
function validar_creacion(response, status){

    if (status >= 200 && status <300){
        sweet_alert("Prestamo creado", "success")

    } else {
        sweet_alert("No aceptado", "warning")

    }
}
function mostrar_plan_cuotas(){
    var contendor_cuotas = document.getElementById("contenedor_plan_cuotas")
    contendor_cuotas.style = " "

    var contendor_cuotas = document.getElementById("contenedor_detalle")
    contendor_cuotas.style = "display: none;"
}

function mostrar_detalles(){
    var contendor_cuotas = document.getElementById("contenedor_plan_cuotas")
    contendor_cuotas.style = "display: none;"

    var contendor_cuotas = document.getElementById("contenedor_detalle")
    contendor_cuotas.style = " "
}