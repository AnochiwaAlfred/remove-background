
async function markAsRead(notificationID) {
    const notificationsUrl = `http://127.0.0.1:8000/api/v1/notifications/notification/${notificationID}/mark_as_read`;
    try {
        const response = await fetch(notificationsUrl, {
            method: 'PATCH',
        });

        if (response.ok) {
            const message = await response.json();
            // console.log(message);
            console.log("Marked as read");
        } else {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
    } catch (error) {
        // Handle errors here
        console.error('An error occurred:', error);
    }
}









document.addEventListener("DOMContentLoaded", async function () {
    const user_id = localStorage.getItem("user_id");
    const notificationsUrl = `http://127.0.0.1:8000/api/v1/notifications/${user_id}/list_all_notifications/`;

    try {
        const response = await fetch(notificationsUrl, {
            method: 'GET',
        });

        if (response.ok) {
            const notifications = await response.json();

            // Get the container where you want to append notifications
            const alertsContainer = document.getElementById('alerts');

            // Iterate through the notifications and create HTML elements
            notifications.forEach(notification => {
                const listItem = document.createElement('a');
                listItem.href = '#';
                listItem.className = 'filterNotifications all latest notification';
                listItem.setAttribute('data-toggle', 'list');
                listItem.setAttribute('onClick', `markAsRead('${notification.id}')`);

                // Create and append the rest of the HTML structure based on the notification data
                // ...
                const notificationImage = document.createElement('img')
                notificationImage.className = 'avatar-md'
                notificationImage.src = notification.sender.image;
                notificationImage.alt = "avatar";
                notificationImage.setAttribute('data-toggle', 'tooltip');
                notificationImage.setAttribute('data-placement', 'top');
                notificationImage.setAttribute('title', `${notification.sender.display_name}`);

                const notificationStatus = document.createElement('div')
                notificationStatus.className = 'status'
                const notificationIcon = document.createElement('i')
                if (notification.sender.is_online==true){
                    notificationIcon.className = 'material-icons online'
                }else{
                    notificationIcon.className = 'material-icons offline'
                }
                notificationIcon.innerHTML = 'fiber_manual_record'
                notificationStatus.appendChild(notificationIcon)

                const notificationData = document.createElement('div')
                notificationData.className = 'data'
                const notificationDataP = document.createElement('p')
                notificationDataP.innerHTML = notification.content
                const notificationTime = document.createElement('span')
                notificationTime.innerHTML = notification.timestamp
                notificationData.append(notificationDataP)
                notificationData.appendChild(notificationTime)


                listItem.appendChild(notificationImage)
                listItem.appendChild(notificationStatus)
                listItem.appendChild(notificationData)
                alertsContainer.appendChild(listItem);
            });
        } else {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
    } catch (error) {
        // Handle errors here
        console.error('An error occurred:', error);
    }







    const contactsUrl = `http://127.0.0.1:8000/api/v1/profiles/friendship/${user_id}/friends/`;
    try {
        const response = await fetch(contactsUrl, {
            method: 'GET',
        });

        if (response.ok) {
            const contacts = await response.json();

            // Get the container where you want to append contacts
            const contactsContainer = document.getElementById('contacts');

            // Iterate through the contacts and create HTML elements
            contacts.forEach(contact => {
                const anchorItem = document.createElement('a');
                anchorItem.href = '#';
                anchorItem.className = 'filterMembers all online contact';
                anchorItem.setAttribute('data-toggle', 'list');
                // anchorItem.setAttribute('onClick', `markAsRead('${contact.id}')`);

                // Create and append the rest of the HTML structure based on the contact data
                // ...
                const contactImage = document.createElement('img')
                contactImage.className = 'avatar-md'
                contactImage.src = contact.image;
                contactImage.alt = "avatar";
                contactImage.setAttribute('data-toggle', 'tooltip');
                contactImage.setAttribute('data-placement', 'top');
                contactImage.setAttribute('title', `${contact.display_name}`);

                const contactStatus = document.createElement('div')
                contactStatus.className = 'status'
                const contactIcon = document.createElement('i')
                if (contact.is_online==true){
                    contactIcon.className = 'material-icons online'
                }else{
                    contactIcon.className = 'material-icons offline'
                }
                contactIcon.innerHTML = 'fiber_manual_record'
                contactStatus.appendChild(contactIcon)

                const contactData = document.createElement('div')
                contactData.className = 'data'
                const contactDataP = document.createElement('p')
                contactDataP.innerHTML = contact.username
                const contactH5 = document.createElement('h5')
                contactH5.innerHTML = contact.display_name
                contactData.appendChild(contactH5)
                contactData.append(contactDataP)

                const contactPerson = document.createElement('div')
                contactPerson.className = 'person-add'
                const contactPersonIcon = document.createElement('i')
                contactPersonIcon.className = 'material-icons'
                contactPersonIcon.innerHTML = 'person'
                contactPerson.appendChild(contactPersonIcon)


                anchorItem.appendChild(contactImage)
                anchorItem.appendChild(contactStatus)
                anchorItem.appendChild(contactData)
                anchorItem.appendChild(contactPerson)
                contactsContainer.appendChild(anchorItem);
            });
        } else {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
    } catch (error) {
        // Handle errors here
        console.error('An error occurred:', error);
    }
});



document.addEventListener("DOMContentLoaded", async function () {
    document.getElementById('sendRequestButton').addEventListener('click', async (event) => {
    event.preventDefault();
    const userNameInput = document.getElementById('user').value;
    // Construct the URL with path parameters
    const url = `http://127.0.0.1:8000/api/v1/profiles/friendship/friends/add/`
    const userId = localStorage.getItem("user_id");
    // Call the endpoint to create a user object
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'accept': '*'
        },
        body: new URLSearchParams({
        user_id: userId,
            friend_username: userNameInput,
        }).toString(),
    })

    if (response.ok) {
        const message = await response.json();
        console.log('Friend Request Sent!');
        // callLoginPage();
        console.log(message)
    } else {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    // location.reload();
    });
});