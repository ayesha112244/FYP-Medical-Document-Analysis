<?php

namespace App\Http\Controllers;

use App\Models\Report;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class ReportController extends Controller
{
    // Dashboard
    public function index(Request $request)
    {
        $user  = Auth::user();
        $query = $request->input('search', '');
        $type  = $request->input('type', '');

        $builder = $user->isAdmin()
            ? Report::query()
            : Report::where('user_id', $user->id);

        if ($query) {
            $builder->where(function($q) use ($query) {
                $q->where('patient_name', 'like', "%{$query}%")
                ->orWhere('doc_id',       'like', "%{$query}%")
                ->orWhere('test_type',    'like', "%{$query}%");
            });
        }

        if ($type) {
            $builder->where('test_type', $type);
        }

        $reports    = $builder->orderBy('uploaded_at', 'desc')->paginate(10)->withQueryString();
        $allReports = $user->isAdmin()
            ? Report::all()
            : Report::where('user_id', $user->id)->get();

        return view('dashboard', compact('reports', 'user', 'allReports', 'query', 'type'));
    }

    // Report Detail
    public function show($id)
    {
        $user   = Auth::user();
        $report = Report::with('medicalValues')->findOrFail($id);

        if (!$user->isAdmin() && $report->user_id !== $user->id) {
            abort(403, 'Unauthorized');
        }

        return view('report-detail', compact('report'));
    }

    // Delete Report
    public function destroy($id)
    {
        $user   = Auth::user();
        $report = Report::findOrFail($id);

        if (!$user->isAdmin() && $report->user_id !== $user->id) {
            abort(403, 'Unauthorized');
        }

        // Delete medical values first, then report
        $report->medicalValues()->delete();
        $report->delete();

        return redirect('/')->with('success', 'Report deleted successfully.');
    }
}