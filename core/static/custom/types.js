$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-type").modal("show");
            },
            success: function (data) {
                $("#modal-type .modal-content").html(data.html_form);
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
                    $("#type-table tbody").html(data.html_type_list);
                    $("#modal-type").modal("hide");
                } else {
                    $("#modal-type .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    /* Binding */

    // Create type
    $(".js-create-type").click(loadForm);
    $("#modal-type").on("submit", ".js-type-create-form", saveForm);

    // Update type
    $("#type-table").on("click", ".js-update-type", loadForm);
    $("#modal-type").on("submit", ".js-type-update-form", saveForm);

    // view type
    $("#type-table").on("click", ".js-view-type", loadForm);
    $("#modal-type").on("submit", ".js-type-view-form", saveForm);
    
    // Delete type
    $("#type-table").on("click", ".js-delete-type", loadForm);
    $("#modal-type").on("submit", ".js-type-delete-form", saveForm);

});
