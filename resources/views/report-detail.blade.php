@extends('layouts.app')
@section('title', 'Report Details')

@section('content')

@php
$paramInfo = [
    // CBC
    'Haemoglobin'         => ['unit' => 'g/dL',      'min' => 13.5, 'max' => 17.5],
    'RBC'                 => ['unit' => '×10⁶/µL',   'min' => 4.5,  'max' => 5.9],
    'PCV_HCT'             => ['unit' => '%',          'min' => 41.0, 'max' => 53.0],
    'MCV'                 => ['unit' => 'fL',         'min' => 80.0, 'max' => 100.0],
    'MCH'                 => ['unit' => 'pg',         'min' => 27.0, 'max' => 33.0],
    'MCHC'                => ['unit' => 'g/dL',       'min' => 32.0, 'max' => 36.0],
    'RDW'                 => ['unit' => '%',          'min' => 11.5, 'max' => 14.5],
    'WBC'                 => ['unit' => '×10³/µL',   'min' => 4.0,  'max' => 11.0],
    'Platelets'           => ['unit' => '×10³/µL',   'min' => 150.0,'max' => 400.0],
    'Neutrophils'         => ['unit' => '×10³/µL',   'min' => 1.8,  'max' => 7.7],
    'Lymphocytes'         => ['unit' => '×10³/µL',   'min' => 1.0,  'max' => 4.8],

    // LFT
    'ALT'                 => ['unit' => 'U/L',        'min' => 7.0,  'max' => 56.0],
    'AST'                 => ['unit' => 'U/L',        'min' => 10.0, 'max' => 40.0],
    'ALP'                 => ['unit' => 'U/L',        'min' => 44.0, 'max' => 147.0],
    'GGT'                 => ['unit' => 'U/L',        'min' => 8.0,  'max' => 61.0],
    'Bilirubin_Total'     => ['unit' => 'mg/dL',      'min' => 0.2,  'max' => 1.2],
    'Albumin'             => ['unit' => 'g/dL',       'min' => 3.5,  'max' => 5.0],

    // RFT
    'Creatinine'          => ['unit' => 'mg/dL',      'min' => 0.7,  'max' => 1.3],
    'Urea'                => ['unit' => 'mg/dL',      'min' => 7.0,  'max' => 20.0],
    'eGFR'                => ['unit' => 'mL/min/1.73m²', 'min' => 60.0, 'max' => 120.0],
    'Potassium'           => ['unit' => 'mmol/L',     'min' => 3.5,  'max' => 5.1],
    'Sodium'              => ['unit' => 'mmol/L',     'min' => 136.0,'max' => 145.0],
    'Uric_Acid'           => ['unit' => 'mg/dL',      'min' => 3.5,  'max' => 7.2],

    // BSG
    'Fasting_Glucose'     => ['unit' => 'mg/dL',      'min' => 70.0, 'max' => 99.0],
    'Post_Prandial_Glucose'=> ['unit' => 'mg/dL',     'min' => 70.0, 'max' => 140.0],
    'Random_Glucose'      => ['unit' => 'mg/dL',      'min' => 70.0, 'max' => 140.0],
    'HbA1c'               => ['unit' => '%',          'min' => 4.0,  'max' => 5.6],
    'Fasting_Insulin'     => ['unit' => 'µIU/mL',    'min' => 2.6,  'max' => 24.9],

    // Lipid
    'Total_Cholesterol'   => ['unit' => 'mg/dL',      'min' => 0.0,  'max' => 200.0],
    'LDL'                 => ['unit' => 'mg/dL',      'min' => 0.0,  'max' => 100.0],
    'HDL'                 => ['unit' => 'mg/dL',      'min' => 40.0, 'max' => 999.0],
    'Triglycerides'       => ['unit' => 'mg/dL',      'min' => 0.0,  'max' => 150.0],
    'VLDL'                => ['unit' => 'mg/dL',      'min' => 2.0,  'max' => 30.0],
    'Non_HDL'             => ['unit' => 'mg/dL',      'min' => 0.0,  'max' => 130.0],
];
@endphp

{{-- Top Bar --}}
<div class="d-flex justify-content-between align-items-center mb-3">
    <a href="/" class="btn btn-outline-secondary btn-sm">
        ← Back to Dashboard
    </a>
    <button onclick="window.print()" class="btn btn-sm text-white fw-bold"
            style="background: linear-gradient(135deg, #1F4E79, #2E75B6);
                   border-radius:8px; padding: 8px 18px;">
        <i class="fas fa-print me-1"></i> Print Report
    </button>
</div>

