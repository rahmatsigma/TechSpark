function togglePassword() {
    const passwordInput = document.getElementById('password');
    const type = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = type;
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// Event listener untuk form
document.getElementById('loginForm').addEventListener('submit', function(e) {
    // Kita tidak perlu e.preventDefault() lagi
    // Biarkan form dikirim secara normal ke backend Django
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Validasi sederhana
    if (!email || !password) {
        e.preventDefault(); // Hentikan pengiriman jika validasi gagal
        showError('Email dan password harus diisi!');
        return;
    }

    // Jika valid, form akan di-submit ke backend Django
    // (karena kita tidak pakai e.preventDefault() di sini)
    console.log('Form disubmit ke Django...');
});

function loginWithGoogle() {
    alert('Login dengan Google - Fitur akan segera hadir!');
}

function loginWithFacebook() {
    alert('Login dengan Facebook - Fitur akan segera hadir!');
}

// Kita tidak perlu cek localStorage lagi, 
// Django akan menangani sesi login di backend