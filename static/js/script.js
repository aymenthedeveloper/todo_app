function move(x){
    var drop;
    x.classList.toggle("change")
    drop = document.getElementById("drop");
    if (drop.style.maxHeight){
        drop.style.maxHeight = null; 
    } else{
        drop.style.maxHeight = drop.scrollHeight + "px"; 
    }
}