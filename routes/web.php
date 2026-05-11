<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\ReportController;
use App\Http\Controllers\UploadController;

// Auth Routes
Route::get('/login',    [AuthController::class, 'showLogin'])->name('login');
Route::post('/login',   [AuthController::class, 'login']);
Route::get('/register', [AuthController::class, 'showRegister'])->name('register');
Route::post('/register',[AuthController::class, 'register']);
Route::post('/logout',  [AuthController::class, 'logout'])->name('logout');

// Protected Routes
Route::middleware('auth')->group(function () {
    Route::get('/',              [ReportController::class, 'index']);
    Route::get('/report/{id}',   [ReportController::class, 'show']);
    Route::get('/upload',        [UploadController::class, 'showUpload']);
    Route::post('/upload',       [UploadController::class, 'processUpload']);
    Route::delete('/report/{id}', [ReportController::class, 'destroy']);
});