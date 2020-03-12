$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-cab").modal("show");
            },
            success: function (data) {
                $("#modal-cab .modal-content").html(data.html_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        var formData = new FormData(form[0]);
        $.ajax({
            url: form.attr("action"),
            data: formData,
            type: form.attr("method"),
            dataType: 'json',
            async: true,
            cache: false,
            contentType: false,
            enctype: form.attr("enctype"),
            processData: false,
            success: function (data) {
                if (data.form_is_valid) {
                    $("#cab-table tbody").html(data.html_cab_list);
                    $("#modal-cab").modal("hide");
                } else {
                    $("#modal-cab .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    /* Binding */

    // Create cab
    $(".js-create-cab").click(loadForm);
    $("#modal-cab").on("submit", ".js-cab-create-form", saveForm);

    // Update cab
    $("#cab-table").on("click", ".js-update-cab", loadForm);
    $("#modal-cab").on("submit", ".js-cab-update-form", saveForm);

    // view cab
    $("#cab-table").on("click", ".js-view-cab", loadForm);
    $("#modal-cab").on("submit", ".js-cab-view-form", saveForm);
    
    // Delete cab
    $("#cab-table").on("click", ".js-delete-cab", loadForm);
    $("#modal-cab").on("submit", ".js-cab-delete-form", saveForm);

});
