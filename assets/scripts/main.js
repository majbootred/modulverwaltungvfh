$(function () {
    console.log("ready!");
    $('.collapse').on('shown.bs.collapse', function () {
        $(this).parent().find(".collapse-icon .glyphicon").addClass('glyphicon-chevron-up').removeClass('glyphicon-chevron-down');
    });

    $('.collapse').on('hidden.bs.collapse', function () {
        $(this).parent().find(".collapse-icon .glyphicon").addClass('glyphicon-chevron-down').removeClass('glyphicon-chevron-up');
    });

    $("#id_type_of_semester").change(function () {
        let type_of_semester = $(this).val();

        $.ajax({
            url: '/ajax/get_modules',
            data: {
                'type_of_semester': type_of_semester
            },
            success: function (data) {
                $("#id_module").html(data);
            }
        });
    });

    $('#confirmModal').on('show.bs.modal', function (event) {
        let trigger = $(event.relatedTarget);
        let pk = trigger.data('modal');
        let modal = $(this);
        modal.find('#confirmDelete').attr("href", '/assignment-delete/' + pk);
    })
});
