@extends('layouts.app')
@section('title', 'Dashboard')

@section('content')
<div class="row mb-4">
    <div class="col">
        <h2 class="fw-bold" style="color: #1F4E79;">
            Reports Dashboard
        </h2>
        <p class="text-muted">Total Reports: {{ $allReports->count() }}</p>
    </div>
    <div class="col-auto d-flex align-items-center">
        <a href="/upload"
           class="btn text-white fw-bold"
           style="background: linear-gradient(135deg, #1F4E79, #2E75B6);
                  border-radius: 8px; padding: 10px 20px;">
            + Upload New Report
        </a>
    </div>
</div>

{{-- Success Message --}}
@if(session('success'))
    <div class="alert alert-success alert-dismissible fade show mb-4">
        {{ session('success') }}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
@endif

{{-- Summary Cards --}}
<div class="row mb-4">
    @php
        $types = ['CBC', 'LFT', 'RFT', 'BSG', 'Lipid'];
        $colors = ['1F4E79', '2E75B6', '70AD47', 'ED7D31', '9B59B6'];
    @endphp
    @foreach($types as $i => $testType)
    <div class="col-md-2 mb-3">
        <div class="card text-center p-3">
            <h4 style="color: #{{ $colors[$i] }};">
                {{ $allReports->where('test_type', $testType)->count() }}
            </h4>
            <small class="text-muted">{{ $testType }}</small>
        </div>
    </div>
    @endforeach
</div>

{{-- Search and Filter Bar --}}
<div class="card mb-3">
    <div class="card-body py-3">
        <form method="GET" action="/" id="searchForm">
            <div class="row g-2 align-items-center">
                <div class="col-md-6">
                    <div class="input-group">
                        <span class="input-group-text" style="background:#f0f4f8; border-color:#dde3ea;">
                            <i class="fas fa-search" style="color:#1F4E79;"></i>
                        </span>
                        <input type="text" name="search" id="searchInput"
                               class="form-control"
                               placeholder="Search by patient name, doc ID or test type..."
                               style="border-color:#dde3ea; background:#f0f4f8;"
                               value="{{ $query }}">
                    </div>
                </div>
                <div class="col-md-3">
                    <select name="type" id="typeFilter" class="form-select"
                            style="border-color:#dde3ea; background:#f0f4f8;"
                            onchange="document.getElementById('searchForm').submit()">
                        <option value="" {{ $type === '' ? 'selected' : '' }}>All Test Types</option>
                        <option value="CBC"   {{ $type === 'CBC'   ? 'selected' : '' }}>CBC</option>
                        <option value="LFT"   {{ $type === 'LFT'   ? 'selected' : '' }}>LFT</option>
                        <option value="RFT"   {{ $type === 'RFT'   ? 'selected' : '' }}>RFT</option>
                        <option value="BSG"   {{ $type === 'BSG'   ? 'selected' : '' }}>BSG</option>
                        <option value="Lipid" {{ $type === 'Lipid' ? 'selected' : '' }}>Lipid</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn w-100 text-white fw-bold"
                            style="background: linear-gradient(135deg, #1F4E79, #2E75B6);">
                        <i class="fas fa-search me-1"></i> Search
                    </button>
                </div>
                <div class="col-md-1">
                    <a href="/" class="btn btn-outline-secondary w-100" title="Clear">
                        <i class="fas fa-times"></i>
                    </a>
                </div>
            </div>

            {{-- Search Feedback --}}
            @if($query || $type)
            <div class="mt-2" style="font-size:13px; color:#1F4E79;">
                @if($reports->total() == 0)
                    <i class="fas fa-exclamation-circle me-1" style="color:#dc3545;"></i>
                    <span style="color:#dc3545;">No results found for
                        <strong>{{ $query }}{{ $type ? ' / '.$type : '' }}</strong>
                    </span>
                @else
                    <i class="fas fa-check-circle me-1"></i>
                    Showing <strong>{{ $reports->total() }}</strong> results for
                    <strong>{{ $query }}{{ $type ? ' / '.$type : '' }}</strong>
                @endif
            </div>
            @endif
        </form>
    </div>
</div>
{{-- Reports Table --}}
<div class="card">
    <div class="card-body">
        <table class="table table-hover">
            <thead style="background-color: #1F4E79; color: white;">
                <tr>
                    <th>#</th>
                    <th>Doc ID</th>
                    <th>Patient</th>
                    <th>Gender</th>
                    <th>Test Type</th>
                    <th>Date</th>
                    <th>Source</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                @forelse($reports as $report)
                <tr class="report-row"
                    data-name="{{ strtolower($report->patient_name) }}"
                    data-docid="{{ strtolower($report->doc_id) }}"
                    data-type="{{ $report->test_type }}">

                    <td>{{ $report->id }}</td>
                    <td><small>{{ $report->doc_id }}</small></td>
                    <td>
                        @if($report->patient_name == 'NOT_FOUND')
                            <span class="badge" style="background-color:#adb5bd; font-weight:500;">Not Found</span>
                        @else
                            {{ $report->patient_name }}
                        @endif
                    </td>
                    <td>
                        @if($report->patient_gender == 'NOT_FOUND')
                            <span class="badge" style="background-color:#adb5bd; font-weight:500;">Not Found</span>
                        @else
                            {{ $report->patient_gender }}
                        @endif
                    </td>
                    <td>
                        <span class="badge" style="background-color:
                            @if($report->test_type == 'CBC') #1F4E79
                            @elseif($report->test_type == 'LFT') #2E75B6
                            @elseif($report->test_type == 'RFT') #70AD47
                            @elseif($report->test_type == 'BSG') #ED7D31
                            @else #9B59B6
                            @endif">
                            {{ $report->test_type }}
                        </span>
                    </td>
                    <td>
                        @if($report->test_date == 'NOT_FOUND')
                            <span class="badge" style="background-color:#adb5bd; font-weight:500;">Not Found</span>
                        @else
                            {{ $report->test_date }}
                        @endif
                    </td>
                    <td><small>{{ $report->source_type }}</small></td>
                    <td class="d-flex gap-1">
                        <a href="/report/{{ $report->id }}"
                           class="btn btn-sm btn-primary">
                            View
                        </a>
                        <form method="POST" action="/report/{{ $report->id }}"
                              onsubmit="return confirm('Are you sure you want to delete this report? This cannot be undone.')">
                            @csrf
                            @method('DELETE')
                            <button type="submit" class="btn btn-sm btn-danger">
                                Delete
                            </button>
                        </form>
                    </td>
                </tr>
                @empty
                <tr>
                    <td colspan="8" class="text-center py-5">
                        <i class="fas fa-folder-open fa-3x mb-3" style="color: #ccc;"></i>
                        <p class="text-muted mb-1">No reports found.</p>
                        <a href="/upload" class="btn btn-sm btn-primary mt-2">
                            Upload Your First Report
                        </a>
                    </td>
                </tr>
                @endforelse
            </tbody>
        </table>
    </div>
</div>

{{-- Pagination --}}
@if($reports->hasPages())
<div class="d-flex justify-content-between align-items-center mt-3">
    <small class="text-muted">
        Showing {{ $reports->firstItem() }}–{{ $reports->lastItem() }}
        of {{ $allReports->count() }} reports
    </small>
    <nav>
        {{ $reports->links('pagination::bootstrap-5') }}
    </nav>
</div>
@endif

@endsection