const domain = 'http://localhost:8000/api/v1/';

const list = document.querySelector('#list');
const itemId = document.querySelector('#list');
const itemName = document.querySelector('#name');

async function loadItem(e){
    e.preventDefault();
    const result = await fetch(e.target.href);
    if (result.ok){
        const data = await result.json();
        itemId.value = data.id;
        itemName.value = data.name;
    } else {
        console.log(result.statusText);
    }
}

async function loadList(){
    const result = await fetch(`${domain}rubrics`)
    if (result.ok){
        const data = await result.json();
        let s = '', d;
        for (let i = 0; i < data.length; i++){
            d = data[i]
            s += `<li>${d.name} 
                        <a href="${domain}rubrics/${d.id}/" class="detail">Вывести</a>
                    </li>`;
        }
        list.innerHTML = s;

        let links = list.querySelectorAll('ul li a.detail')
        links.forEach((link) => {
            link.addEventListener('click', loadItem);
        });

    } else {
        // window.alert(result.statusText);
        console.log(result.statusText)
    }
}

loadList();

// const domain = 'http://localhost:8000/api/v1/';
// const list = document.querySelector('#list');

// async function loadList() {
//     try {
//         const result = await fetch(`${domain}rubrics/`);

//         if (result.ok) {
//             const data = await result.json();
//             let s = '';

//             for (let i = 0; i < data.length; i++) {
//                 const d = data[i];
//                 s += `<li>${d.name}</li>`;
//             }

//             list.innerHTML = s;
//         } else {
//             console.log(result.status, result.statusText);
//         }
//     } catch (error) {
//         console.log('Ошибка запроса:', error);
//     }
// }
