let select = document.getElementById("select");
let list = document.getElementById("list");
let selectText = document.getElementById("selectText");
let options = document.getElementsByClassName("options");

select.onclick = function(){
    list.classList.toggle("open");
}

for(option of options){
    option.onclick = function(){
        selectText.innerHTML = this.innerHTML;
    }
}

document.addEventListener("click", function(event) {
    const isClickInside = select.contains(event.target) || list.contains(event.target);
    if (!isClickInside) {
        list.classList.remove("open");
    }
});