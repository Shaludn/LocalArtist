const langSelect = document.getElementById('langSelect');
let currentLang = localStorage.getItem('lang') || 'en';

function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('lang', lang);
    const t = translations[lang];

    document.getElementById('title').innerText = t.title;
    document.getElementById('subtitle').innerText = t.subtitle;
    document.getElementById('customerBtn').innerText = t.customerBtn;
    document.getElementById('customerDesc').innerText = t.customerDesc;
    document.getElementById('sellerBtn').innerText = t.sellerBtn;
    document.getElementById('sellerDesc').innerText = t.sellerDesc;
    document.getElementById('customerExplore').innerText = t.startSelling;
    document.getElementById('sellerStart').innerText = t.startSelling;
    document.getElementById('adminBtn').innerText = t.adminBtn;
    document.getElementById('adminDesc').innerText = t.adminDesc;
    document.getElementById('adminGo').innerText = t.goAdmin;

    document.getElementById('sellerWelcome').innerText = t.sellerWelcome;
    document.getElementById('uploadArtwork').innerText = t.uploadArtwork;
    document.getElementById('uploadDesc').innerText = t.uploadDesc;
    document.getElementById('aiDesigns').innerText = t.aiDesigns;
    document.getElementById('aiDesc').innerText = t.aiDesc;
    document.getElementById('notifications').innerText = t.notifications;
    document.getElementById('notifDesc').innerText = t.notifDesc;

    document.getElementById('loginBtn').innerText = t.login;
    document.getElementById('logoutBtn').innerText = t.logout;
}

langSelect.value = currentLang;
setLanguage(currentLang);

langSelect.addEventListener('change', (e) => {
    setLanguage(e.target.value);
});

document.getElementById('loginBtn').addEventListener('click', () => {
    localStorage.setItem('role', 'seller'); // simulate login
    document.getElementById('roleSelect').style.display = 'none';
    document.getElementById('sellerLanding').style.display = 'block';
    document.getElementById('loginBtn').style.display = 'none';
    document.getElementById('logoutBtn').style.display = 'inline-block';
});

document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('role');
    document.getElementById('roleSelect').style.display = 'block';
    document.getElementById('sellerLanding').style.display = 'none';
    document.getElementById('logoutBtn').style.display = 'none';
    document.getElementById('loginBtn').style.display = 'inline-block';
});

function goRole(role) {
    if (role === 'seller') {
        document.getElementById('roleSelect').style.display = 'none';
        document.getElementById('sellerLanding').style.display = 'block';
        document.getElementById('loginBtn').style.display = 'none';
        document.getElementById('logoutBtn').style.display = 'inline-block';
    } else {
        alert(`Redirecting to ${role} dashboard (not implemented in this demo)`);
    }
}
const BASE_URL = "http://localhost:3000"; // change to live URL after deployment