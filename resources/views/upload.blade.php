@extends('layouts.app')
@section('title', 'Upload Report')

@section('content')
<div class="row justify-content-center">
    <div class="col-md-7">

        {{-- Back Button --}}
        <div class="mb-3">
            <a href="/" class="btn btn-outline-secondary btn-sm">
                ← Back to Dashboard
            </a>
        </div>

        {{-- Error Message --}}
        @if(session('error'))
            <div class="alert alert-danger alert-dismissible fade show">
                {{ session('error') }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        @endif

        {{-- Upload Card --}}
        <div class="card" style="border-radius: 16px; overflow: hidden;">

            {{-- Header --}}
            <div class="card-header text-white py-3"
                 style="background: linear-gradient(135deg, #1F4E79, #2E75B6);">
                <h5 class="mb-0 fw-bold">
                    Upload Medical Report
                </h5>
                <small style="opacity: 0.8;">
                    PDF, PNG or JPEG — Max 10MB
                </small>
            </div>

            <div class="card-body p-4">
                <form method="POST" action="/upload"
                      enctype="multipart/form-data" id="uploadForm">
                    @csrf

                    {{-- Drop Zone --}}
                    <div id="dropZone"
                         onclick="document.getElementById('report_file').click()"
                         style="
                            border: 2px dashed #2E75B6;
                            border-radius: 12px;
                            padding: 50px 20px;
                            text-align: center;
                            cursor: pointer;
                            background: #f0f6ff;
                            transition: all 0.3s;
                         ">
                        <div id="dropIcon">
                            <svg width="60" height="60" viewBox="0 0 24 24"
                                 fill="none" stroke="#2E75B6" stroke-width="1.5">
                                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                                <polyline points="14 2 14 8 20 8"/>
                                <line x1="12" y1="18" x2="12" y2="12"/>
                                <polyline points="9 15 12 12 15 15"/>
                            </svg>
                        </div>
                        <p class="mt-3 mb-1 fw-bold" style="color: #1F4E79;">
                            Click to browse or drag & drop
                        </p>
                        <p class="text-muted" style="font-size: 13px;">
                            Supported: PDF, PNG, JPEG
                        </p>
                        <div id="fileName" class="mt-2"
                             style="color: #2E75B6; font-size: 14px; font-weight: 600;">
                        </div>
                    </div>

                    {{-- Hidden File Input --}}
                    <input type="file" id="report_file" name="report_file"
                           accept=".pdf,.png,.jpg,.jpeg"
                           style="display: none;"
                           onchange="updateFileName(this)">

                    @error('report_file')
                        <div class="text-danger mt-2" style="font-size: 13px;">
                            {{ $message }}
                        </div>
                    @enderror

                    {{-- Supported Types --}}
                    {{-- Supported Types --}}
                    <div class="d-flex gap-2 mt-3 justify-content-center">
                        <span class="badge" style="background:#dc3545; font-size:12px;">PDF</span>
                        <span class="badge" style="background:#198754; font-size:12px;">PNG</span>
                        <span class="badge" style="background:#0d6efd; font-size:12px;">JPEG</span>
                    </div>

                    {{-- Test Type Selection --}}
                    <div class="mt-4">
                        <label class="form-label fw-bold" style="color:#1F4E79; font-size:14px;">
                            <i class="fas fa-flask me-1"></i>
                            Select Report Category <span class="text-danger">*</span>
                        </label>
                        <select name="selected_type" id="selected_type"
                                class="form-select"
                                style="border-color:#2E75B6; font-size:14px;"
                                required>
                            <option value="">-- Please select report type --</option>
                            <option value="CBC">CBC — Complete Blood Count</option>
                            <option value="LFT">LFT — Liver Function Test</option>
                            <option value="RFT">RFT — Renal Function Test</option>
                            <option value="BSG">BSG — Blood Sugar / Glucose</option>
                            <option value="Lipid">Lipid — Lipid Profile</option>
                            <option value="Other">Other — Unsupported / Unknown Type</option>
                        </select>
                        <small class="text-muted mt-1 d-block">
                            Select the category manually to ensure correct extraction.
                        </small>
                    </div>

                    {{-- Submit Button --}}
                    <button type="submit" id="submitBtn"
                            class="btn w-100 mt-4 py-3 fw-bold text-white"
                            style="background: linear-gradient(135deg, #1F4E79, #2E75B6);
                                   border-radius: 10px; font-size: 15px; border: none;">
                        Upload & Extract Data
                    </button>

                    {{-- Processing Message --}}
                    <div id="processingMsg"
                         class="text-center mt-3"
                         style="display: none; color: #2E75B6;">
                        <div class="spinner-border spinner-border-sm me-2"></div>
                        Processing report... Please wait.
                    </div>

                </form>
            </div>
        </div>

        {{-- Info Card --}}
        <div class="card mt-3" style="border-radius: 12px;">
            <div class="card-body py-3">
                <h6 class="fw-bold mb-2" style="color: #1F4E79;">
                    How it works:
                </h6>
                <div class="d-flex align-items-start gap-2 mb-2">
                    <span class="badge rounded-pill"
                          style="background:#1F4E79; min-width:22px;">1</span>
                    <small>Upload your lab report (PDF or image)</small>
                </div>
                <div class="d-flex align-items-start gap-2 mb-2">
                    <span class="badge rounded-pill"
                          style="background:#2E75B6; min-width:22px;">2</span>
                    <small>System automatically extracts patient info and medical values</small>
                </div>
                <div class="d-flex align-items-start gap-2">
                    <span class="badge rounded-pill"
                          style="background:#70AD47; min-width:22px;">3</span>
                    <small>Results appear on your dashboard instantly</small>
                </div>
            </div>
        </div>

    </div>
</div>

<script>
function updateFileName(input) {
    const fileName = document.getElementById('fileName');
    const dropZone = document.getElementById('dropZone');
    if (input.files && input.files[0]) {
        fileName.textContent = '✓ ' + input.files[0].name;
        dropZone.style.borderColor = '#198754';
        dropZone.style.background  = '#f0fff4';
    }
}

// Drag and Drop
const dropZone = document.getElementById('dropZone');
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#1F4E79';
    dropZone.style.background  = '#e8f0fe';
});
dropZone.addEventListener('dragleave', () => {
    dropZone.style.borderColor = '#2E75B6';
    dropZone.style.background  = '#f0f6ff';
});
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('report_file');
    fileInput.files = e.dataTransfer.files;
    updateFileName(fileInput);
});

// Show processing message on submit
document.getElementById('uploadForm').addEventListener('submit', function() {
    document.getElementById('submitBtn').disabled = true;
    document.getElementById('submitBtn').textContent = 'Processing...';
    document.getElementById('processingMsg').style.display = 'block';
});
</script>
@endsection