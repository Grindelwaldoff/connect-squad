
// const form = document.getElementById('acc-filter-form');

// form.addEventListener('submit', event=>{
//     event.preventDefault()
// });


inputDelSymbols()
function inputDelSymbols(){
    let inputs = document.querySelectorAll('input[type="number"]');
    let invalidChars = [
                        "-",
                        "+",
                        "e",
                        ];

    inputs.forEach( e=>{
        e.addEventListener('keydown', el =>{
            e.addEventListener("input", function() {
                this.value = this.value.replace(/[e\+\-]/gi, "");
            });
            if(invalidChars.includes(el.key)){
                el.preventDefault()
            }
        
        })
    })

}


const body  = document.querySelector('body');

window.addEventListener('click', function(event){
    let nodeEl = event.target;
    let popupClass = closestAttr(nodeEl, 'data-popup')
    let popupClassClose = closestAttr(nodeEl, 'data-close')
    
    tabsMove(nodeEl)
    dropdownListMove(nodeEl)
    popupMove(nodeEl,popupClass)
    popupClose(nodeEl, popupClassClose)
    openSelect(nodeEl)
    selectChooseItem(nodeEl)
    delitedAreaItem(nodeEl)
    changeValue(nodeEl)
    passMowe(nodeEl)
    copyContentArea(nodeEl)
})

function popupClose(item, className){
    if(item.classList.contains('popup-wrapper')){
        item.classList.remove('--is-active')
        body.classList.remove('--no-skroll')
        bodyToHidden()
    }
    if(className === null){
        return
    }
    let popup = document.querySelector(`.${className}`)
    if(popup){
        popup.classList.remove('--is-active')
        body.classList.remove('--no-skroll')
        bodyToHidden()
    }
    
}



function popupMove(item,className){
    if(className === null){
        return
    }
    let popup = document.querySelector(`.${className}`)
    if(popup){
        popup.classList.add('--is-active')
        bodyToHidden()
        if(popup.classList.contains('--is-active')){
            popupBuyMowe(item,popup)
        }
        
    }
    
}
function popupBuyMowe(item, popup){
    if(popup.classList.contains('popup-buy')){
        let itemParentNode = item.closest('.goods-list-item')
        
        const parentNodeData = {
            quantity:itemParentNode.querySelector('.goods-list-item__quantity-num').innerText,
            price: itemParentNode.querySelector('.goods-list-item__price-num').innerText,
            text: itemParentNode.querySelector('.goods-list-item__column-text').innerText,
        }
        popup.querySelector('.popup-buy__content-text').innerText = parentNodeData.text;
        popup.querySelector('.popup-buy-price-num-default').value = parentNodeData.price;
        popup.querySelector('.counter-max-num-wrapper').innerText = parentNodeData.quantity;
        popup.querySelector('.items__current').value = 1;
        // popup.querySelector('.popup-buy-tag__container').innerHTML =;
        changeValue(item)
        
    }else{
        return
    }
    

}

function bodyToHidden(){
    document.querySelectorAll('.popup-wrapper').forEach(e=>{
        if(e.classList.contains('--is-active')){
            body.classList.add('--no-skroll')
        }
    })
}


function closestAttr(el, attr){
    let node = el;
    while (node) {
        let attrValue = node.getAttribute(attr);
        if(attrValue){
            return attrValue
        }
        
        node = node.parentElement;
    }
    return null
}
keyMowe()
function keyMowe(){
    let counterArea = document.querySelector('.items__current');
    if(!counterArea){
        return
    }
    let counterMaxValue = document.querySelector('.counter-max-num-wrapper');
    if(Number(counterArea.value)>=Number(counterMaxValue.innerText)){
        counterArea.addEventListener('input', e=>{
            let counterAreaValue = e.target.value
            if(Number(counterAreaValue)>=Number(counterMaxValue.innerText)){
                e.target.value = counterMaxValue.innerText
            }
            if(Number(counterAreaValue)===0 && counterAreaValue !== ''){
                e.target.value = 1
            }
        })
    }
}

