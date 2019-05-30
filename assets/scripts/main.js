
$(function() {
    console.log( "ready!" );
    $('#modules').on('shown.bs.collapse', function() {
    $(this).find(".collapse-icon .glyphicon").addClass('glyphicon-chevron-up').removeClass('glyphicon-chevron-down');
  });

$('#modules').on('hidden.bs.collapse', function() {
    $(this).find(".collapse-icon .glyphicon").addClass('glyphicon-chevron-down').removeClass('glyphicon-chevron-up');
  });
});
