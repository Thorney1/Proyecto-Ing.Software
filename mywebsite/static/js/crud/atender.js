$(function () {
    $("#add-row").on("click", function () {
        add_row();
    });
})

function add_row() {
    let genId = uuidv4();

    let newtr = '<tr>'
    newtr += `<td><input type="text" name="detail_${genId}" id="id_detail_${genId}" class="form-control"/></td>`
    newtr += `<td><input type="text" name="medicamento_${genId}" id="id_medicamento${genId}" class="form-control"/></td>`
    newtr += '<td><button type="button" class="btn btn-danger btn-sm remove-item" data-datakey="' + genId + '"><i class="fa fa-times"></i></button></td>';
    newtr += '</tr>'

    $('#table-data').prepend(newtr);
    let hiddenKeys = '<input type="hidden" id="rowKey_' + genId + '" name="rowKey[]" value="' + genId + '" />';

    $("#hidden-keys").append(hiddenKeys);
    $('.remove-item').off().on("click", function () {
        var datakey = $(this).data("datakey");
        $("#rowKey_" + datakey).remove();
        $(this).parent('td').parent('tr').remove();
        if ($('#table-data tr.item').length == 0)
            $('#table-data .no-item').slideDown(300);
    });
}

function uuidv4() {
    return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}