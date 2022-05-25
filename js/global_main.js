$(document).ready(function(){
    topNavigation();

    // $('.js-add-visit-hours-input').datepicker({
    //     multidate: true,
    //     format: 'dd-mm-yyyy'
    // });

    $('.datepicker').datepicker({
        format: 'mm/dd/yyyy',
        startDate: '-1d',
        multidate: true,
    });
      
});
  