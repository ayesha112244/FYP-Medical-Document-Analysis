-- Schema for the fyp_medical database
-- The users table is created by Laravel's migrations (php artisan migrate).

CREATE TABLE IF NOT EXISTS reports (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         BIGINT UNSIGNED NULL,
    doc_id          VARCHAR(255) NOT NULL,
    patient_name    VARCHAR(255) NULL,
    patient_gender  VARCHAR(50)  NULL,
    test_date       VARCHAR(100) NULL,
    test_type       VARCHAR(50)  NULL,
    lab_name        VARCHAR(255) NULL,
    source_type     VARCHAR(100) NULL,
    file_type       VARCHAR(20)  NULL,
    file_path       VARCHAR(500) NULL,
    uploaded_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS medical_values (
    id           BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    report_id    BIGINT UNSIGNED NOT NULL,
    param_name   VARCHAR(100) NOT NULL,
    param_value  VARCHAR(100) NULL,
    CONSTRAINT fk_medical_values_report
        FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
);
