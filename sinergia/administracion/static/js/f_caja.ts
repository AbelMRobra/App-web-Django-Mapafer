
var service 
var template_utils 

(() => {

    type ResponseCreate = {
        "id": number,
        "cuenta": string,
        "concepto": string,
        "fecha": string,
        "ingreso": boolean,
        "monto": number,
    };

    const token:string = `${(document.getElementById('token') as HTMLInputElement).value}`;
    const host:string = `${(document.getElementById('host') as HTMLInputElement).value}`;

    class TemplateUtils {
        show_message:Function = (status_code:number, message?:string) => {
            switch (status_code) {
                case 0:
                    sweet_alert("Procesando ..", "info");
                    break;

                case 2:
                    sweet_alert("Error en el servicio", "error");
                    break;
                
                case 201:
                    sweet_alert("Creado!", "success");
                    break;

                default:
                    sweet_alert("Problemas", "error");
                    break;
            }

        };

        add_row:Function = (response:ResponseCreate) => {
            var table = $('#balance').DataTable();
            var ingreso = (response.ingreso) ? '<b class="text-success">INGRESO</b>' : '<b class="text-danger">SALIDA</b>'
 
            table.row.add( [
                `<b class="text-info table_row" 
                onClick="service.open_modal(${response.id})" 
                data-toggle="modal" data-target="#ModalEditarRegistros">${response.cuenta}</b>`,
                response.concepto,
                response.fecha,
                ingreso,
                `$${response.monto}`,

            ]).node().id = `mov_${response.id}`
            table.draw();

        };

        delete_row:Function = (id:number) => {
            var table = $('#balance').DataTable();
            table.row(`#mov_${id}`).remove().draw();
        };


    }

    class ServiceRegistrosContables {
        url_principal:string = `${ host }api/api-caja/`
        template_utils = new TemplateUtils()
        say_status:Function = () => {
            console.log("Service is ready")
        };

        open_modal:Function = (id:number) => {
            console.log("Open modal");

            this.get_record_data(id);

            var boton:HTMLButtonElement = (document.getElementById('delete_boton') as HTMLButtonElement);
            boton.onclick = () => {
                this.delete_data(id);
            };

            var boton_upload:HTMLButtonElement = (document.getElementById('editar_boton') as HTMLButtonElement);
            boton_upload.onclick = () => {
                this.upload_data(id);
            };
        };

        get_record_data:Function = async (id:number) => {
            var request = await fetch(`${this.url_principal}${id}` ,{
                method: "GET",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken' : `${token}`,
                },

            }).catch((error) => {
                console.log(error);
                sweet_alert('Problemas al pedir data', 'error');
            })

            var response = await request.json();
            var status_code = await request.status;
            
            var template_managment = ():void => {
                if (status_code >= 200 && status_code < 300) {
                    console.log("Consulta exitosa");
                    console.log(response);

                    var up_cuenta:HTMLFormElement = (document.getElementById('up_cuenta') as HTMLFormElement);
                    up_cuenta.value = response.cuenta;
                    
                    var up_concepto:HTMLFormElement = (document.getElementById('up_concepto') as HTMLFormElement);
                    up_concepto.value = response.concepto;

                    var up_fecha:HTMLFormElement = (document.getElementById('up_fecha') as HTMLFormElement);
                    up_fecha.value = response.fecha;

                    var up_monto:HTMLFormElement = (document.getElementById('up_monto') as HTMLFormElement);
                    up_monto.value = response.monto;

                    var up_ingreso:HTMLFormElement = (document.getElementById('up_ingreso') as HTMLFormElement);
                    if (response.ingreso) {
                        up_ingreso.checked = true;
                    } else {
                        up_ingreso.checked = false;
                    }
                                    
                } else {
                    console.log("Consulta fallida");
                    console.log(response);
                    sweet_alert('Problemas de servidor', 'error');
                }
            };
            template_managment();
        };

        delete_data:Function = async (id:number) => {

            var request = await fetch(`${this.url_principal}${id}/` ,{
                method: "DELETE",
                headers: {
                    'X-CSRFToken' : `${token}`,
                    'Content-Type': 'application/json',
                },

            }).catch((error) => {
                console.log(error);
                sweet_alert('Problemas al enviar', 'error');
            })

            var status_code = await request.status;
            
            var template_managment = ():void => {
                if (status_code >= 200 && status_code < 300) {
                    this.template_utils.delete_row(id);
                    sweet_alert('Borrado!', 'success');
                } else {
                    sweet_alert('Problemas en el servidor', 'error');
                }
            };
            template_managment();
        };

        add_record:Function = async () => {
            this.template_utils.show_message(0);
            var request = await fetch(this.url_principal ,{
                method: "POST",
                headers: {
                    'X-CSRFToken' : `${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'ingreso': `${ (document.getElementById('nr_ingreso') as HTMLInputElement).checked}`,
                    'cuenta': `${(document.getElementById('nr_cuenta') as HTMLInputElement).value}`,
                    'concepto': `${(document.getElementById('nr_concepto') as HTMLInputElement).value}`,
                    'fecha': `${(document.getElementById('nr_fecha') as HTMLInputElement).value}`,
                    'monto': `${(document.getElementById('nr_monto') as HTMLInputElement).value}`
                })
            }).catch((error) => {
                var message = this.template_utils.show_message(2)
            })

            var response = await request.json()
            var status_code = await request.status
            var message = await this.template_utils.show_message(status_code)
            var template_managment = ():void => {
                console.log(response)
                if (status_code >= 200 && status_code < 300) {
                    console.log("Agregando fila")
                    this.template_utils.add_row(response)
                }
            }

            template_managment()
        };

        upload_data:Function = async (id:number) => {

            var request = await fetch(`${this.url_principal}${id}/` ,{
                method: "PATCH",
                headers: {
                    'X-CSRFToken' : `${token}`,
                    'Content-Type': 'application/json',
                },
                
                body: JSON.stringify({
                    'cuenta': `${ (document.getElementById('up_cuenta') as HTMLInputElement).value}`,
                    'concepto': `${(document.getElementById('up_concepto') as HTMLInputElement).value}`,
                    'fecha': `${(document.getElementById('up_fecha') as HTMLInputElement).value}`,
                    'monto': `${(document.getElementById('up_monto') as HTMLInputElement).value}`,
                    'ingreso': `${ (document.getElementById('up_ingreso') as HTMLInputElement).checked}`,

                })

            }).catch((error) => {
                console.log(error);
                sweet_alert('Problemas al enviar', 'error');
            })

            var response = await request.json();
            var status_code = await request.status;
            
            var template_managment = ():void => {
                if (status_code >= 200 && status_code < 300) {
                    sweet_alert('Editado!', 'success');
                    var delete_row = this.template_utils.delete_row(response.id);
                    var add_row = this.template_utils.add_row(response);
  
                } else {
                    sweet_alert('Problemas de servidor', 'error');
                }
            };
            
            template_managment();
        };
    };

    service = new ServiceRegistrosContables();
    template_utils = new TemplateUtils();
    service.say_status();
  
})()

