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


    // Обработчик события для уменьшения значения
    $(document).on("click", ".decrement", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством 
        var cartItem = $(this).closest('.prod_quant');
        var $input = cartItem.find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());

        // Если количества больше одного, то только тогда делаем -1
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            // Запускаем функцию определенную ниже
            // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    // Обработчик события для увеличения значения
    $(document).on("click", ".increment", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством 
        var cartItem = $(this).closest('.prod_quant');
        var $input = cartItem.find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        // Запускаем функцию определенную ниже
        // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
        updateCart(cartID, currentValue + 1, 1, url);
    });

    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {

                // Изменяем количество товаров в корзине
                var goodsInCartCount = $("#products-in-cart-count");
                var cartCount = parseInt(goodsInCartCount.text() || 0);
                cartCount += change;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины
                var cartItemsContainer = $("#cart_order");
                cartItemsContainer.html(data.carts_items_html);

            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    }

    
})