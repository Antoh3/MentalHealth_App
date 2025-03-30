const youtubeApiKey = 'AIzaSyC4rf_npXpl-vcfMwjNw7GrQaWV2wkHkbM'; // Replace with your YouTube API key
const pexelsApiKey = '4F1cxJgWCUdHCrY02k2mFH1HpIigcDVYcqJnyBwkIOijdkmvCFCHUk8d'; // Replace with your Pexels API key
const pixabayApiKey = '49054213-4b536867bb64b511af4a98667'
const videoContainer = document.getElementById('yt-video-container');
const tabs = document.querySelectorAll(".tab1")

// search video accoring to category
const fetchVideosCategory = async (query) => {
    try {
        const youtubeResponse = await fetch(`https://www.googleapis.com/youtube/v3/search?part=snippet&q=${query}&type=video&maxResults=21&key=${youtubeApiKey}`);
        const youtubeData = await youtubeResponse.json();

        videoContainer.innerHTML = '';


        // Add YouTube videos
        youtubeData.items.forEach(video => {
            const videoId = video.id.videoId;
            const fullTitle = video.snippet.title;
            const words = fullTitle.split(' ');
            const shortTitle = words.length > 7 ? words.slice(0, 7).join(' ') + '...' : fullTitle;
            const downloadUrl = `https://ssyoutube.com/watch?v=${videoId}`;

            const videoElement = `
                        <div class="col-md-4 mb-3">
                            <div class="card shadow-lg video-card">
                                <iframe width="100%" height="300" src="https://www.youtube.com/embed/${videoId}" frameborder="0" allowfullscreen></iframe>
                                <div class="card-body">
                                    <h6 class="card-title video-title">${shortTitle}</h6>
                                    ${words.length > 7 ? `<button class="view-more-btn" onclick="toggleTitle(this, '${fullTitle}')">View More</button>` : ''}
                                    <a href="${downloadUrl}" target="_blank" class="btn btn-success btn-sm">Download</a>
                                </div>
                            </div>
                        </div>
                    `;
            videoContainer.innerHTML += videoElement;
        });



    } catch (error) {
        console.error("error in fetching data");
    }

}
tabs.forEach((tab) =>{
    tab.addEventListener("click",() =>{
        let query;
        if (tab.textContent.trim() === "All") {
            query = "Mental health and guidance"
        }else if(tab.textContent.trim() === "Shorts"){
            query = "Mental short videos"
        }else{
            query = tab.textContent.trim();
        }
        fetchVideosCategory(query);
    })
})



// search video
document.getElementById("searchBtn").addEventListener("click", () => {
    const query = document.getElementById("searchInput").value.trim();
    if (query) {
        searchVideos(query);
    }
});
async function searchVideos(category) {
    const pixabayUrl = `https://pixabay.com/api/videos/?key=${pixabayApiKey}&q=${encodeURIComponent(category)}`;
    const youtubeUrl = `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(category)}&type=video&maxResults=21&key=${youtubeApiKey}`;
    const pexelsUrl = `https://api.pexels.com/videos/search?query=${encodeURIComponent(category)}&per_page=6`;

    try {
        const [pixabayRes, youtubeRes, pexelsRes] = await Promise.all([
            fetch(pixabayUrl),
            fetch(youtubeUrl),
            fetch(pexelsUrl, { headers: { Authorization: pexelsApiKey } }).then(res => res.json())
        ]);

        const youtubeData = await youtubeRes.json();

        console.log(("data", youtubeData));

        videoContainer.innerHTML = '';


        // Add YouTube videos
        youtubeData.items.forEach(video => {
            const videoId = video.id.videoId;
            const fullTitle = video.snippet.title;
            const words = fullTitle.split(' ');
            const shortTitle = words.length > 7 ? words.slice(0, 7).join(' ') + '...' : fullTitle;
            const downloadUrl = `https://ssyoutube.com/watch?v=${videoId}`;

            const videoElement = `
                        <div class="col-md-4 mb-3">
                            <div class="card shadow-lg video-card">
                                <iframe width="100%" height="300" src="https://www.youtube.com/embed/${videoId}" frameborder="0" allowfullscreen></iframe>
                                <div class="card-body">
                                    <h6 class="card-title video-title">${shortTitle}</h6>
                                    ${words.length > 7 ? `<button class="view-more-btn" onclick="toggleTitle(this, '${fullTitle}')">View More</button>` : ''}
                                    <a href="${downloadUrl}" target="_blank" class="btn btn-success btn-sm">Download</a>
                                </div>
                            </div>
                        </div>
                    `;
            videoContainer.innerHTML += videoElement;
        });

    } catch (error) {
        console.error("Error fetching videos:", error);
    }
}


