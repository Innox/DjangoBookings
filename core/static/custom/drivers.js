$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-driver").modal("show");
            },
            success: function (data) {
                $("#modal-driver .modal-content").html(data.html_form);
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
                    $("#driver-table tbody").html(data.html_driver_list);
                    $("#modal-driver").modal("hide");
                } else {
                    $("#modal-driver .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    /* Binding */

    // Create driver
    $(".js-create-driver").click(loadForm);
    $("#modal-driver").on("submit", ".js-driver-create-form", saveForm);

    // Update driver
    $("#driver-table").on("click", ".js-update-driver", loadForm);
    $("#modal-driver").on("submit", ".js-driver-update-form", saveForm);

    // view driver
    $("#driver-table").on("click", ".js-view-driver", loadForm);
    $("#modal-driver").on("submit", ".js-driver-view-form", saveForm);
    
    // Delete driver
    $("#driver-table").on("click", ".js-delete-driver", loadForm);
    $("#modal-driver").on("submit", ".js-driver-delete-form", saveForm);

});
