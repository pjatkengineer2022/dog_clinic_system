$(document).ready(function(){
    topNavigation();
    globalMethods();

    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        startDate: '0d',
        multidate: true,
        weekStart: 1,
        locale: 'pl',
        language:'pl'
    });     
});
  