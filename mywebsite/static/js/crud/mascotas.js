$(function () {
    $("#btnBuscarcliente").on("click", function () {

    })
})

var Fn = {
    // Valida el rut con su cadena completa "XXXXXXXX-X"
    validaRut: function (rutCompleto) {
        if (!/^[0-9]+[-|‐]{1}[0-9kK]{1}$/.test(rutCompleto))
            return false;
        var tmp = rutCompleto.split('-');
        var digv = tmp[1];
        var rut = tmp[0];
        if (digv == 'K') digv = 'k';
        return (Fn.dv(rut) == digv);
    },
    dv: function (T) {
        var M = 0, S = 1;
        for (; T; T = Math.floor(T / 10))
            S = (S + T % 10 * (9 - M++ % 6)) % 11;
        return S ? S - 1 : 'k';
    }
}

function buscarCliente() {
    let buscar = $("#rut_cliente_id").val();

    if (buscar.length == 0) {
        alert("Por favor, ingrese el rut del cliente")
        return;
    }

    if (!Fn.validaRut(buscar)) {
        alert("El rut es inválido");
        return;
    }
    try
    {
        let url = `/mascotas/getcliente/${buscar}`
        $.getJSON(url, function(result){

            console.log(result);
            
          });
    }catch{
        alert("Se ha detectado un error de servidor.")
    }



}