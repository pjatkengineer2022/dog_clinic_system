$(document).ready(function(){
    $('#js-select-medicines').dropdown({
    });
    $('#js-select-old-diseases').dropdown({
    });
    $('#js-select-diseases').dropdown({
        allowAdditions: true,
        hideAdditions: false,
    });

    $(".js-new-diseases-row").addClass('--active');

    $('.js-treatment-select').on('change', function() {
        console.log(this.value);
        $(".diagnosis__diseases-row").removeClass('--active');
        if (this.value == '1') {
            $(".js-new-diseases-row").addClass('--active');
        } else {
            $(".js-old-diseases-row").addClass('--active');
        }
    });
});
