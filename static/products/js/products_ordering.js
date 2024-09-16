$(document).ready(function() {
    $('.btn-action').click(function() {
        var action = $(this).data('action'); // Получаем значение атрибута data-action
        var currentUrl = window.location.href;

        var searchParams = new URLSearchParams(currentUrl);
        let filter_object = {
            'category_slug': searchParams.get('category_slug'),
            'filter': searchParams.getAll('filter').map(Number),
            'action': action
        };
        $.ajax({
            type: 'GET',
            url: '/filter-products', // Укажите здесь URL вашего Django view
            data: filter_object,// Передаем параметр action в запросе
            dataType: 'json',
            success: function(response) {
                console.log(currentUrl);
                $("#filtered-product").html(response.data)
            },
        });
    });
});