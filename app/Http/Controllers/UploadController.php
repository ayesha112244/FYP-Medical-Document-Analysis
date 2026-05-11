<?php

namespace App\Http\Controllers;

use App\Models\Report;
use App\Models\MedicalValue;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Http;

class UploadController extends Controller
{
    // Show Upload Form
    public function showUpload()
    {
        return view('upload');
    }

    // Handle Upload
    public function processUpload(Request $request)
    {
        // Step 1: Validate file
        $request->validate([
            'report_file'   => 'required|file|mimes:pdf,png,jpg,jpeg|max:10240',
            'selected_type' => 'required|in:CBC,LFT,RFT,BSG,Lipid,Other',
        ]);

        $selectedType = $request->input('selected_type');

        $file     = $request->file('report_file');
        $ext      = strtolower($file->getClientOriginalExtension());
        $filename = pathinfo($file->getClientOriginalName(), PATHINFO_FILENAME);
        $doc_id   = preg_replace('/[^a-zA-Z0-9_-]/', '_', $filename);

        // Step 2: Send file to FastAPI
        $fastapiUrl = env('FASTAPI_URL', 'http://127.0.0.1:8001');

        try {
            $response = Http::timeout(120)
                ->attach(
                    'file',
                    file_get_contents($file->getRealPath()),
                    $doc_id . '.' . $ext
                )
                ->post($fastapiUrl . '/extract', [
                    'doc_id'        => $doc_id,
                    'selected_type' => $selectedType,
                ]);
                
        } catch (\Exception $e) {
            return back()->with('error',
                'Could not connect to extraction service. 
                 Please ensure the API server is running. 
                 Error: ' . $e->getMessage());
        }

        // Step 3: Check response
        if (!$response->successful()) {
            $body = $response->json();
            return back()->with('error',
                'Extraction failed: ' . ($body['error'] ?? 'Unknown error'));
        }

        $result = $response->json();
        $data   = $result['data'] ?? [];

        if (empty($data)) {
            return back()->with('error', 'No data extracted from file.');
        }

        // Step 4: Determine file type
        if ($ext === 'jpg' || $ext === 'jpeg') {
            $fileType = 'JPEG';
        } elseif ($ext === 'png') {
            $fileType = 'PNG';
        } else {
            $fileType = 'PDF';
        }

        // Step 5: Save to database — use user-selected type, not pipeline's
        $report = Report::create([
            'user_id'        => Auth::id(),
            'doc_id'         => $data['doc_id']         ?? $doc_id,
            'patient_name'   => $data['patient_name']   ?? 'NOT_FOUND',
            'patient_gender' => $data['patient_gender'] ?? 'NOT_FOUND',
            'test_date'      => $data['test_date']      ?? 'NOT_FOUND',
            'test_type'      => $selectedType,
            'lab_name'       => $data['lab_name']       ?? 'NOT_FOUND',
            'source_type'    => 'user_upload',
            'file_type'      => $fileType,
            'file_path'      => $file->getClientOriginalName(),
        ]);

        // Step 6: Save medical values
        $medicalValues = $data['medical_values'] ?? [];

        // If "Other" type and no values detected → show friendly message
        if ($selectedType === 'Other' && empty($medicalValues)) {
            $report->medicalValues()->delete();
            $report->delete();
            return back()->with('error',
                'This report type is not yet supported by the system. ' .
                'No medical values could be extracted. ' .
                'Currently supported types are: CBC, LFT, RFT, BSG, and Lipid Profile.');
        }

        foreach ($medicalValues as $paramName => $paramValue) {
            MedicalValue::create([
                'report_id'   => $report->id,
                'param_name'  => $paramName,
                'param_value' => (string) $paramValue,
            ]);
        }

        // Success message based on type
        if ($selectedType === 'Other') {
            $successMsg = 'Report uploaded. Some values may have been extracted but full support for this type is not available yet.';
        } else {
            $successMsg = "Report uploaded and extracted successfully!";
        }

        return redirect('/')->with('success', $successMsg);
    }
}