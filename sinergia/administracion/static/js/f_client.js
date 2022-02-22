

async function service_borrar_cliente(id) {
    const url = `${document.getElementById("host").value}api/api_clientes/${id}/`;
    sweet_alert("Procesando ..", "warning");
    var respuesta = await fetch(url ,{
        method: "DELETE",
        headers: {
            'X-CSRFToken' : `${document.getElementById("token").value}`,
            'Content-Type': 'application/json',
        },

    });

    var status = await respuesta.status;
    return validar_respuesta_borrado(status, id)
}

async function service_crear_cliente() {
    const url = `${document.getElementById("host").value}api/api_clientes/`;
    sweet_alert("Procesando ..", "warning");
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${document.getElementById("token").value}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'nombre' : document.getElementById("nombre").value,
            'apellido' : document.getElementById("apellido").value,
            'score' : document.getElementById("score").value,
            'email' : document.getElementById("email").value,
            'cuil' : document.getElementById("cuil").value,
            'telefono' : document.getElementById("telefono").value,
            'direccion' : document.getElementById("direccion").value,
            'empresa' : document.getElementById("empresa").value,
            'username' : document.getElementById("username").value,
            'password' : document.getElementById("password").value,
            'localidad' : document.getElementById("localidad").value,
            'provincia' : document.getElementById("provincia").value
        })

    });

    var response = await respuesta.json();
    var status = await respuesta.status;
    return validar_respuesta_creacion(response, status)
}

function validar_respuesta_creacion(response, status){
    
    if (status >= 200 && status <300){
        sweet_alert("Cliente creado", "success")
    } else {
        sweet_alert(response.message, "error")
    }
}

function validar_respuesta_borrado(status, id){
    
    if (status >= 200 && status <300){
        sweet_alert("Perfecto", "success");
        var row = document.getElementById(`${id}`)
        row.remove()
    } else {
        sweet_alert("Problema de servidor", "error")
    }
}

function autocompletar_user(){

    var nombre = document.getElementById("nombre").value
    var apellido = document.getElementById("apellido").value
    var cuil = document.getElementById("cuil").value

    var username = document.getElementById("username")
    username.value = `${String(cuil).replace("-", "")}`
    var password = document.getElementById("password")
    password.value = `${String(cuil).replace("-", "")}`
    

}