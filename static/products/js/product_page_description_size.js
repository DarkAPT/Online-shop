let descr_height = document.getElementById("description_div").offsetHeight;
document.getElementById("product-param_div").className = 'div_active';
let param_height = document.getElementById("product-param_div").offsetHeight;
let buttons_height = document.getElementById("descr_buttons").offsetHeight;
document.getElementById("product-param_div").className = 'div_hidden';
if(  param_height > descr_height){
    document.getElementById('description').style.minHeight = param_height + buttons_height + 50 + "px";
}
else{
    document.getElementById('description').style.minHeight = descr_height + buttons_height + 50 + "px";
}