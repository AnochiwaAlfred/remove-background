// async function markAsRead(notificationID) {
//     const notificationsUrl = `http://127.0.0.1:8000/api/v1/notifications/notification/${notificationID}/mark_as_read`;
//     try {
//         const response = await fetch(notificationsUrl, {
//             method: 'PATCH',
//         });

//         if (response.ok) {
//             const message = await response.json();
//             // console.log(message);
//             console.log("Marked as read");
//         } else {
//             throw new Error(`HTTP error! Status: ${response.status}`);
//         }
//     } catch (error) {
//         // Handle errors here
//         console.error('An error occurred:', error);
//     }
// }

document.addEventListener("DOMContentLoaded", async function () {
  const user_id = localStorage.getItem("user_id");
  const galleryItemsUrl = `http://127.0.0.1:8000/api/v1/clean_image/${user_id}/images/`;

  try {
    const response = await fetch(galleryItemsUrl, {
      method: "GET",
    });

    if (response.ok) {
      const gallery = await response.json();

      // Get the container where you want to append gallery
      const galleryContainer = document.getElementById("gallery-row");

      // Iterate through the gallery and create HTML elements
      gallery.forEach((galleryItem) => {
        const listItem = document.createElement("div");
        listItem.className = "col-lg-4 col-md-6 ma_bottom30 mb-5";

        const div1 = document.createElement("div");
        div1.className = "lightbox";

        const galleryImage = document.createElement("img");
        galleryImage.src = galleryItem.image;
        galleryImage.alt = "Removed Item BG";

        const div2 = document.createElement("div");
        div2.className = "view_main";

        const div3 = document.createElement("div");
        div3.className = "pose";

        const anchor1 = document.createElement("a");
        anchor1.className = "read_more";
        anchor1.href = galleryItem.image;
        anchorImage = document.createElement("img");
        anchorImage.src = "images/ga.png";
        anchorImage.setAttribute("alt", "#");
        anchor1.appendChild(anchorImage);

        para = document.createElement("p");
        para.innerHTML =
          "more-or-less normal distribution of<br> letters, as opposed to using";

        div3.appendChild(anchor1);
        div3.appendChild(para);
        div2.appendChild(div3);
        div1.appendChild(galleryImage);
        div1.appendChild(div2);
        listItem.appendChild(div1);
        galleryContainer.appendChild(listItem);
      });
    } else {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
  } catch (error) {
    // Handle errors here
    console.error("An error occurred:", error);
  }
});


document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('submitImage').addEventListener('click', async (event) => {
        event.preventDefault();

        // Get the file directly from the input element:
        const imageFile = document.getElementById('image').files[0];

        // Get the user_id before creating FormData:
        const userId = localStorage.getItem('user_id');

        // Create FormData with the image file and user_id:
        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('user_id', userId);

        // Make the request:
        const url = 'http://127.0.0.1:8000/api/v1/clean_image/image/process/';
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
        });

        try {
            if (response.ok) {
                const { message } = await response.json();
                console.log(message);
                location.reload()
                // Handle successful processing
            } else {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
        } catch (error) {
            console.error('Error processing image:', error);
            // Handle errors gracefully
        }
    });
});