// Display video when page loads
async function fetchVideos() {
    let query = "mental+health+and+guidance";
    const pixabayUrl = `https://pixabay.com/api/videos/?key=${pixabayApiKey}&q=mental+health`;
    const youtubeUrl = `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${query}&type=video&maxResults=21&key=${youtubeApiKey}`;
    const pexelsUrl = `https://api.pexels.com/videos/search?query=mental%20health&per_page=6`;

    try {
        const [youtubeResponse, pexelsResponse, pixabayResponse] = await Promise.all([
            fetch(youtubeUrl),
            fetch(pexelsUrl, { headers: { Authorization: pexelsApiKey } }),
            fetch(pixabayUrl)
        ]);

        const youtubeData = await youtubeResponse.json();
        const pexelsData = await pexelsResponse.json();
        const pixabayData = await pixabayResponse.json();


        videoContainer.innerHTML = '';

        // Add YouTube videos
        youtubeData.items.forEach(video => {
            const videoId = video.id.videoId;
            const fullTitle = video.snippet.title;
            const words = fullTitle.split(' ');
            const shortTitle = words.length > 7 ? words.slice(0, 7).join(' ') + '...' : fullTitle;
            const downloadUrl = `https://ssyoutube.com/watch?v=${videoId}`;

            const videoElement = `
                        <div class="col-md-4 mb-3">
                            <div class="card shadow-lg video-card">
                                <iframe width="100%" height="300" src="https://www.youtube.com/embed/${videoId}" frameborder="0" allowfullscreen></iframe>
                                <div class="card-body">
                                    <h6 class="card-title video-title">${shortTitle}</h6>
                                    ${words.length > 7 ? `<button class="view-more-btn" onclick="toggleTitle(this, '${fullTitle}')">View More</button>` : ''}
                                    <a href="${downloadUrl}" target="_blank" class="btn btn-success btn-sm">Download</a>
                                </div>
                            </div>
                        </div>
                    `;
            videoContainer.innerHTML += videoElement;
        });


    } catch (error) {
        console.error('Error fetching videos:', error);
    }
}

function toggleTitle(button, fullTitle) {
    const titleElement = button.previousElementSibling;
    const isExpanded = !titleElement.innerText.endsWith('...');

    titleElement.innerText = isExpanded ? fullTitle.split(' ').slice(0, 7).join(' ') + '...' : fullTitle;
    button.innerText = isExpanded ? 'View More' : 'Show Less';
}

document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.querySelector(".yt-menu");
    const sidebar = document.querySelector(".yt-sidebar");
    const videoSection = document.querySelector(".yt-video");

    menuButton.addEventListener("click", function () {
        sidebar.classList.toggle("sidebar-collapsed");
        videoSection.classList.toggle("sidebar-collapsed");
    });

    fetchVideos();
});


document.querySelector('.navbar-toggler').addEventListener('click', function () {
    const sidebar = document.getElementById('sidebarCollapse');
    sidebar.classList.toggle('d-none');
});

// document.addEventListener("DOMContentLoaded", function () {
//     const menuButton = document.querySelector(".yt-menu");
//     const sidebar = document.querySelector(".yt-sidebar");

//     menuButton.addEventListener("click", function () {
//         sidebar.classList.toggle("collapsed");
//     });
// });

// document.addEventListener("DOMContentLoaded", function () {
//     fetchVideos()
// });