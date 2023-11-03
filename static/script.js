/* funcion para la satisfaccion y recomendacion */

function highlightNumber(element, group) {
    let numbers, inputElement;
    
    if (group === 1) {
        numbers = document.querySelectorAll('.numbers2 span');
        inputElement = document.getElementById('satisfaccion');
    } else if (group === 2) {
        numbers = document.querySelectorAll('.numbers span');
        inputElement = document.getElementById('recomendacion');
    } else {
        return; 
    }
    
    numbers.forEach(num => num.classList.remove('active'));

    element.classList.add('active');

    if(inputElement) {
        inputElement.value = element.getAttribute('data-value');
    }
}

/* funcion para abrir cada casilla de preguntas frecuentes */

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.faq-question').forEach(function(question) {
        question.addEventListener('click', function() {
            question.classList.toggle('active');
            let answer = question.nextElementSibling;
            answer.style.maxHeight = question.classList.contains('active') ? answer.scrollHeight + 'px' : '0';
        });
    });
});


/* funcion para leer cada casilla del formulario y que esten todos llenos */


document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');

    form.addEventListener('submit', function (e) {
        const edad = document.getElementById('edad').value;
        const genero = document.getElementById('genero').value;
        const cesfam = document.getElementById('cesfam').value;
        const frecuencia = document.getElementById('frecuencia').value;
        const satisfaccion = document.getElementById('satisfaccion').value;
        const recomendacion = document.getElementById('recomendacion').value;
        const razon = document.getElementById('razon').value;
        
        if (!edad || !genero || !cesfam || !frecuencia || !satisfaccion || !recomendacion || !razon) {
            e.preventDefault();  // Stop form from submitting
            alert('¡Todos los campos deben ser rellenados!');  // Show error message
            return;
        }
        
        if (razon.length < 25) {
            e.preventDefault();  // Stop form from submitting
            alert('¡Debe ingresar al menos 25 caracteres en el campo de razón!');  // Show error message
        }
    });
});

/* funcion para los caracteres restantes del campo abierto */

function updateCharCount() {
    const textarea = document.getElementById('razon');
    const charCountDiv = document.getElementById('charCount');
    const maxLength = 512;
    const currentLength = textarea.value.length;
    const remainingChars = maxLength - currentLength;
    
    charCountDiv.textContent = `${remainingChars} caracteres restantes`;
}

