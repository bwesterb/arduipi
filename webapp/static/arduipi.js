function main() {
    // Set-up CSRF protection.
    var csrftoken = $('meta[name=csrf-token]').attr('content');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)
                    && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })
}

$(function() {
    main();
});
