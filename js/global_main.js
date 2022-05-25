$(document).ready(function(){
    topNavigation();

    // $('.js-add-visit-hours-input').datepicker({
    //     multidate: true,
    //     format: 'dd-mm-yyyy'
    // });

    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        startDate: '-1d',
        multidate: true,
    });
      
});
  