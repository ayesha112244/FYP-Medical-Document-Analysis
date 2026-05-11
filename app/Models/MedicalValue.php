<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class MedicalValue extends Model
{
    protected $table = 'medical_values';

    public $timestamps = false;

    protected $fillable = [
        'report_id',
        'param_name',
        'param_value',
    ];

    // Relationship: MedicalValue belongs to Report
    public function report()
    {
        return $this->belongsTo(Report::class);
    }
}