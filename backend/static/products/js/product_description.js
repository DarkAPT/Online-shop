function product_description(){
    let active = document.getElementById("description_div");
    if(active.className === 'div_hidden'){
        document.getElementById("product-param_div").className = 'div_hidden';
        active.className = 'div_active';

        let temp = document.getElementById("active");
        document.getElementById("not_active").id = 'active';
        temp.id = "not_active";
    }
}

function product_param(){
    let active = document.getElementById("product-param_div");
    if(active.className === 'div_hidden'){
        document.getElementById("description_div").className = 'div_hidden';
        active.className = 'div_active';

        let temp = document.getElementById("active");
        document.getElementById("not_active").id = 'active';
        temp.id = "not_active";
    }
}