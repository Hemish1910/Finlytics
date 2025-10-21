document.addEventListener('DOMContentLoaded', function() {
    // Navigation
    const navItems = document.querySelectorAll('.nav-link');
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const targetSection = this.getAttribute('href');
            showSection(targetSection);
        });
    });

    function showSection(sectionId) {
        const sections = document.querySelectorAll('.section');
        sections.forEach(section => section.style.display = 'none');
        document.querySelector(sectionId).style.display = 'block';
        // Reset nav active state
        navItems.forEach(item => item.classList.remove('active'));
        document.querySelector(`[href="${sectionId}"]`).classList.add('active');
    }

    // Initial setup
    showSection('#instagram');
    populateNiches();
    displayInstagram();
    displayYouTube();
    displayAnalytics();

    // Search and filters
    document.getElementById('insta-search').addEventListener('input', filterInstagram);
    document.getElementById('insta-niche').addEventListener('change', filterInstagram);
    document.getElementById('yt-search').addEventListener('input', filterYouTube);
    document.getElementById('yt-niche').addEventListener('change', filterYouTube);
});

function populateNiches() {
    const niches = window.niches;
    const instaNicheSelect = document.getElementById('insta-niche');
    const ytNicheSelect = document.getElementById('yt-niche');

    niches.forEach(niche => {
        const option = document.createElement('option');
        option.value = niche;
        option.textContent = niche;
        instaNicheSelect.appendChild(option.cloneNode(true));
        ytNicheSelect.appendChild(option);
    });
}

function displayInstagram(filteredData = null) {
    const data = filteredData || window.instagramData;
    const container = document.getElementById('insta-list');
    container.innerHTML = '';
    data.forEach(account => {
        const card = createCard(account, 'instagram');
        container.appendChild(card);
    });
    updateInstagramChart(data);
}

function displayYouTube(filteredData = null) {
    const data = filteredData || window.youtubeData;
    const container = document.getElementById('yt-list');
    container.innerHTML = '';
    data.forEach(account => {
        const card = createCard(account, 'youtube');
        container.appendChild(card);
    });
    updateYouTubeChart(data);
}

function createCard(account, platform) {
    const card = document.createElement('div');
    card.className = 'col-md-4 col-sm-6';
    card.innerHTML = `
        <div class="card h-100">
            <img src="${account.profilePic}" class="card-img-top" alt="${account.name}">
            <div class="card-body d-flex flex-column">
                <h5 class="card-title">${account.name}</h5>
                <p class="card-text">@${account.username}</p>
                <p class="card-text"><small class="text-muted">${platform === 'instagram' ? account.followers.toLocaleString() + ' followers' : account.subscribers.toLocaleString() + ' subscribers'}</small></p>
                <p class="card-text"><em>${account.niche}</em></p>
                <button class="btn btn-primary mt-auto" onclick="showDetails('${account.id}', '${platform}')">View Details</button>
            </div>
        </div>
    `;
    return card;
}

function showDetails(id, platform) {
    const data = platform === 'instagram' ? window.instagramData : window.youtubeData;
    const account = data.find(a => a.id == id);
    
    document.getElementById('modal-title').textContent = `${account.name} (@${account.username})`;
    document.getElementById('modal-body').innerHTML = `
        <img src="${account.profilePic}" class="img-fluid rounded mb-3" alt="${account.name}">
        <p><strong>Niche:</strong> ${account.niche}</p>
        <p><strong>Bio/Description:</strong> ${account.bio || account.description}</p>
        <div class="row">
            <div class="col-md-6">
                <p><strong>${platform === 'instagram' ? 'Followers' : 'Subscribers'}:</strong> ${platform === 'instagram' ? account.followers.toLocaleString() : account.subscribers.toLocaleString()}</p>
            </div>
            <div class="col-md-6">
                <p><strong>${platform === 'instagram' ? 'Posts' : 'Videos'}:</strong> ${platform === 'instagram' ? account.posts : account.videos}</p>
            </div>
        </div>
        ${platform === 'instagram' ? `<p><strong>Engagement Rate:</strong> ${account.engagement}%</p>` : `<p><strong>Total Views:</strong> ${account.views.toLocaleString()}</p><p><strong>Average Views per Video:</strong> ${account.avgViews.toLocaleString()}</p>`}
    `;
    
    const modal = new bootstrap.Modal(document.getElementById('details-modal'));
    modal.show();
}