function changeValue(item){
    let counterBtn = item.getAttribute('data-action');
    if(!counterBtn){
        return
    }
    event.preventDefault()

    let counterParent = item.closest('.buy-popup__form-inner');
    let counterWrapper = counterParent.querySelector('.items__current');
    let counterValue = Number(counterWrapper.value)
    let maxValue = Number(counterParent.querySelector('.counter-max-num-wrapper').innerText);

    if(counterBtn === 'plus'){
        counterWrapper.value = counterValue + 1
        if(counterValue >= maxValue){
            counterWrapper.value = maxValue
        }
    }
    if(counterBtn === 'minus'){
        counterWrapper.value = counterValue - 1
        if(counterValue > maxValue){
            counterWrapper.value = maxValue
        }
        if(counterValue <= 1){
            counterWrapper.value = 1
        }
    }
}












function dropdownListMove(item){
    if(!item.classList.contains('dropdown-item-button')){
        document.querySelectorAll('.dropdown-all').forEach(e=>{
            e.classList.remove('--is-active')
        })
        return
    }
    event.preventDefault()
    document.querySelectorAll('.dropdown-all').forEach(e=>{
        e.classList.remove('--is-active')
    })
    if(item.closest('.dropdown')){
        item.closest('.dropdown').classList.toggle('--is-active')
    }
    
    errorDropdown(item)
}

function errorDropdown(el){
    if(!el.closest('.dropdown-error')){
        return
    }
    const errorList = document.querySelector('.error-header__dropdown-inner')
    if(errorList.children.length === 0){
        return
    }
    el.closest('.dropdown-error').classList.toggle('--is-active')
    
    
}



function openSelect(item){
    document.querySelectorAll('.all-select-container').forEach(e=>{
        e.classList.remove('--is-active')
    })
    if(!item.classList.contains('select-all-area') && !item.classList.contains('select-all-item__value') && !item.classList.contains('select-all-item')){
        return
    }
    event.preventDefault()
     let area = item
        area.closest('.all-select-container').classList.toggle('--is-active')
        if(area.closest('.all-select-container').querySelector('.select-no-multiple-choice')){
            area.closest('.all-select-container').querySelector('.select-no-multiple-choice').classList.toggle('--is-active')
        }
        
}








function selectChooseItem(item){   
    if(!item.classList.contains('select-all-list__item')){
        return
    }
    event.preventDefault() 
    let itemText = item.innerText
    let itemId = item.dataset.id
    const selectValue = item.getAttribute('data-item-value')
    let area = item.closest('.all-select-container').querySelector('.select-all-area');
    let areaDellItem = item.closest('.all-select-container').querySelector('.--dropdown-close')
    let selectItems = item.closest('.all-select-container').querySelectorAll('.select-all-list__item')
        if(item.classList.contains('--dropdown-close')){
            area.innerHTML = item.getAttribute('data-name');
            selectItems.forEach(e=>{
                e.classList.remove('select-kist__item-events-none')
            })
        }else{
            if(!item.closest('.all-select-container').querySelector('.select-no-multiple-choice')){
                if(area.innerText == areaDellItem.getAttribute('data-name')){
                    console.log(2)
                    area.innerHTML = '';
                }
            }
            const selectItemName = item.getAttribute('data-item-name')
            
            area.innerHTML += criationTemplateItem(itemText, selectValue, itemId, selectItemName)
        }
    
    item.closest('.all-select-container').classList.remove('--is-active')
    if(!item.closest('.all-select-container').querySelector('.select-no-multiple-choice')){
        if(item.classList.contains('--dropdown-close')){
            return
        }
        item.classList.add('select-kist__item-events-none')
    }
    if(item.closest('.all-select-container').querySelector('.select-no-multiple-choice')){
        const targetSelectItem = item.closest('.all-select-container').querySelector('.select-no-multiple-choice')
        const targetSelectItemName = item.getAttribute('data-name')
        
        targetSelectItem.innerHTML = `<input type="text" data-id="${itemId}" name="${targetSelectItemName}" class="input-hidden" form="acc-filter-form" value="${selectValue}"><p class="select-all-item">${itemText}</p>`
        if(item.getAttribute('data-id') === '1' && !item.classList.contains('--add-name')){
            targetSelectItem.querySelector('.input-hidden').name = '';
        }
    }
}







