-- Create database and tables for WhatsApp Microlearning Coach

CREATE DATABASE IF NOT EXISTS microlearning_coach;
USE microlearning_coach;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100),
    preferred_language VARCHAR(10) DEFAULT 'en',
    subscription_status ENUM('free', 'daily', 'weekly', 'premium') DEFAULT 'free',
    subscription_start DATE,
    subscription_end DATE,
    current_streak INT DEFAULT 0,
    total_lessons_completed INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Lesson categories
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Lessons table
CREATE TABLE lessons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    difficulty_level ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner',
    estimated_duration INT DEFAULT 5, -- in minutes
    lesson_order INT,
    media_url VARCHAR(500),
    quiz_questions JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- User progress tracking
CREATE TABLE user_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    lesson_id INT,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quiz_score INT,
    time_spent INT, -- in seconds
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (lesson_id) REFERENCES lessons(id),
    UNIQUE KEY unique_user_lesson (user_id, lesson_id)
);

-- Subscriptions table
CREATE TABLE subscriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    plan_type ENUM('daily', 'weekly', 'monthly') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    payment_status ENUM('pending', 'completed', 'failed', 'cancelled') DEFAULT 'pending',
    payment_id VARCHAR(100),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Certificates and badges
CREATE TABLE certificates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    category_id INT,
    certificate_type ENUM('completion', 'mastery', 'streak') NOT NULL,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    certificate_url VARCHAR(500),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Message logs for WhatsApp interactions
CREATE TABLE message_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message_type ENUM('incoming', 'outgoing') NOT NULL,
    message_content TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert sample categories
INSERT INTO categories (name, description, icon) VALUES
('English Language', 'Improve your English speaking, writing, and comprehension skills', '🇬🇧'),
('Digital Skills', 'Learn essential computer and internet skills for the modern workplace', '💻'),
('Vocational Training', 'Practical skills for various trades and professions', '🔧'),
('Business Skills', 'Entrepreneurship, marketing, and business management', '💼'),
('Financial Literacy', 'Money management, budgeting, and investment basics', '💰');

-- Insert sample lessons for English Language
INSERT INTO lessons (category_id, title, content, difficulty_level, lesson_order, quiz_questions) VALUES
(1, 'Basic Greetings', 'Learn essential greetings in English:\n\n• Hello / Hi - Casual greeting\n• Good morning - Before 12 PM\n• Good afternoon - 12 PM to 6 PM\n• Good evening - After 6 PM\n\nPractice: Use these greetings with 3 different people today!', 'beginner', 1, 
'[{"question": "What greeting do you use after 6 PM?", "options": ["Good morning", "Good afternoon", "Good evening", "Hello"], "correct": 2}]'),

(1, 'Introducing Yourself', 'Master self-introductions:\n\n• "My name is..." or "I am..."\n• "I am from [country/city]"\n• "I work as a [job]" or "I am a student"\n• "Nice to meet you"\n\nExample: "Hi, my name is Sarah. I am from Lagos and I work as a teacher. Nice to meet you!"', 'beginner', 2,
'[{"question": "Complete: My name ___ John", "options": ["am", "is", "are", "be"], "correct": 1}]');

-- Insert sample lessons for Digital Skills
INSERT INTO lessons (category_id, title, content, difficulty_level, lesson_order, quiz_questions) VALUES
(2, 'Email Basics', 'Master professional email communication:\n\n• Subject line: Clear and specific\n• Greeting: Dear [Name] or Hello [Name]\n• Body: Keep it concise and clear\n• Closing: Best regards, Thank you\n• Signature: Your name and contact\n\nTip: Always proofread before sending!', 'beginner', 1,
'[{"question": "What should you always do before sending an email?", "options": ["Add emoji", "Proofread", "Use caps", "Make it long"], "correct": 1}]'),

(2, 'Internet Safety', 'Stay safe online:\n\n• Use strong passwords (8+ characters, mix of letters, numbers, symbols)\n• Never share personal info with strangers\n• Verify websites before entering details\n• Keep software updated\n• Be cautious with public WiFi\n\nRemember: If something seems too good to be true, it probably is!', 'beginner', 2,
'[{"question": "A strong password should have at least how many characters?", "options": ["4", "6", "8", "10"], "correct": 2}]');
