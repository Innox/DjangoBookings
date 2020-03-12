$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-accommodation").modal("show");
            },
            success: function (data) {
                $("#modal-accommodation .modal-content").html(data.html_form);
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
                    $("#accommodation-table tbody").html(data.html_accommodation_list);
                    $("#modal-accommodation").modal("hide");
                } else {
                    $("#modal-accommodation .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    /* Binding */

    // Create accommodation
    $(".js-create-accommodation").click(loadForm);
    $("#modal-accommodation").on("submit", ".js-accommodation-create-form", saveForm);

    // Update accommodation
    $("#accommodation-table").on("click", ".js-update-accommodation", loadForm);
    $("#modal-accommodation").on("submit", ".js-accommodation-update-form", saveForm);

    // view accommodation
    $("#accommodation-table").on("click", ".js-view-accommodation", loadForm);
    $("#modal-accommodation").on("submit", ".js-accommodation-view-form", saveForm);
    
    // Delete accommodation
    $("#accommodation-table").on("click", ".js-delete-accommodation", loadForm);
    $("#modal-accommodation").on("submit", ".js-accommodation-delete-form", saveForm);

});
