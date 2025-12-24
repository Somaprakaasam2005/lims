-- Sample data for testing LIMS (MySQL)
USE lims_db;

INSERT INTO users (username, password_hash, role) VALUES
('admin', '-sha256$...examplehash', 'Admin');

INSERT INTO samples (sample_id, sample_type, project_name, client_name, date_collected) VALUES
('C-2025-0001', 'Concrete', 'Library Extension', 'City Council', '2025-12-01'),
('S-2025-0001', 'Soil', 'Roadworks A', 'Highway Dept', '2025-11-20');

INSERT INTO test_results (sample_id, test_name, raw_values, date_tested) VALUES
(1, 'Compressive Strength', '250.0,19600', NOW()),
(2, 'Sieve Analysis', '75:10;37.5:20;19:30;9.5:25;4.75:10;total:95', NOW());
