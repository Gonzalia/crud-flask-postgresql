const userForm = document.querySelector('#userForm')

let users = []
let editing = false
let userId = null

window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch('/api/users', {
        method: 'GET'
    })
    const user_list = await response.json()
    users = user_list
    renderUser(users)

})

userForm.addEventListener('submit', async e => {
    e.preventDefault()

    const username = userForm['username'].value // name atributte
    const password = userForm['password'].value
    const email = userForm['email'].value


    if (!editing) {

        const response = await fetch('/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
                email: email,
            }),
        });

        const data = await response.json()
        users.unshift(data)

    } else {
        const response = await fetch(`/api/users/${userId}`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                password,
                email
            }),
        })

        const user_data = await response.json()
        users = users.map(user => user.id == user_data.id ? user_data : user)
        editing = false
        userId = null

    }

    renderUser(users.reverse()) // Stack 

    userForm.reset()
})

function renderUser(users) {
    const user_list = document.querySelector('#userList')
    user_list.innerHTML = ''

    users.reverse().forEach(user => {
        const userItem = document.createElement('li')
        userItem.innerHTML = `
            
                <h3 class="card-title">${user.username}</h3>
            <header class = "user_item"> 
                <button class="btn-delete">Delete</button>
                <button class="btn-edit">Edit</button>
            </header>
            <p class = "email">${user.email}</p>
            
        `

        const btnDelete = userItem.querySelector('.btn-delete')
        btnDelete.addEventListener('click', async () => {
            const response = await fetch(`/api/users/${user.id}`, {
                method: "DELETE"
            })
            const user_deleted = await response.json()


            users = users.filter(user => user.id != user_deleted.id)
            renderUser(users.reverse())
        })

        const btnEdit = userItem.querySelector('.btn-edit')
        btnEdit.addEventListener('click', async () => {
            const response = await fetch(`/api/users/${user.id}`)
            const user_data = await response.json()

            userForm["username"].value = user_data.username
            userForm["email"].value = user_data.email

            editing = true
            userId = user_data.id
        })

        user_list.append(userItem)
    });

}
