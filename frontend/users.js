const domain = 'http://localhost:8000/api/v1/';
const userForm = document.querySelector('#userForm')
const userLogin = document.querySelector('#userlogin')
const userPassword = document.querySelector('#password')
const resultText = document.querySelector('#result')

userForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const result = await fetch(`${domain}/users/`, {
        method: 'POST',
        body: JSON.stringify({ userlogin: userLogin.value, password: userPassword.value }),
        headers: { "Content-Type": "application/json" }
    })

    const data = await result.json()

    if (result.ok){
        resultText.textContent = `Пользователь ${data.userlogin} успешно создан`
        userForm.reset()
    } else {
        resultText.textContent = JSON.stringify(data)
        console.log(data)
    }
})