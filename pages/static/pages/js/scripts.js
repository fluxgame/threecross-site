window.setTimeout(function() {
    $("#announcement").fadeTo(500, 0, function(){
        $(this).remove(); 
    });
}, 60000);

$(function() {
    $(document).ready( function () {
        $('textarea').each(function () {
            this.setAttribute('style', 'height:' + (this.scrollHeight + 8) + 'px;overflow-y:hidden;');
        }).on('input', function () {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight + 8) + 'px';
        });
    });

    $('input[type="tel"]').inputmask("(999) 999-9999");
});
