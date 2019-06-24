$(function () {

    // for collapsable panels
    $('.collapse').on('shown.bs.collapse', function () {
        $(this).parent().find(".collapse-icon .glyphicon").addClass('glyphicon-chevron-up').removeClass('glyphicon-chevron-down');
    });

    $('.collapse').on('hidden.bs.collapse', function () {
        $(this).parent().find(".collapse-icon .glyphicon").addClass('glyphicon-chevron-down').removeClass('glyphicon-chevron-up');
    });

    // for conditional rendering of assignable modules
    $("#id_type_of_semester").change(function () {
        let type_of_semester = $(this).val();
        let year = $("#id_year").val();
        $.ajax({
            url: '/ajax/get_modules',
            data: {
                'type_of_semester': type_of_semester,
                'year': year
            },
            success: function (data) {
                $("#id_module").html(data);
            }
        });
    });

    $("#id_year").change(function () {
        let type_of_semester = $("#id_type_of_semester").val();
        if (type_of_semester != "") {
            let year = $(this).val();
            $.ajax({
                url: '/ajax/get_modules',
                data: {
                    'type_of_semester': type_of_semester,
                    'year': year
                },
                success: function (data) {
                    $("#id_module").html(data);
                }
            });
        }

    });

    // for confirmation window when a model shall be deleted
    $('#confirmModal').on('show.bs.modal', function (event) {
        let trigger = $(event.relatedTarget);
        let pk = trigger.data('modal');
        let modal = $(this);
        modal.find('#confirmDelete').attr("href", '/assignment-delete/' + pk);
    })
});
