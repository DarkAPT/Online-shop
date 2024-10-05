$(document).ready(function(){
    var currentUrl = window.location.href.split('/');
    let query = window.location.href.split('?');
    if (query.length >= 2) {
        category_slug = currentUrl.pop() && currentUrl.pop();
    } else {
        category_slug = currentUrl.pop() || currentUrl.pop();
    }    
    if (query.length > 1 && query[1].split("=")[0] === "q") {
        query = decodeURIComponent(query[1].split("=")[1]); // Декодируем строку
    }

    let filter_object = {
        'category_slug': category_slug,  // Добавляем category_slug в объект фильтра
        'page': 1,
        'q': query
    };
    $('.page_button').click(function() {
        let current_page = $(this).data("page");
        filter_object.page = current_page;
    })
    $('.btn-action').click(function() {
        let action = $(this).data('action');
        filter_object.order_by = action;
        filter_object.page = 1
    })
    $('.price_button').click(function() {
        let max_price = document.querySelector(".input-max").value;
        let min_price = document.querySelector(".input-min").value;
        filter_object.min_price = min_price;
        filter_object.max_price = max_price;
        filter_object.page = 1
    })
    $('.next_page').click(function() {
        filter_object.page = filter_object.page+1
    })
    $(".filter-checkbox, .first_page").click(function(){
        filter_object.page = 1
    })
    $(".filter-checkbox, .btn-action, .price_button, .page_button, .first_page, .next_page").on("click", function(){
        $(".filter-checkbox").each(function(){
            let filter_key = $(this).data("filter")

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element) {
                return element.value
            })
        })
        $.ajax({
            url: '/filter-products',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
            },
            success: function (response) {
                $("#product_page").html(response.data)
            }
        })
    })
})

