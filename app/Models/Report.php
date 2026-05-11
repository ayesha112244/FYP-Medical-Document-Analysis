<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Report extends Model
{
    protected $table = 'reports';
    public $timestamps = false;

    protected $fillable = [
        'user_id',
        'doc_id',
        'patient_name',
        'patient_gender',
        'test_date',
        'test_type',
        'lab_name',
        'source_type',
        'file_type',
        'file_path',
    ];

    // Relationship: Report has many MedicalValues
    public function medicalValues()
    {
        return $this->hasMany(MedicalValue::class, 'report_id');
    }

    // Relationship: Report belongs to User
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}