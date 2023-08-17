document.querySelectorAll('.sale-acc-input__content').forEach(e=>{
   let inputValue =  e.querySelector('.input-value');
   if(!inputValue){
    return
   }
   inputValue.value = e.innerText
   console.log(inputValue.value);
})

document.querySelector('body').addEventListener('click', event=>{
    let node = event.target;

    tabMove(node)
})

function tabMove(el){
    if(!el.classList.contains('tab-btn')){
        return
    }
    event.preventDefault();
    const parrent = el.closest('.tab-container');
    parrent.classList.toggle('--is-active')

}


