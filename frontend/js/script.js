
var userLoggedIn = false; 

function updateUserUI(){
    if (userLoggedIn) {
        const storedUsername = localStorage.getItem('username');
        console.log(`${storedUsername} Logged in`)
        console.log(localStorage.getItem('user_id'))
        // document.getElementById('settingsUsername').innerHTML=storedUsername
        
    } else {
        console.log('User Logged out')
        // window.location = "sign-in.html";
    }
}

function updateUserUI2(){
    window.location = 'index.html';
    updateUserUI();
}

function postLogin(){
    window.location = 'index.html';
    updateUserUI();
}

function callLoginPage(){
    window.location = 'sign-in.html';
    updateUserUI();
}

document.addEventListener("DOMContentLoaded", function () {
    const storedToken = localStorage.getItem('access_token');
    if (storedToken) {
        userLoggedIn = true;
    }
    // Call the function to update UI
    updateUserUI();

    document.getElementById('loginButton').addEventListener('click', async (event) => {
        event.preventDefault(); 
        const email = document.getElementById('inputEmail').value;
        const password = document.getElementById('inputPassword').value;
        try {
            const response = await fetch(`http://127.0.0.1:8001/api/v1/auth/login?email=${email}&password=${password}`, {
                method: 'POST',
            });
            if (response.ok) {
                const { access_token, user_id, username, email, message } = await response.json();
                if (access_token){
                    userLoggedIn = true;
                    localStorage.setItem('access_token', access_token);
                    localStorage.setItem('user_id', user_id);
                    localStorage.setItem('username', username);
                    localStorage.setItem('email', email);
                    console.log(message)
                    window.location = 'index.html';
                    // alert("Logged In")

                }else{
                    console.warn(message)
                    console.error('Login failed');
                }
            } else {
                    console.error('Login failed');
            }
        } catch (error) {
            console.error('Error during login:', error);
            console.log('adhiadibhuabcbakdbkjabdkjabkdhbahbdkajbsdkjabshdbkajbfkhdbkx')
        }
    });
});





document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('logout').addEventListener('click', async (event) => {
        event.preventDefault(); 
        try {
            const storedToken = localStorage.getItem('access_token');
            const response = await fetch(`http://127.0.0.1:8001/api/v1/auth/logout/${storedToken}`, {
                method: 'POST',
            });
            if (response.ok) {
                userLoggedIn = false
                updateUserUI()
                localStorage.clear();
                console.log('Logged out successfully');
                window.location = "sign-in.html";
            } else {
                console.error('Logout failed');
                
            }
        } catch (error) {
            console.error('Error during logout:', error);
        }
    });
});





document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('signUpButton').addEventListener('click', async (event) => {
        event.preventDefault();
        const inputEmail = document.getElementById('inputEmail').value;
        const inputUsername = document.getElementById('inputUsername').value;
        const inputPassword = document.getElementById('inputPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        // Check if the password and confirmPassword match
        if (inputPassword === confirmPassword) {
            // Construct the URL with path parameters
            const url = `http://127.0.0.1:8001/api/v1/auth/register-via-email/?password=${inputPassword}&passwordConfirm=${confirmPassword}`
            // Call the endpoint to create a user object
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'accept': '*'
                },
                body: new URLSearchParams({
                    email: inputEmail,
                    username: inputUsername,
                }).toString(),
            })

            if (response.ok) {
                const { message } = await response.json();
                console.log('User registered successfully!');
                callLoginPage();
                console.log(message)
            } else {
                document.getElementById('passwordMismatchError').innerHTML="Registration unsuccessful"
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            // location.reload();
        } else {
            // Handle non matching passwords (optional)
            console.error('Passwords do not match.');
            document.getElementById('passwordMismatchError').innerHTML="Passwords do not match"
        }
    });
});