function delitedAreaItem(item){    
    if(!item.classList.contains('select-all-item__close')){
        return
    }
    event.preventDefault()
    let closeParent = item.closest('.select-all-item');
    
    let itemId = closeParent.dataset.id;
    let listNode = closeParent.closest('.all-select-container').querySelectorAll('.select-all-list__item');
    listNode.forEach(e=>{
        if(e.dataset.id === itemId){
            e.classList.remove('select-kist__item-events-none')
        }
    })
    
    let area = item.closest('.select-all-area')
    
    item.closest('.select-all-item').remove()
    if(area.innerText === ''){
        area.innerHTML =  `${area.closest('.all-select-container').querySelector('.--dropdown-close').getAttribute('data-name')}`
    }
}






function criationTemplateItem(text,value,id, name){

    return `<label class="select-all-item" data-id="${id}">
                <input type="text" form="acc-filter-form" value="${value}" name="${name}" class="select-all-item__input input-hidden">
                <p class="select-all-item__value">${text}</p>
                 <div class="select-all-item__close"></div>
            </label>
            `
}



selectsAddId()
function selectsAddId(){
    document.querySelectorAll('.select-all-list').forEach(e=>{
        let listIteme = e.querySelectorAll('.select-all-list__item');
        let itemId = 1;
        for(let i = 0; i < listIteme.length; i++){
            listIteme[i].dataset.id = itemId++
        }
    })
    
}





creationAccsList()
function creationAccsList(){
    const tabsBtns = document.querySelectorAll('.list-button__btn');
    if(!tabsBtns){
        return
    }
    let tabsListItem = document.querySelectorAll('.list-content');
    tabsListItem.forEach((e,id)=>{
        e.dataset.content = id
    }) 
    for(let i = 0; i < tabsBtns.length; i++){
        tabsBtns[i].dataset.id = i;
    }
    
}

function tabsMove(item){
    if(!item.classList.contains('list-button__btn')){
        return
    }
    event.preventDefault()
    item.closest('.list-button').classList.remove('--is-active')
    let tabButtons = document.querySelectorAll('.list-button__btn')
    let cl = 0;
    tabButtons.forEach(e=>{
        e.setAttribute('data-id', `${cl++}`)
    })
    tabButtons.forEach(e=>{
        e.classList.remove('--is-active')
    })
    let tabsContent = document.querySelectorAll('.list-content');
   
    tabsContent.forEach(e=>{
        e.classList.remove('--is-active')
    })
    let tabContent = document.querySelector(`[data-content="${item.dataset.id}"`);
    let tabContentList = tabContent.children
    if(!tabContent || tabContentList.length === 0){
        return
    }
    tabContent.classList.add('--is-active')
    item.classList.add('--is-active')
    item.closest('.list-button').classList.add('--is-active')

}



addIdCheck()
function addIdCheck(){
    let input = document.querySelectorAll('.list-content__item-check-input');
    let label = document.querySelectorAll('.list-content__item-check-label');
    if(!input&&!label){
        return
    }
    input.forEach((e, index)=>{
        e.setAttribute("id", `acc-check-${index}`)
    })
    label.forEach((e,index)=>{
        e.setAttribute("for", `acc-check-${index}`)
    })
    
}


function passMowe(item){
    let passHiddenBtn = document.querySelector('.hidden-btn-value');
    
    if(!passHiddenBtn || !item.classList.contains('hidden-btn-value')){
        return
    }
    
    
    event.preventDefault()
    let passHiddenBtnPar = item.closest('.container-hidden-value');
    let pasInput = passHiddenBtnPar.querySelector('.input-hidden-value');
    if(pasInput.value == ''){
        return
    }
    item.classList.toggle('--is-active')
    if(item.classList.contains('--is-active')){
        pasInput.setAttribute('type', 'text')
    }else{
        pasInput.setAttribute('type', 'password')
    }
}
    

