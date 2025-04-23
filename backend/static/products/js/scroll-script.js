window.onload = function() {
    slideMin();
    slideMax();
}

const minVal = document.querySelector(".range-min");
const maxVal = document.querySelector(".range-max");
const priceInputMin = document.querySelector(".input-min");
const priceInputMax = document.querySelector(".input-max");
const progress = document.querySelector(".price-slider .progress");
const minGap = 0;
const sliderMinValue = parseInt(minVal.min);
const sliderMaxValue = parseInt(maxVal.max);


function slideMin(){
    let gap = parseInt(maxVal.value) - parseInt(minVal.value);
    if (gap <= minGap){
        minVal.value = parseInt(maxVal.value) - minGap;
    }
    priceInputMin.value = minVal.value;
    setArea();
}

function slideMax(){
    let gap = parseInt(maxVal.value) - parseInt(minVal.value);
    if (gap <= minGap){
        maxVal.value = parseInt(minVal.value) + minGap;
    }
    priceInputMax.value = maxVal.value;
    setArea();
}

function setArea(){
    progress.style.left = (minVal.value / sliderMaxValue) * 100 + "%";
    progress.style.right = 100 - (maxVal.value / sliderMaxValue) * 100 + "%";

}

function setMinInput(){
    let minPrice = parseInt(priceInputMin.value);
    if(minPrice < sliderMinValue){
        priceInputMin.value = sliderMinValue;
    }
    minVal.value = priceInputMin.value;
    slideMin();
}

function setMaxInput(){
    let maxPrice = parseInt(priceInputMax.value);
    if(maxPrice > sliderMaxValue){
        priceInputMax.value = sliderMaxValue;
    }
    maxVal.value = priceInputMax.value;
    document.querySelector(".input-max").value = "1000"
    slideMax();
}