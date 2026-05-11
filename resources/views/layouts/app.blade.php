<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>
        @hasSection('title')
            @yield('title') — Medical Document Analysis
        @else
            Medical Document Analysis
        @endif
    </title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .navbar { background-color: #1F4E79; }
        .navbar-brand, .nav-link { color: white !important; }
        .card { border: none; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .badge-cbc   { background-color: #1F4E79; }
        .badge-lft   { background-color: #2E75B6; }
        .badge-rft   { background-color: #70AD47; }
        .badge-bsg   { background-color: #ED7D31; }
        .badge-lipid { background-color: #9B59B6; }
        .nav-link.active-page {
            background: rgba(255,255,255,0.15);
            border-radius: 6px;
        }
        @media (max-width: 768px) {
            .navbar .d-flex { gap: 8px !important; }
            .register-wrapper { width: 100% !important; flex-direction: column; }
            .left-panel { display: none !important; }
            h2.fw-bold { font-size: 1.4rem; }
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg mb-4">
        <div class="container">
            {{-- Brand --}}
            <a class="navbar-brand fw-bold d-flex align-items-center gap-2" href="/">
                <i class="fas fa-notes-medical"></i>
                Medical Document Analysis
            </a>

            {{-- Mobile toggler --}}
            <button class="navbar-toggler border-light" type="button"
                    data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon" style="filter: invert(1);"></span>
            </button>

            {{-- Nav links --}}
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto ms-3">
                    @auth
                    <li class="nav-item">
                        <a class="nav-link {{ request()->is('/') ? 'active-page' : '' }}"
                           href="/">
                            <i class="fas fa-table me-1"></i>Dashboard
                        </a>
                    </li>
                    @endauth
                </ul>

                {{-- User info + logout --}}
                <div class="d-flex align-items-center gap-3">
                    @auth
                    <span class="text-white opacity-75" style="font-size:14px;">
                        <i class="fas fa-user-circle me-1"></i>
                        {{ Auth::user()->name }}
                        @if(Auth::user()->isAdmin())
                            <span class="badge bg-warning text-dark ms-1">Admin</span>
                        @endif
                    </span>
                    <form method="POST" action="/logout" class="m-0">
                        @csrf
                        <button type="submit"
                                class="btn btn-sm btn-outline-light">
                            <i class="fas fa-sign-out-alt me-1"></i>Logout
                        </button>
                    </form>
                    @endauth
                </div>
            </div>
        </div>
    </nav>

    <div class="container pb-5">
        @yield('content')
    </div>

    {{-- Footer --}}
    <footer style="background-color: #1F4E79; color: rgba(255,255,255,0.85);
                   padding: 18px 0; margin-top: 40px; font-size: 13px;">
        <div class="container d-flex justify-content-between align-items-center flex-wrap gap-2">
            <div>
                <i class="fas fa-notes-medical me-1"></i>
                <strong>Medical Document Analysis System</strong>
            </div>
            <div class="opacity-75">
                Final Year Project &nbsp;|&nbsp; 2025–2026
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>