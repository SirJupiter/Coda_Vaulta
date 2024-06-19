-- Create User table
CREATE TABLE User (
  user_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password_hash CHAR(60) NOT NULL,
  email VARCHAR(255) UNIQUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create Snippet table
CREATE TABLE Snippet (
  snippet_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  code TEXT NOT NULL,
  user_id INT UNSIGNED NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  privacy ENUM('public', 'private') NOT NULL DEFAULT 'private',
  FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- -- Create Tag table
-- CREATE TABLE Tag (
--   tag_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
--   name VARCHAR(50) NOT NULL UNIQUE
-- );

-- -- Create Snippet_Tag table (many-to-many relationship)
-- CREATE TABLE Snippet_Tag (
--   snippet_id INT UNSIGNED NOT NULL,
--   tag_id INT UNSIGNED NOT NULL,
--   FOREIGN KEY (snippet_id) REFERENCES Snippet(snippet_id),
--   FOREIGN KEY (tag_id) REFERENCES Tag(tag_id),
--   PRIMARY KEY (snippet_id, tag_id)
-- );
