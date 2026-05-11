<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register — Medical Document Analysis</title>
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

        .register-wrapper {
            display: flex;
            width: 900px;
            min-height: 580px;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 25px 60px rgba(0,0,0,0.3);
        }

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

        .step-item {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin-top: 18px;
            width: 100%;
        }

        .step-num {
            width: 26px;
            height: 26px;
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 700;
            flex-shrink: 0;
        }

        .step-item span {
            font-size: 13px;
            opacity: 0.85;
            padding-top: 4px;
        }

        .right-panel {
            flex: 1;
            background: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 45px 45px;
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
            margin-bottom: 25px;
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

        .btn-register {
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
        }

        .btn-register:hover {
            background: linear-gradient(135deg, #163a5a, #1F4E79);
            transform: translateY(-1px);
            box-shadow: 0 5px 15px rgba(31,78,121,0.3);
        }

        .login-link {
            text-align: center;
            margin-top: 18px;
            font-size: 13px;
            color: #888;
        }

        .login-link a {
            color: #2E75B6;
            font-weight: 600;
            text-decoration: none;
        }

        input[type="password"]::-ms-reveal,
        input[type="password"]::-webkit-contacts-auto-fill-button,
        input::-webkit-credentials-auto-fill-button { display: none !important; }
        
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

<div class="register-wrapper">

    {{-- Left Panel --}}
    <div class="left-panel">
        <div class="icon-circle">
            <i class="fas fa-user-plus"></i>
        </div>
        <h2>Create Your Account</h2>
        <p>Join the Medical Document Analysis system</p>

        <div class="step-item">
            <div class="step-num">1</div>
            <span>Register with your email and password</span>
        </div>
        <div class="step-item">
            <div class="step-num">2</div>
            <span>Login to your personal dashboard</span>
        </div>
        <div class="step-item">
            <div class="step-num">3</div>
            <span>Upload your lab reports (PDF or image)</span>
        </div>
        <div class="step-item">
            <div class="step-num">4</div>
            <span>View automatically extracted medical values</span>
        </div>
    </div>

    {{-- Right Panel --}}
    <div class="right-panel">
        <h3>Create Account</h3>
        <p class="subtitle">Fill in the details below to get started</p>

        @if($errors->any())
            <div class="alert alert-danger mb-3">
                <i class="fas fa-exclamation-circle me-2"></i>
                {{ $errors->first() }}
            </div>
        @endif

        <form method="POST" action="/register">
            @csrf

            <div class="mb-3">
                <label class="form-label">Full Name</label>
                <div class="input-group">
                    <span class="input-group-text">
                        <i class="fas fa-user fa-sm"></i>
                    </span>
                    <input type="text" name="name"
                           class="form-control"
                           placeholder="Enter your full name"
                           value="{{ old('name') }}"
                           required>
                </div>
            </div>

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
                           id="password"
                           class="form-control"
                           placeholder="Minimum 6 characters"
                           required>
                    <button type="button" class="btn btn-outline-secondary"
                            style="border-color:#dde3ea; background:#f0f4f8;"
                            onclick="togglePass('password','eyeIcon1')">
                        <i class="fas fa-eye fa-sm" id="eyeIcon1" style="color:#1F4E79;"></i>
                    </button>
                </div>
            </div>

            <div class="mb-3">
                <label class="form-label">Confirm Password</label>
                <div class="input-group">
                    <span class="input-group-text">
                        <i class="fas fa-lock fa-sm"></i>
                    </span>
                    <input type="password" name="password_confirmation"
                           id="password_confirmation"
                           class="form-control"
                           placeholder="Repeat your password"
                           required>
                    <button type="button" class="btn btn-outline-secondary"
                            style="border-color:#dde3ea; background:#f0f4f8;"
                            onclick="togglePass('password_confirmation','eyeIcon2')">
                        <i class="fas fa-eye fa-sm" id="eyeIcon2" style="color:#1F4E79;"></i>
                    </button>
                </div>
            </div>

            <button type="submit" class="btn-register">
                <i class="fas fa-user-plus me-2"></i>Create Account
            </button>
        </form>

        <div class="login-link">
            Already have an account?
            <a href="/login">Sign in here</a>
        </div>
    </div>

</div>

<script>
    function togglePass(fieldId, iconId) {
        const field = document.getElementById(fieldId);
        const icon  = document.getElementById(iconId);
        if (field.type === 'password') {
            field.type = 'text';
            icon.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            field.type = 'password';
            icon.classList.replace('fa-eye-slash', 'fa-eye');
        }
    }
</script>

</body>
</html>