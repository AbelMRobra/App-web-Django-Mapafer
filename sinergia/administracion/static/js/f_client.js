

async function service_crear_cliente() {

    const url = `${document.getElementById("host").value}api/api_clientes/`;
    
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
            'telfono' : document.getElementById("telfono").value,
            'direccion' : document.getElementById("direccion").value,
            'empresa' : document.getElementById("empresa").value,
            'username' : document.getElementById("username").value,
            'password' : document.getElementById("password").value,
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
        console.log(Object.keys(response))
        let errors = Object.keys(response)
        for (let i=0; i <= errors.length -1; i++){
            console.log(response[errors[i]])
        }

        sweet_alert("No aceptado", "warning")
 
    }
}

function autocompletar_user(){

    var nombre = document.getElementById("nombre").value
    var apellido = document.getElementById("apellido").value
    var cuil = document.getElementById("cuil").value

    var username = document.getElementById("username")
    username.value = `${nombre}${apellido}`
    var password = document.getElementById("password")
    password.value = `${String(cuil).replace("-", "")}`
    

}