$(document).ready(function(){
    $(document).on("click", ".add-to-cart", function (e) {
        e.preventDefault();

        var productsInCartCount = $("#products-in-cart-count");
        var cartCount = parseInt(productsInCartCount.text() || 0);

        var product_id = $(this).data("product-id");

        var add_to_cart_url = $(this).attr("href");
        const csrftoken = $('meta[name="csrf-token"]').attr('content');

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: csrftoken,
            },
            success: function (data) {
                // Увеличиваем количество товаров в корзине (отрисовка в шаблоне)
                cartCount++;
                productsInCartCount.text(cartCount);
            },

            error: function (xhr, status, error) {
                console.error("Ошибка при добавлении товара:", error); // Для отладки
            }
        });

    })
    
    // Ловим собыитие клика по кнопке удалить товар из корзины
    $(document).on("click", ".remove-from-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();
        
        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var goodsInCartCount = $("#products-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);
        
        // Получаем id корзины из атрибута data-cart-id
        var cart_id = $(this).data("cart-id");
        // Из атрибута href берем ссылку на контроллер django
        var remove_from_cart = $(this).attr("href");
        
        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            
            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                
                // Уменьшаем количество товаров в корзине (отрисовка)
                cartCount -= data.quantity_deleted;
                goodsInCartCount.text(cartCount);
                
                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.carts_items_html);
                
            },
            
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });
    
})