{{-- Report Info Card --}}
<div class="card mb-4">
    <div class="card-header fw-bold d-flex align-items-center gap-2"
         style="background-color: #1F4E79; color: white;">
        <i class="fas fa-file-medical"></i>
        Report Details — {{ $report->doc_id }}
    </div>
    <div class="card-body">
        <div class="row g-3">
            <div class="col-md-6">
                <table class="table table-borderless mb-0">
                    <tr>
                        <th width="40%" class="text-muted" style="font-size:13px;">Patient Name</th>
                        <td>
                            @if($report->patient_name == 'NOT_FOUND')
                                <span class="badge" style="background-color:#adb5bd;">Not Found</span>
                            @else
                                {{ $report->patient_name }}
                            @endif
                        </td>
                    </tr>
                    <tr>
                        <th class="text-muted" style="font-size:13px;">Gender</th>
                        <td>
                            @if($report->patient_gender == 'NOT_FOUND')
                                <span class="badge" style="background-color:#adb5bd;">Not Found</span>
                            @else
                                {{ $report->patient_gender }}
                            @endif
                        </td>
                    </tr>
                    <tr>
                        <th class="text-muted" style="font-size:13px;">Test Date</th>
                        <td>
                            @if($report->test_date == 'NOT_FOUND')
                                <span class="badge" style="background-color:#adb5bd;">Not Found</span>
                            @else
                                {{ $report->test_date }}
                            @endif
                        </td>
                    </tr>
                </table>
            </div>
            <div class="col-md-6">
                <table class="table table-borderless mb-0">
                    <tr>
                        <th width="40%" class="text-muted" style="font-size:13px;">Test Type</th>
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
                    </tr>
                    <tr>
                        <th class="text-muted" style="font-size:13px;">Lab Name</th>
                        <td>
                            @if(!$report->lab_name || $report->lab_name == 'NOT_FOUND')
                                <span class="badge" style="background-color:#adb5bd;">Not Found</span>
                            @else
                                {{ $report->lab_name }}
                            @endif
                        </td>
                    </tr>
                    <tr>
                        <th class="text-muted" style="font-size:13px;">Source</th>
                        <td>{{ $report->source_type }}</td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</div>

{{-- Medical Values Card --}}
<div class="card">
    <div class="card-header fw-bold d-flex align-items-center gap-2"
         style="background-color: #2E75B6; color: white;">
        <i class="fas fa-flask"></i>
        Extracted Medical Values
        <small class="ms-2 opacity-75" style="font-size:11px;">
            * Reference ranges based on standard adult values (WHO / NHS guidelines)
        </small>
    </div>
    <div class="card-body">
        @if($report->medicalValues->count() > 0)
        <div class="row">
            @foreach($report->medicalValues as $value)
            @php
                $info   = $paramInfo[$value->param_name] ?? null;
                $unit   = $info['unit'] ?? '';
                $numVal = is_numeric($value->param_value) ? (float)$value->param_value : null;
                $status = null;
                if ($numVal !== null && $info) {
                    if ($numVal < $info['min'])      $status = 'low';
                    elseif ($numVal > $info['max'])  $status = 'high';
                    else                             $status = 'normal';
                }
            @endphp
            <div class="col-md-4 mb-3">
                @if($value->param_value == 'NOT_FOUND')
                {{-- NOT FOUND card --}}
                <div class="card text-center p-3 h-100"
                     style="border-left: 4px solid #adb5bd;">
                    <small class="text-muted mb-1">{{ $value->param_name }}</small>
                    <span class="badge mx-auto mt-1"
                          style="background-color:#adb5bd; width:fit-content;">
                        Not Found
                    </span>
                    @if($info)
                    <small class="text-muted mt-2" style="font-size:10px;">
                        Normal: {{ $info['min'] }}–{{ $info['max'] }} {{ $unit }}
                    </small>
                    @endif
                </div>
                @else
                {{-- Value card --}}
                @php
                    $borderColor = $status == 'high' ? '#dc3545'
                                 : ($status == 'low'  ? '#fd7e14'
                                 : '#198754');
                    $valColor    = $status == 'high' ? 'text-danger'
                                 : ($status == 'low'  ? 'text-warning'
                                 : 'text-success');
                @endphp
                <div class="card text-center p-3 h-100"
                     style="border-left: 4px solid {{ $borderColor }};">
                    <small class="text-muted mb-1">{{ $value->param_name }}</small>
                    <h5 class="{{ $valColor }} mt-1 mb-0">
                        {{ $value->param_value }}
                        @if($unit)
                            <small class="text-muted" style="font-size:11px;">{{ $unit }}</small>
                        @endif
                    </h5>
                    @if($status)
                    <div class="mt-1">
                        @if($status == 'high')
                            <span class="badge bg-danger" style="font-size:10px;">HIGH ↑</span>
                        @elseif($status == 'low')
                            <span class="badge bg-warning text-dark" style="font-size:10px;">LOW ↓</span>
                        @else
                            <span class="badge bg-success" style="font-size:10px;">Normal ✓</span>
                        @endif
                    </div>
                    @endif
                    @if($info)
                    <small class="text-muted mt-1" style="font-size:10px;">
                        Range: {{ $info['min'] }}–{{ $info['max'] }} {{ $unit }}
                    </small>
                    @endif
                </div>
                @endif
            </div>
            @endforeach
        </div>
        @else
            <div class="text-center py-4">
                <i class="fas fa-flask fa-2x mb-2" style="color:#ccc;"></i>
                <p class="text-muted">No medical values extracted.</p>
            </div>
        @endif
    </div>
</div>

<style>
@media print {
    .navbar, .btn, a.btn { display: none !important; }
    .card { box-shadow: none !important; }
}
</style>

@endsection