function copyContentArea(item){
    if(!item.classList.contains('copy-btn')){
        return
    }
    let copyParent = item.closest('.copy-parent');
    if(!copyParent){
        return
    }
    let copyArea = copyParent.querySelector('.copy-area');
    copyArea.select()
    document.execCommand("copy")   
}







if(document.querySelector('.page-marcet__header')){
    let headerMenu = document.querySelector('.page-marcet__menu')
    let popupMenu = document.querySelector('.menu-popup__nav');

    let hederbottomItem = document.querySelector('.page-marcet__header-bottom-inner')

    let docWidth = document.documentElement.clientWidth;
    window.addEventListener('resize', function(){
        docWidth = document.documentElement.clientWidth;
        hiddenHeaderMenu(headerMenu,popupMenu,docWidth)
        wiewHeaderMenu(headerMenu,popupMenu,docWidth)

        hiddenElementBottomMenu(hederbottomItem, popupMenu, docWidth)
        wiewElementBottomMenu(hederbottomItem, popupMenu, docWidth)
    })

        hiddenHeaderMenu(headerMenu,popupMenu,docWidth)
        wiewHeaderMenu(headerMenu,popupMenu,docWidth)


        hiddenElementBottomMenu(hederbottomItem, popupMenu, docWidth)
        wiewElementBottomMenu(hederbottomItem, popupMenu, docWidth)


    function hiddenHeaderMenu(start, end, width){
        if(width <= 860){
            if(start.innerHTML){
                end.innerHTML = start.innerHTML
                document.querySelector('.page-marcet__header-top').style.display = 'none'
                start.innerHTML = ''
            }
        
        }
    }

    function dicoratinMainChange(){
        let dicoratiItem = document.querySelector('header__decoration-img')
    }

    function wiewHeaderMenu(start, end, width){
        if(width > 860){
            document.querySelector('.menu-popup').classList.remove('--is-active')
            if(end.innerHTML){
                start.innerHTML = end.innerHTML
                document.querySelector('.page-marcet__header-top').style.display = 'block'
                end.innerHTML = ''
            }
        }
    }
    function hiddenElementBottomMenu(start, end, width){
        if(width <= 640){
            if(start.innerHTML){
                let endTemplate = document.createElement('div');
                endTemplate.className = 'page-marcet__header-popup-inner'
                end.prepend(endTemplate)
                endTemplate.innerHTML = start.innerHTML
                start.innerHTML = ''
            }
        
        }
    }

    function wiewElementBottomMenu(start, end, width){
        if(width > 640){
            let endInner = end.querySelector('.page-marcet__header-popup-inner')
            if(endInner){ 
                start.innerHTML = endInner.innerHTML
                endInner.remove()
            }
        }
    }
 
}


    let url = document.location.href;
    // document.location.href
    
    let getResponse = async(url)=>{

        const response = await fetch(url);
        if(!response.ok){
            throw new Error(errorMowe(url, response.status))
            
        }

    }

getResponse(url)



function errorMowe(u, s){
    let errorContainer = document.querySelector('.error-container')
    if(!s){
        return
    }

    const errorTemplate =  `<div class="error-label">
                                <div class="error-title">${s}</div>
                                <p class="error-subtitle">Ошибка!</p>
                                <p class="error-text">${u}</p>
                            </div>`;
    
    const errorWrapper =  document.querySelector('.error-wrapper');
    const notification = document.querySelector('.--notification');
    const errordropdownInner = document.querySelector('.error-header__dropdown-inner');
    setTimeout(function(){
        errorWrapper.innerHTML += errorTemplate;
        if(errorWrapper.children){
            errorContainer.classList.add('--is-active')
        }
    }, 1000)
    setTimeout(function(){

        if(errorWrapper.children){
            errorContainer.classList.remove('--is-active')
            errordropdownInner.innerHTML  += errorWrapper.innerHTML;
            notification.classList.add('--is-active')
            errorWrapper.innerHTML =''
        }
    }, 4000)
    
}



