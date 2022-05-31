$(document).ready(function(){
    topNavigation();
    globalMethods();

    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        startDate: '-1d',
        multidate: true,
    });    
});
  