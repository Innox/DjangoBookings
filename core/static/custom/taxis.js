$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-taxi").modal("show");
            },
            success: function (data) {
                $("#modal-taxi .modal-content").html(data.html_form);
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
                    $("#taxi-table tbody").html(data.html_taxi_list);
                    $("#modal-taxi").modal("hide");
                } else {
                    $("#modal-taxi .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    /* Binding */

    // Create taxi
    $(".js-create-taxi").click(loadForm);
    $("#modal-taxi").on("submit", ".js-taxi-create-form", saveForm);

    // Update taxi
    $("#taxi-table").on("click", ".js-update-taxi", loadForm);
    $("#modal-taxi").on("submit", ".js-taxi-update-form", saveForm);

    // view taxi
    $("#taxi-table").on("click", ".js-view-taxi", loadForm);
    $("#modal-taxi").on("submit", ".js-taxi-view-form", saveForm);
    
    // Delete taxi
    $("#taxi-table").on("click", ".js-delete-taxi", loadForm);
    $("#modal-taxi").on("submit", ".js-taxi-delete-form", saveForm);

});
