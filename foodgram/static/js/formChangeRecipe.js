const counterId = document.querySelector('#counter');

const formFieldIngredinet = document.querySelector('.form__field-group-ingredientes');
const nameIngredient = document.querySelector('#nameIngredient');
const formDropdownItems = document.querySelector('.form__dropdown-items');
const cantidadVal = document.querySelector('#cantidadVal');
const cantidad = document.querySelector('#cantidad')
const addIng = document.querySelector('#addIng');
const photoFilename = document.querySelector('#photoFilename');
const photoInput = document.querySelector('#id_file');
const deleteIngredientButtons = document.querySelectorAll('.form__field-item-delete')
const existingIngredients = document.querySelectorAll('.form__field-item-ingredient');

const api = new Api(apiUrl);
const header = new Header(counterId);


function Ingredients() {
    let cur = existingIngredients.length + 1;
    // клик по элементам с сервера
    const dropdown = (e) => {
        if (e.target.classList.contains('form__item-list')) {
            nameIngredient.value = e.target.textContent;
            formDropdownItems.style.display = ''
            cantidadVal.textContent = e.target.getAttribute('data-val');
            console.log(cantidadVal.textContent)
            if (cantidadVal.textContent === "по вкусу")
                cantidad.disabled = true;
            else
                cantidad.disabled = false;
        }
    };
    // Добавление элемента из инпута
    const addIngredient = (e) => {
        if(nameIngredient.value && (cantidad.value || cantidadVal.textContent === "по вкусу")) {
            const data = getValue();
            const elem = document.createElement('div');
            elem.classList.add('form__field-item-ingredient');
            elem.id = `ing${cur}`;
            elem.innerHTML = `<span> ${data.name} ${data.value}${data.units}</span> <span class="form__field-item-delete"></span>
                             <input id="nameIngredient_${cur}" name="nameIngredient_${cur}" type="hidden" value="${data.name}">
                             <input id="valueIngredient_${cur}" name="valueIngredient_${cur}" type="hidden" value="${data.value}">
                             <input id="unitsIngredient_${cur}" name="unitsIngredient_${cur}" type="hidden" value="${data.units}">`;
            cur++;
            elem.addEventListener('click', eventDelete);
            formFieldIngredinet.insertAdjacentElement('afterend',elem);
        }
    };
    // удаление элемента
    const eventDelete = (e) => {
        if(e.target.classList.contains('form__field-item-delete')) {
            const item = e.target.closest('.form__field-item-ingredient');
            item.removeEventListener('click',eventDelete);
            item.remove()
        };
    };
    // получение данных из инпутов для добавления
    const getValue = (e) => {
        const data = {
            name: nameIngredient.value,
            value: cantidad.value,
            units: cantidadVal.textContent
        };
        clearValue(nameIngredient);
        clearValue(cantidad);
        return data;
    };
    // очистка инпута
    const clearValue = (input) => {
        input.value = '';
    };
    return {
        clearValue,
        getValue,
        addIngredient,
        dropdown,
        eventDelete
    }
}

const cbEventInput = (elem) => {
    return api.getIngredients(elem.target.value).then( e => {
        if(e.length !== 0 ) {
            const items = e.map( elem => {
                return `<a class="form__item-list" data-val="${elem.dimension}"">${elem.title}</a>`
            }).join(' ')
            formDropdownItems.style.display = 'flex';
            formDropdownItems.innerHTML = items;
        }
    })
    .catch( e => {
        console.log(e)
    })
};

const cutPhotoFilename = () => {
    photoFilename.textContent = photoFilename.textContent.replace(/^.*[\\\/]/, '');
}
photoInput.addEventListener('change', () => {
    photoFilename.textContent = photoInput.value;
    cutPhotoFilename();
});
cutPhotoFilename();

const eventInput = debouncing(cbEventInput, 1000);

// вешаем апи
nameIngredient.addEventListener('input', eventInput);
const ingredients = Ingredients();
// вешаем слушатель на элементы с апи
formDropdownItems.addEventListener('click', ingredients.dropdown);
// вешаем слушатель на кнопку
addIng.addEventListener('click', ingredients.addIngredient);

deleteIngredientButtons.forEach(button => button.addEventListener('click', ingredients.eventDelete))

