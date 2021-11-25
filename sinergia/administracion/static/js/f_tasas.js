
function traer_nombre () {
    for (let i=0; i <= data_tasas.length -1; i++){

        if (data_tasas[i].id == document.getElementById("campo_id_tasa").value) {
            return data_tasas[i].nombre;

            
        }

    }
}

async function modificar_tasa() {

    const url = `${document.getElementById("host").value}api/api_tasas/${document.getElementById("campo_id_tasa").value}/`;

    var nombre = traer_nombre();

    var respuesta = await fetch(url ,{
        method: "PUT",
        headers: {
            'X-CSRFToken' : `${document.getElementById("token").value}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'nombre' : nombre,
            'valor_tasa' : document.getElementById("campo_valor_tasa").value,

        })
        });

    var response = await respuesta.json();
    var status = await respuesta.status
    return validar_respuesta(response, status);
    }

function validar_respuesta(response, status){
    
    if (status >= 200 && status <300){

        sweet_alert("Tasa editada", "success");


        for (let i=0; i <= data_tasas.length -1; i++){

            if (data_tasas[i].id == response.id) {
                data_tasas[i].valor_tasa = response.valor_tasa;

                
            } 

        }

        var option = document.getElementById(`option_formulario_${response.id}`);
        option.value = response.valor_tasa;
        option.text = `${response.nombre} (${response.valor_tasa}%)`;

        edicion_tasas_valor();
    } else {
        sweet_alert("Hubo un problema!", "warning")
    }
}

function edicion_tasas_valor() {

    
    var campo_nombre_tasa = document.getElementById("campo_nombre_tasa");
    var campo_valor_tasa = document.getElementById("campo_valor_tasa");
    var campo_id_tasa = document.getElementById("campo_id_tasa");

    for (let i=0; i <= data_tasas.length -1; i++){

        if (data_tasas[i].id == campo_nombre_tasa.value) {
            campo_valor_tasa.value = data_tasas[i].valor_tasa;
            campo_id_tasa.value = data_tasas[i].id;
            console.log(data_tasas[i].id);
            
        }
        
    }



}

async function crear_tasa() {

    const url = `${document.getElementById("host").value}api/api_tasas/`;

    var nombre = traer_nombre();

    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${document.getElementById("token").value}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'nombre' : document.getElementById("campo_nombre_newtasa").value,
            'valor_tasa' : document.getElementById("campo_valor_newtasa").value,

        })
        });

    var response = await respuesta.json();
    var status = await respuesta.status
    return validar_creacion(response, status);
}

function validar_creacion(response, status) {
    if (status >= 200 && status <300){

        sweet_alert("Tasa creada", "success");

        modificar_select(response);


        edicion_tasas_valor();
    } else {
        sweet_alert("Hubo un problema!", "warning")
    }
}

function modificar_select(response) {

    var select = document.getElementById('campo_nombre_tasa');
    var option = document.createElement('option');
    option.id = `modal_option_${response.id}`;
    option.value = response.id;
    option.text = response.nombre;
    select.appendChild(option);

    var select = document.getElementById('select_formulario');
    var option = document.createElement('option');
    option.id = `option_formulario_${response.id}`;
    option.value = response.valor_tasa;
    option.text = `${response.nombre} (${response.valor_tasa}%)`;
    select.appendChild(option);

    data_tasas.unshift(response);
    console.log(data_tasas);

}

async function eliminar_tasa() {

    var id_tasa = document.getElementById("campo_id_tasa").value

    const url = `${document.getElementById("host").value}api/api_tasas/${id_tasa}/`;

    var respuesta = await fetch(url ,{
        method: "DELETE",
        headers: {
            'X-CSRFToken' : `${document.getElementById("token").value}`,
            'Content-Type': 'application/json',
        },

        });


    var status = await respuesta.status
    return validar_delete(id_tasa, status);
}

function validar_delete(id_tasa, status) {
    if (status >= 200 && status <300){

        sweet_alert("Tasa eliminada", "success");

        modificar_select_delete(id_tasa);


        edicion_tasas_valor();
    } else {
        sweet_alert("Hubo un problema!", "warning")
    }
}

function modificar_select_delete(id_tasa) {

    var option = document.getElementById(`modal_option_${id_tasa}`);
    option.remove()

    var option = document.getElementById(`option_formulario_${id_tasa}`);
    option.remove()
    
    data_tasas.unshift(response);


}
