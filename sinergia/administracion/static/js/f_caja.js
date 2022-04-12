"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var service;
var template_utils;
(() => {
    const token = `${document.getElementById('token').value}`;
    const host = `${document.getElementById('host').value}`;
    class TemplateUtils {
        constructor() {
            this.show_message = (status_code, message) => {
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
            this.add_row = (response) => {
                var table = $('#balance').DataTable();
                var ingreso = (response.ingreso) ? '<b class="text-success">INGRESO</b>' : '<b class="text-danger">SALIDA</b>';
                table.row.add([
                    `<b class="text-info table_row" 
                onClick="service.open_modal(${response.id})" 
                data-toggle="modal" data-target="#ModalEditarRegistros">${response.cuenta}</b>`,
                    response.concepto,
                    response.fecha,
                    ingreso,
                    `$${response.monto}`,
                ]).node().id = `mov_${response.id}`;
                table.draw();
            };
            this.delete_row = (id) => {
                var table = $('#balance').DataTable();
                table.row(`#mov_${id}`).remove().draw();
            };
        }
    }
    class ServiceRegistrosContables {
        constructor() {
            this.url_principal = `${host}api/api-caja/`;
            this.template_utils = new TemplateUtils();
            this.say_status = () => {
                console.log("Service is ready");
            };
            this.open_modal = (id) => {
                console.log("Open modal");
                this.get_record_data(id);
                var boton = document.getElementById('delete_boton');
                boton.onclick = () => {
                    this.delete_data(id);
                };
                var boton_upload = document.getElementById('editar_boton');
                boton_upload.onclick = () => {
                    this.upload_data(id);
                };
            };
            this.get_record_data = (id) => __awaiter(this, void 0, void 0, function* () {
                var request = yield fetch(`${this.url_principal}${id}`, {
                    method: "GET",
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': `${token}`,
                    },
                }).catch((error) => {
                    console.log(error);
                    sweet_alert('Problemas al pedir data', 'error');
                });
                var response = yield request.json();
                var status_code = yield request.status;
                var template_managment = () => {
                    if (status_code >= 200 && status_code < 300) {
                        console.log("Consulta exitosa");
                        console.log(response);
                        var up_cuenta = document.getElementById('up_cuenta');
                        up_cuenta.value = response.cuenta;
                        var up_concepto = document.getElementById('up_concepto');
                        up_concepto.value = response.concepto;
                        var up_fecha = document.getElementById('up_fecha');
                        up_fecha.value = response.fecha;
                        var up_monto = document.getElementById('up_monto');
                        up_monto.value = response.monto;
                        var up_ingreso = document.getElementById('up_ingreso');
                        if (response.ingreso) {
                            up_ingreso.checked = true;
                        }
                        else {
                            up_ingreso.checked = false;
                        }
                    }
                    else {
                        console.log("Consulta fallida");
                        console.log(response);
                        sweet_alert('Problemas de servidor', 'error');
                    }
                };
                template_managment();
            });
            this.delete_data = (id) => __awaiter(this, void 0, void 0, function* () {
                var request = yield fetch(`${this.url_principal}${id}/`, {
                    method: "DELETE",
                    headers: {
                        'X-CSRFToken': `${token}`,
                        'Content-Type': 'application/json',
                    },
                }).catch((error) => {
                    console.log(error);
                    sweet_alert('Problemas al enviar', 'error');
                });
                var status_code = yield request.status;
                var template_managment = () => {
                    if (status_code >= 200 && status_code < 300) {
                        this.template_utils.delete_row(id);
                        sweet_alert('Borrado!', 'success');
                    }
                    else {
                        sweet_alert('Problemas en el servidor', 'error');
                    }
                };
                template_managment();
            });
            this.add_record = () => __awaiter(this, void 0, void 0, function* () {
                this.template_utils.show_message(0);
                var request = yield fetch(this.url_principal, {
                    method: "POST",
                    headers: {
                        'X-CSRFToken': `${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        'ingreso': `${document.getElementById('nr_ingreso').checked}`,
                        'cuenta': `${document.getElementById('nr_cuenta').value}`,
                        'concepto': `${document.getElementById('nr_concepto').value}`,
                        'fecha': `${document.getElementById('nr_fecha').value}`,
                        'monto': `${document.getElementById('nr_monto').value}`
                    })
                }).catch((error) => {
                    var message = this.template_utils.show_message(2);
                });
                var response = yield request.json();
                var status_code = yield request.status;
                var message = yield this.template_utils.show_message(status_code);
                var template_managment = () => {
                    console.log(response);
                    if (status_code >= 200 && status_code < 300) {
                        console.log("Agregando fila");
                        this.template_utils.add_row(response);
                    }
                };
                template_managment();
            });
            this.upload_data = (id) => __awaiter(this, void 0, void 0, function* () {
                var request = yield fetch(`${this.url_principal}${id}/`, {
                    method: "PATCH",
                    headers: {
                        'X-CSRFToken': `${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        'cuenta': `${document.getElementById('up_cuenta').value}`,
                        'concepto': `${document.getElementById('up_concepto').value}`,
                        'fecha': `${document.getElementById('up_fecha').value}`,
                        'monto': `${document.getElementById('up_monto').value}`,
                        'ingreso': `${document.getElementById('up_ingreso').checked}`,
                    })
                }).catch((error) => {
                    console.log(error);
                    sweet_alert('Problemas al enviar', 'error');
                });
                var response = yield request.json();
                var status_code = yield request.status;
                var template_managment = () => {
                    if (status_code >= 200 && status_code < 300) {
                        sweet_alert('Editado!', 'success');
                        var delete_row = this.template_utils.delete_row(response.id);
                        var add_row = this.template_utils.add_row(response);
                    }
                    else {
                        sweet_alert('Problemas de servidor', 'error');
                    }
                };
                template_managment();
            });
        }
    }
    ;
    service = new ServiceRegistrosContables();
    template_utils = new TemplateUtils();
    service.say_status();
})();
