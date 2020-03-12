$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-about").modal("show");
            },
            success: function (data) {
                $("#modal-about .modal-content").html(data.html_form);
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
                    $("#about-table tbody").html(data.html_about_list);
                    $("#modal-about").modal("hide");
                } else {
                    $("#modal-about .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create about
    $(".js-create-about").click(loadForm);
    $("#modal-about").on("submit", ".js-about-create-form", saveForm);

    // view about
    $("#about-table").on("click", ".js-view-about", loadForm);
    $("#modal-about").on("submit", ".js-about-view-form", saveForm);

    // Update about
    $("#about-table").on("click", ".js-update-about", loadForm);
    $("#modal-about").on("submit", ".js-about-update-form", saveForm);

    // Delete about
    $("#about-table").on("click", ".js-delete-about", loadForm);
    $("#modal-about").on("submit", ".js-about-delete-form", saveForm);

});