function filterInstagram() {
    const searchTerm = document.getElementById('insta-search').value.toLowerCase();
    const nicheFilter = document.getElementById('insta-niche').value;
    const filtered = window.instagramData.filter(account => {
        return (account.name.toLowerCase().includes(searchTerm) || account.username.toLowerCase().includes(searchTerm)) &&
               (!nicheFilter || account.niche === nicheFilter);
    });
    displayInstagram(filtered);
}

function filterYouTube() {
    const searchTerm = document.getElementById('yt-search').value.toLowerCase();
    const nicheFilter = document.getElementById('yt-niche').value;
    const filtered = window.youtubeData.filter(account => {
        return (account.name.toLowerCase().includes(searchTerm) || account.username.toLowerCase().includes(searchTerm)) &&
               (!nicheFilter || account.niche === nicheFilter);
    });
    displayYouTube(filtered);
}

function updateInstagramChart(data) {
    const nicheCounts = {};
    data.forEach(account => {
        nicheCounts[account.niche] = (nicheCounts[account.niche] || 0) + 1;
    });
    
    new Chart(document.getElementById('insta-niche-chart'), {
        type: 'pie',
        data: {
            labels: Object.keys(nicheCounts),
            datasets: [{
                data: Object.values(nicheCounts),
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
            }]
        },
        options: {
            responsive: true
        }
    });
}

function updateYouTubeChart(data) {
    const nicheCounts = {};
    data.forEach(account => {
        nicheCounts[account.niche] = (nicheCounts[account.niche] || 0) + 1;
    });
    
    new Chart(document.getElementById('yt-niche-chart'), {
        type: 'pie',
        data: {
            labels: Object.keys(nicheCounts),
            datasets: [{
                data: Object.values(nicheCounts),
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
            }]
        },
        options: {
            responsive: true
        }
    });
}

function displayAnalytics() {
    // Combined bar chart for followers/subscribers
    const instaFollowers = window.instagramData.reduce((sum, acc) => sum + acc.followers, 0);
    const ytSubscribers = window.youtubeData.reduce((sum, acc) => sum + acc.subscribers, 0);
    
    new Chart(document.getElementById('combined-chart'), {
        type: 'bar',
        data: {
            labels: ['Instagram Followers', 'YouTube Subscribers'],
            datasets: [{
                label: 'Total',
                data: [instaFollowers, ytSubscribers],
                backgroundColor: ['#E4405F', '#FF0000']
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Niche comparison
    const instaNiches = {};
    const ytNiches = {};
    
    window.instagramData.forEach(acc => instaNiches[acc.niche] = (instaNiches[acc.niche] || 0) + acc.followers);
    window.youtubeData.forEach(acc => ytNiches[acc.niche] = (ytNiches[acc.niche] || 0) + acc.subscribers);
    
    new Chart(document.getElementById('niche-comparison-chart'), {
        type: 'horizontalBar',
        data: {
            labels: window.niches,
            datasets: [{
                label: 'Instagram',
                data: window.niches.map(n => instaNiches[n] || 0),
                backgroundColor: '#E4405F'
            }, {
                label: 'YouTube',
                data: window.niches.map(n => ytNiches[n] || 0),
                backgroundColor: '#FF0000'
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    beginAtZero: true
                }
            }
        }
    });

    // Growth chart (mock data)
    const growthLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
    const growthData = [1000, 1200, 1400, 1600, 1800, 2000];
    
    new Chart(document.getElementById('growth-chart'), {
        type: 'line',
        data: {
            labels: growthLabels,
            datasets: [{
                label: 'Follows/Subscribes Growth',
                data: growthData,
                borderColor: '#28a745',
                tension: 0.1
            }]
        },
        options: {
            responsive: true
        }
    });

    // Top list
    const topList = [...window.instagramData.map(acc => ({...acc, metric: acc.followers, platform: 'IG'})),
                     ...window.youtubeData.map(acc => ({...acc, metric: acc.subscribers, platform: 'YT'}))];
    topList.sort((a, b) => b.metric - a.metric);
    const ul = document.getElementById('top-list');
    ul.innerHTML = '';
    topList.slice(0, 5).forEach(req => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.textContent = `${req.name} (@${req.username})`;
        li.innerHTML += `<span class="badge bg-primary rounded-pill">${req.metric.toLocaleString()}</span>`;
        ul.appendChild(li);
    });
}
