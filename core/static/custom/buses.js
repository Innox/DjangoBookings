$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-bus").modal("show");
            },
            success: function (data) {
                $("#modal-bus .modal-content").html(data.html_form);
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
                    $("#bus-table tbody").html(data.html_bus_list);
                    $("#modal-bus").modal("hide");
                } else {
                    $("#modal-bus .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    /* Binding */

    // Create bus
    $(".js-create-bus").click(loadForm);
    $("#modal-bus").on("submit", ".js-bus-create-form", saveForm);

    // Update bus
    $("#bus-table").on("click", ".js-update-bus", loadForm);
    $("#modal-bus").on("submit", ".js-bus-update-form", saveForm);

    // view bus
    $("#bus-table").on("click", ".js-view-bus", loadForm);
    $("#modal-bus").on("submit", ".js-bus-view-form", saveForm);
    
    // Delete bus
    $("#bus-table").on("click", ".js-delete-bus", loadForm);
    $("#modal-bus").on("submit", ".js-bus-delete-form", saveForm);

});
