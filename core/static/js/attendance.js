var AttendanceListPage = {
    init: function () {
        this.$container = $('.attendances-container');
        this.render();
        this.bindEvents();
    },

    render: function () {

    },

    bindEvents: function () {
        $('.btn-present', this.$container).on('click', function (e) {
            e.preventDefault();

            var self = $(this);
            var url = $(this).attr('href');
            $.getJSON(url, function (result) {
                if (result.success) {
                    $('.glyphicon-record', self).toggleClass('active');
                }
            });

            return false;
        });

        $('.btn-late', this.$container).on('click', function (e) {
            e.preventDefault();

            var self = $(this);
            var url = $(this).attr('href');
            $.getJSON(url, function (result) {
                if (result.success) {
                    $('.glyphicon-record', self).toggleClass('active');
                }
            });

            return false;
        });

        $('.btn-absent', this.$container).on('click', function (e) {
            e.preventDefault();

            var self = $(this);
            var url = $(this).attr('href');
            $.getJSON(url, function (result) {
                if (result.success) {
                    $('.glyphicon-record', self).toggleClass('active');
                }
            });

            return false;
        });
    }
};


$(document).ready(function () {
    AttendanceListPage.init();
});
