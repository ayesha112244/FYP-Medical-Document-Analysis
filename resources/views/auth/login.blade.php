<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login — Medical Document Analysis</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            min-height: 100vh;
            background: linear-gradient(135deg, #1F4E79 0%, #2E75B6 50%, #1a3a5c 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', sans-serif;
        }

        .login-wrapper {
            display: flex;
            width: 900px;
            min-height: 520px;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 25px 60px rgba(0,0,0,0.3);
        }

        /* Left Panel */
        .left-panel {
            flex: 1;
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.15);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 50px 40px;
            color: white;
        }

        .left-panel .icon-circle {
            width: 90px;
            height: 90px;
            background: rgba(255,255,255,0.15);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 25px;
            border: 2px solid rgba(255,255,255,0.3);
        }

        .left-panel .icon-circle i {
            font-size: 40px;
            color: white;
        }

        .left-panel h2 {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 12px;
            text-align: center;
        }

        .left-panel p {
            font-size: 14px;
            text-align: center;
            opacity: 0.8;
            line-height: 1.7;
        }

        .feature-item {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-top: 20px;
            width: 100%;
        }

        .feature-item i {
            font-size: 16px;
            color: #90CAF9;
            width: 20px;
        }

        .feature-item span {
            font-size: 13px;
            opacity: 0.85;
        }

        /* Right Panel */
        .right-panel {
            flex: 1;
            background: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 50px 45px;
        }

        .right-panel h3 {
            font-size: 26px;
            font-weight: 700;
            color: #1F4E79;
            margin-bottom: 6px;
        }

        .right-panel .subtitle {
            font-size: 14px;
            color: #888;
            margin-bottom: 30px;
        }

        .form-label {
            font-size: 13px;
            font-weight: 600;
            color: #444;
            margin-bottom: 6px;
        }

        .input-group-text {
            background: #f0f4f8;
            border: 1px solid #dde3ea;
            border-right: none;
            color: #1F4E79;
        }

        .form-control {
            border: 1px solid #dde3ea;
            border-left: none;
            padding: 10px 15px;
            font-size: 14px;
            background: #f0f4f8;
        }

        .form-control:focus {
            box-shadow: none;
            border-color: #2E75B6;
            background: white;
        }

        .input-group:focus-within .input-group-text {
            border-color: #2E75B6;
            background: white;
        }

        .btn-login {
            background: linear-gradient(135deg, #1F4E79, #2E75B6);
            color: white;
            border: none;
            padding: 12px;
            font-size: 15px;
            font-weight: 600;
            border-radius: 8px;
            width: 100%;
            margin-top: 10px;
            transition: all 0.3s;
            letter-spacing: 0.5px;
        }

        .btn-login:hover {
            background: linear-gradient(135deg, #163a5a, #1F4E79);
            transform: translateY(-1px);
            box-shadow: 0 5px 15px rgba(31,78,121,0.3);
        }

        .register-link {
            text-align: center;
            margin-top: 20px;
            font-size: 13px;
            color: #888;
        }

        .register-link a {
            color: #2E75B6;
            font-weight: 600;
            text-decoration: none;
        }

        .register-link a:hover {
            text-decoration: underline;
        }

        .alert-danger {
            font-size: 13px;
            border-radius: 8px;
            border: none;
            background: #fff0f0;
            color: #c0392b;
            padding: 10px 15px;
        }
    </style>
</head>
<body>

<div class="login-wrapper">

    {{-- Left Panel --}}
    <div class="left-panel">
        <div class="icon-circle">
            <i class="fas fa-file-medical"></i>
        </div>
        <h2>Medical Document Analysis</h2>
        <p>AI-powered lab report extraction and analysis system</p>

        <div class="feature-item">
            <i class="fas fa-check-circle"></i>
            <span>Automatic data extraction from PDF & images</span>
        </div>
        <div class="feature-item">
            <i class="fas fa-check-circle"></i>
            <span>CBC, LFT, RFT, BSG & Lipid Profile support</span>
        </div>
        <div class="feature-item">
            <i class="fas fa-check-circle"></i>
            <span>Secure & private report management</span>
        </div>
        <div class="feature-item">
            <i class="fas fa-check-circle"></i>
            <span>University of Huddersfield — FYP 2025/26</span>
        </div>
    </div>

    {{-- Right Panel --}}
    <div class="right-panel">
        <h3>Welcome Back</h3>
        <p class="subtitle">Sign in to access your reports</p>

        @if($errors->any())
            <div class="alert alert-danger mb-3">
                <i class="fas fa-exclamation-circle me-2"></i>
                {{ $errors->first() }}
            </div>
        @endif

        <form method="POST" action="/login">
            @csrf

            <div class="mb-3">
                <label class="form-label">Email Address</label>
                <div class="input-group">
                    <span class="input-group-text">
                        <i class="fas fa-envelope fa-sm"></i>
                    </span>
                    <input type="email" name="email"
                           class="form-control"
                           placeholder="Enter your email"
                           value="{{ old('email') }}"
                           required>
                </div>
            </div>

            <div class="mb-3">
                <label class="form-label">Password</label>
                <div class="input-group">
                    <span class="input-group-text">
                        <i class="fas fa-lock fa-sm"></i>
                    </span>
                    <input type="password" name="password"
                        id="passwordField"
                        class="form-control"
                        placeholder="Enter your password"
                        required>
                    <span class="input-group-text"
                        style="cursor:pointer; border-left:none;"
                        onclick="togglePassword()">
                        <i class="fas fa-eye" id="eyeIcon"></i>
                    </span>
                </div>
            </div>

            <button type="submit" class="btn-login">
                <i class="fas fa-sign-in-alt me-2"></i>Sign In
            </button>
        </form>

        <div class="register-link">
            Don't have an account?
            <a href="/register">Create one here</a>
        </div>
    </div>

</div>
<script>
function togglePassword() {
    const field = document.getElementById('passwordField');
    const icon  = document.getElementById('eyeIcon');
    if (field.type === 'password') {
        field.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        field.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}
</script>
</body>
</html>