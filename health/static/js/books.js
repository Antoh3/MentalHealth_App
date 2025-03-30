const tabs = document.querySelectorAll("#tab");

tabs.forEach(tab => {
    tab.addEventListener("click", () => {
        let query;
        if (tab.textContent.trim() === "All") {
            query = "Mental health guidance and counseling";
        } else {
            query = tab.textContent.trim();
        }

        fetchBooksCategory(query);
    });
});


const fetchBooksCategory = async (category) => {
    const url = `https://www.googleapis.com/books/v1/volumes?q=${encodeURIComponent(category)}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        const booksContainer = document.getElementById("books-container");

        booksContainer.innerHTML = "";

        data.items.forEach(book => {
            const info = book.volumeInfo;
            const downloadLink = book.accessInfo?.pdf?.downloadLink || info.previewLink;

            const bookDiv = document.createElement("div");
            bookDiv.classList.add("book");

            bookDiv.innerHTML = `
                <img src="${info.imageLinks?.thumbnail || 'https://via.placeholder.com/150'}" alt="Book Image">
                <h3>${info.title}</h3>
                
                ${downloadLink ? `<a href="${downloadLink}" target="_blank" class="download-btn">Download</a>` : ""}
            `;

            booksContainer.appendChild(bookDiv);
        });
    } catch (error) {
        console.error("Error fetching books:", error);
    }
}




async function fetchBooks() {
    try {
        const response = await fetch("https://www.googleapis.com/books/v1/volumes?q=mental+health+guidance+and+counseling");
        const data = await response.json();
        const booksContainer = document.getElementById("books-container");

        data.items.forEach(book => {
            const info = book.volumeInfo;
            const downloadLink = book.accessInfo?.pdf?.downloadLink || info.previewLink;

            const bookDiv = document.createElement("div");
            bookDiv.classList.add("book");

            bookDiv.innerHTML = `
                <img src="${info.imageLinks?.thumbnail || 'https://via.placeholder.com/150'}" alt="Book Image">
                <h3>${info.title}</h3>
                
                ${downloadLink ? `<a href="${downloadLink}" target="_blank" class="download-btn">Download</a>` : ""}
            `;

            booksContainer.appendChild(bookDiv);
        });
    } catch (error) {
        console.error("Error fetching books:", error);
    }
}

fetchBooks();