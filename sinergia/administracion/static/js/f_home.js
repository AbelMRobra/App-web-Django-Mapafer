
window.onload = service_consulta_usuarios()

document.getElementById("usuarios").addEventListener("click", function(event){
    event.preventDefault()
    });


async function service_consulta_usuarios(){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    
    const url = `${document.getElementById("host").value}api/api_users/`

    var respuesta = await fetch(url ,{
        method: "GET",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

    })

    var response = await respuesta.json()
    var status = await respuesta.status

    return validar_consulta_usuarios(response, status)
}
    
function validar_consulta_usuarios(response, status){

    if (status >= 200 && status <300){

        if (document.getElementById('padre_listado')) {
            var listado = document.getElementById('padre_listado');
            listado.remove()

            if (response.length > 0) {
            
                modificar_listado_usuarios(response)
            } 
        } else {
            if (response.length > 0) {
                sweet_alert("Conexión exitosa a la BBDD", "info");
                modificar_listado_usuarios(response)
            } 
        }

        
    
    }
}
    
function modificar_listado_usuarios(response){

    var contenedor = document.getElementById('users');
    var listado= document.createElement('div');
    listado.id = `padre_listado`;
    contenedor.appendChild(listado);

    for (let i=0; i <= response.length -1; i++){
        var componente = document.createElement('div');
        componente.className = "bg-white shadow-sm mb-2 p-3"
        componente.id = `contedor_${response[i].id}`
        componente.innerHTML = `
        <div class="bg-proyecto-color box" onclick = "service_datos_usuario(${response[i].id})">
            <div class="justify-content-between w-100">
                <div class="d-flex text-left align-items-center">
                    <i class="fa fa-university text-info mr-2 mb-3"></i><span ><span class="font-bold w-100">${response[i].user.username}</span>  <span class="text-muted font-bold">
                    Rol otorgado: ${response[i].user_rol}</span></span>
                    
                </div>

            </div>
        </div>       
        `
        listado.appendChild(componente);
    }
    
}
async function service_datos_usuario(id){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    const url = `${document.getElementById("host").value}api/api_users/${id}/`;
    var respuesta = await fetch(url ,{
        method: "GET",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

    })

    var response = await respuesta.json()
    var status = await respuesta.status

    return validar_consulta_usuario(response, status)

}
function validar_consulta_usuario(response, status){

    if (status >= 200 && status <300){

        modificar_template_consulta_usuario(response)   
    }
}
function modificar_template_consulta_usuario(response){

    var principal_tree = document.getElementById('principal_tree');
    principal_tree.style = "display: none;";

    var principal_detail = document.getElementById('principal_detail');
    principal_detail.style = "";

    upload_data_reverse()

    var id = document.getElementById('id_upload');
    id.value = response.id;

    var username = document.getElementById('username');
    username.innerHTML = response.user.username;

    var username_edit = document.getElementById('username_edit');
    username_edit.value = response.user.username;

    var email = document.getElementById('email');
    email.innerHTML = response.user.email;

    var email_edit = document.getElementById('email_edit');
    email_edit.value = response.user.email;

    var user_rol = document.getElementById('user_rol');
    user_rol.innerHTML = response.user_rol;

    var user_rol_edit = document.getElementById('user_rol_edit');
    user_rol_edit.value = response.user_rol;

}
function upload_data(){

    var username = document.getElementById('username');
    username.style = "display: none;";

    var username_edit = document.getElementById('username_edit');
    username_edit.style = "";

    var email = document.getElementById('email');
    email.style = "display: none;";

    var email_edit = document.getElementById('email_edit');
    email_edit.style = "";

    var user_rol = document.getElementById('user_rol');
    user_rol.style= "display: none;";

    var user_rol_edit = document.getElementById('user_rol_edit');
    user_rol_edit.style = "";

    var button_delete = document.getElementById('button_delete');
    button_delete.style = "";

}
function upload_data_reverse(){

    var username = document.getElementById('username');
    username.style = "";

    var username_edit = document.getElementById('username_edit');
    username_edit.style = "display: none;";

    var email = document.getElementById('email');
    email.style = "";

    var email_edit = document.getElementById('email_edit');
    email_edit.style = "display: none;";

    var user_rol = document.getElementById('user_rol');
    user_rol.style= "";

    var user_rol_edit = document.getElementById('user_rol_edit');
    user_rol_edit.style = "display: none;";

    var button_delete = document.getElementById('button_delete');
    button_delete.style = "display: none;";

 

}
// Para modificar o editar los datos de los perfiles existentes

async function service_upload_user(){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    id = document.getElementById('id_upload').value;

    const url = `${document.getElementById("host").value}api/api_users/${id}/editar_usuario/`;
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "user_rol" : document.getElementById('user_rol_edit').value,
            "username" : document.getElementById('username_edit').value,
            "email" : document.getElementById('email_edit').value,

        })

    })

    var status = await respuesta.status

    return validar_upload_user(status)

}

function validar_upload_user(status){

    if (status >= 200 && status <300){
        sweet_alert("Perfil editado", "success");
        service_consulta_usuarios();
        service_datos_usuario();
        upload_data();
    }
}
    

// Validar contraseña

function validar_password(){

    var pass_1 = document.getElementById("pass")
    var pass_2 = document.getElementById("pass_2")
    var container_pass = document.getElementById("container_pass_2")
    var lenght_pass = new String(pass_1.value).length

    if (pass_1.value === pass_2.value && lenght_pass > 8) {
        pass_2.className = "form-control form-control-success"
        container_pass.className = "form-group has-success"
    } else {
        pass_2.className = "form-control form-control-danger"
        container_pass.className = "form-group has-danger"
    }


}

// Crear un usuario

async  function service_create_user(){

    const url = `${document.getElementById("host").value}api/api_users/`;

    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${document.getElementById("token").value}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'username' : document.getElementById("username_create").value,
            'password' : document.getElementById("pass_2").value,
            'email' : document.getElementById("email_create").value,
            'user_rol': document.getElementById("user_rol_create").value,

        })

        });

    var status = await respuesta.status;
    return validar_upload_user(status)

}

function validar_upload_user(status){

    if (status >= 200 && status <300){
        sweet_alert("Perfil creado", "success");
        service_consulta_usuarios();

    } else{
        sweet_alert("Datos no aceptados", "warning");
    }
}

// Service para eliminar usuario


async function service_delete_user(){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    id = document.getElementById('id_upload').value;

    const url = `${document.getElementById("host").value}api/api_users/${id}/`;
    var respuesta = await fetch(url ,{
        method: "DELETE",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },
    })

    var status = await respuesta.status

    return validar_delete_user(status)

}

function validar_delete_user(status){

    if (status >= 200 && status <300){
        sweet_alert("Perfil borrado", "success");
        service_consulta_usuarios();

        var principal_tree = document.getElementById('principal_tree');
        principal_tree.style = "";

        var principal_detail = document.getElementById('principal_detail');
        principal_detail.style = "display: none;";

    } else{
        sweet_alert("Error inesperado", "warning");
    }
}