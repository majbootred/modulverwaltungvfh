
$(function() {
    console.log( "ready!" );
    $('.collapse').on('shown.bs.collapse', function() {
   $(this).parent().find(".collapse-icon .glyphicon").addClass('glyphicon-chevron-up').removeClass('glyphicon-chevron-down');
  });

$('.collapse').on('hidden.bs.collapse', function() {
   $(this).parent().find(".collapse-icon .glyphicon").addClass('glyphicon-chevron-down').removeClass('glyphicon-chevron-up');
  });
});
