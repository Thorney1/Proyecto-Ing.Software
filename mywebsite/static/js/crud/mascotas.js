$(function () {


    $(".action").on("click", function (event) {
        event.preventDefault();
        let url = $(this).attr("href");
        let action = $(this).attr("action");
        console.log(url);
        Swal.fire({
            title: "¿Está seguro/a?",
            text: action,
            icon: "question",
            showCancelButton: true,
            confirmButtonText: '¡Continuar!',
            cancelButtonText: '¡Cancelar!'
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = url;
            }
        })
    });

    $(".show").on("click", function (event) {
        event.preventDefault();
        let id = $(this).attr("id_animal");
        $.ajax({
            url: `/mascotas/traer-detalle/${id}`,
            type: 'GET',
            dataType: 'json',
            statusCode: {
                200: function (response) {
                    console.log('200', response)
                    let table = print_list(response)
                    Swal.fire({
                        title: "Diagnostico",
                        html: table,
                        icon: "info",
                        showCancelButton: true,
                        showConfirmButton: false,
                        cancelButtonText: '¡Cerrar!'
                    })
                },
                500: function (message) {
                    Swal.fire({
                        title: "Proceso terminado",
                        text: "Error de servidor.",
                        icon: "error"
                    });
                }
            }
        });

    $(".show1").on("click", function (event) {
        event.preventDefault();
        let id = $(this).attr("id_animal");
        $.ajax({
            url: `/atenciones/traer-detalle/${id}`,
            type: 'GET',
            dataType: 'json',
            statusCode: {
                200: function (response) {
                    console.log('200', response)
                    let table = print_list(response)
                    Swal.fire({
                        title: "Diagnostico",
                        html: table,
                        icon: "info",
                        showCancelButton: true,
                        showConfirmButton: false,
                        cancelButtonText: '¡Cerrar!'
                    })
                },
                500: function (message) {
                    Swal.fire({
                        title: "Proceso terminado",
                        text: "Error de servidor.",
                        icon: "error"
                    });
                }
            }
        });
    });

    // $(".delete").on("click", function(event){
    //     event.preventDefault();
    //     let url = $(this).attr("href");
    //     console.log(url);
    //     Swal.fire({
    //         title: "¿Está seguro/a?",
    //         text: "Usted eliminará este diagnotico",
    //         icon: "question",
    //         showCancelButton: true,
    //         confirmButtonText: '¡Continuar!',
    //         cancelButtonText: '¡Cancelar!'
    //     }).then((result) => {
    //         if (result.isConfirmed) {
    //             window.location.href = url;
    //         }
    //     })
    // });


    // $(".edit").on("click", function(event){
    //     event.preventDefault();
    //     let url = $(this).attr("href");
    //     console.log(url);
    //     Swal.fire({
    //         title: "¿Está seguro/a?",
    //         text: "Usted irá a la ventana de editar",
    //         icon: "question",
    //         showCancelButton: true,
    //         confirmButtonText: '¡Continuar!',
    //         cancelButtonText: '¡Cancelar!'
    //     }).then((result) => {
    //         if (result.isConfirmed) {
    //             window.location.href = url;
    //         }
    //     })
    // });



})


function print_list(data) {
    let new_line = '<table>'
    new_line += '<tbody>'

    for (let index = 0; index < data.length; index++) {
        new_line += '<tr>'
        new_line += `<td>${data[index]}</td>`
        new_line += `<td>${data[index + 1]}</td>`
        new_line += '</tr>'

    }
    new_line += '</tbody>'
    new_line += '</table>'
    return new_line
}})