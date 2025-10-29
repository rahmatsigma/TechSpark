// Fungsi ini sekarang menerima ID input mana yang mau di-toggle
function togglePassword(fieldId) {
    const passwordInput = document.getElementById(fieldId);
    if (passwordInput) {
        const type = passwordInput.type === 'password' ? 'text' : 'password';
        passwordInput.type = type;
    }
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

document.getElementById('registerForm').addEventListener('submit', function(e) {
    // Ambil semua nilai
    const fullName = document.getElementById('full_name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const passwordConfirm = document.getElementById('password_confirm').value;

    // 1. Cek jika ada yang kosong
    if (!fullName || !email || !password || !passwordConfirm) {
        e.preventDefault(); // Hentikan pengiriman form
        showError('Semua field wajib diisi!');
        return;
    }

    // 2. Cek jika password cocok
    if (password !== passwordConfirm) {
        e.preventDefault(); // Hentikan pengiriman form
        showError('Password dan Konfirmasi Password tidak cocok!');
        return;
    }

    // Jika semua validasi lolos, form akan disubmit ke Django
    console.log('Form disubmit ke Django...');
});

function loginWithGoogle() {
    alert('Login dengan Google - Fitur akan segera hadir!');
}

function loginWithFacebook() {
    alert('Login dengan Facebook - Fitur akan segera hadir!');
}