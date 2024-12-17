-- Create table for Users
CREATE TABLE Users (
    userID SERIAL PRIMARY KEY,
    lastName VARCHAR(255),
    firstName VARCHAR(255),
    middleName VARCHAR(255),
    suffix VARCHAR(10),
    street VARCHAR(255),
    city VARCHAR(255),
    province VARCHAR(255),
    contactNo VARCHAR(15),
    emailAddress VARCHAR(255) UNIQUE,
    facebookLink VARCHAR(255),
    instagramLink VARCHAR(255),
    birthDate DATE,
    incomeSource VARCHAR(255),
    dwellingType VARCHAR(100),
    dwellingOwn BOOLEAN,
    petsAllowed BOOLEAN,
    password VARCHAR(255),
    accountType VARCHAR(10) CHECK (accountType IN ('user', 'admin')) DEFAULT 'user'
);

-- Create the Rescue table
CREATE TABLE Rescue (
    rescueID SERIAL PRIMARY KEY,
    rescueName VARCHAR(255),
    category VARCHAR(100),
    gender VARCHAR(10),
    age INTEGER,
    breed VARCHAR(100),
    medCondition TEXT,
    description TEXT,
    rescueStatus VARCHAR(100),
    adoptedTo INTEGER REFERENCES Users(userID),
    rescuePic VARCHAR(255)
);

-- Create the Application table
CREATE TABLE Application (
    applicationID SERIAL PRIMARY KEY,
    userID INTEGER REFERENCES Users(userID),
    householdNo INTEGER,
    householdSupport VARCHAR(255),
    rescueID INTEGER REFERENCES Rescue(rescueID),
    ownershipExperience TEXT,
    vetCheck BOOLEAN,
    petsCaredList TEXT,
    petsCaredStatus TEXT,
    foundPawssion VARCHAR(255),
    whyAdopt TEXT,
    interviewDate DATE,
    interviewTime TIME,
    approval BOOLEAN,
    adoptedTo INTEGER REFERENCES Users(userID)
);

-- Create the Adoption table
CREATE TABLE Adoption (
    adoptionID SERIAL PRIMARY KEY,
    userID INTEGER REFERENCES Users(userID),
    rescueID INTEGER REFERENCES Rescue(rescueID),
    applicationID INTEGER REFERENCES Application(applicationID)
);

-- Optional: Insert demo data here

-- Insert demo data for Users table
INSERT INTO Users (lastName, firstName, middleName, suffix, street, city, province, contactNo, emailAddress, facebookLink, instagramLink, birthDate, incomeSource, dwellingType, dwellingOwn, petsAllowed, password, accountType)
VALUES
('Smith', 'John', 'A', 'Jr.', '123 Maple St.', 'Springfield', 'Illinois', '123-456-7890', 'john.smith@example.com', 'facebook.com/johnsmith', 'instagram.com/johnsmith', '1985-07-15', 'Software Engineer', 'Apartment', TRUE, TRUE, 'password123', 'admin'),
('Doe', 'Jane', 'B', NULL, '456 Oak Ave.', 'Greenville', 'Texas', '987-654-3210', 'jane.doe@example.com', 'facebook.com/janedoe', 'instagram.com/janedoe', '1990-04-22', 'Teacher', 'House', TRUE, TRUE, 'securepassword', 'user'),
('Johnson', 'Emily', 'C', NULL, '789 Pine Blvd.', 'Fairview', 'California', '555-123-4567', 'emily.j@example.com', 'facebook.com/emilyjohnson', NULL, '1992-12-05', 'Freelancer', 'Apartment', FALSE, FALSE, 'mypassword456', 'user');

-- Insert demo data for Rescue table
INSERT INTO Rescue (rescueName, category, gender, age, breed, medCondition, description, rescueStatus, adoptedTo, rescuePic)
VALUES
('Buddy', 'Dog', 'Male', 3, 'Golden Retriever', 'None', 'Friendly and energetic dog.', 'Available', NULL, 'https://images.aeonmedia.co/images/acd6897d-9849-4188-92c6-79dabcbcd518/essay-final-gettyimages-685469924.jpg?width=3840&quality=75&format=auto'),
('Mittens', 'Cat', 'Female', 2, 'Siamese', 'None', 'Affectionate and loves cuddles.', 'Available', NULL, 'https://i.natgeofe.com/n/4cebbf38-5df4-4ed0-864a-4ebeb64d33a4/NationalGeographic_1468962.jpg?w=2880&h=2120'),
('Charlie', 'Dog', 'Male', 5, 'Labrador', 'Arthritis', 'Calm and gentle, great with kids.', 'Adopted', 1, 'https://hips.hearstapps.com/hmg-prod/images/yorkshire-terrier-dog-sitting-close-up-on-nature-royalty-free-image-1682308117.jpg?crop=0.70029xw:1xh;center,top&resize=980:*'),
('Luna', 'Cat', 'Female', 1, 'Persian', 'None', 'Playful and curious kitten.', 'Available', NULL, 'https://www.newsnationnow.com/wp-content/uploads/sites/108/2022/07/Cat.jpg?w=2560&h=1440&crop=1'),
('Malik', 'Dog', 'Male', 3, 'Golden Retriever', 'None', 'Friendly and energetic dog.', 'Available', NULL, 'https://spca.bc.ca/wp-content/uploads/2023/06/happy-samoyed-dog-outdoors-in-summer-field.jpg'),
('Epsi', 'Cat', 'Female', 2, 'Siamese', 'None', 'Affectionate and loves cuddles.', 'Available', NULL, 'https://i.natgeofe.com/n/9135ca87-0115-4a22-8caf-d1bdef97a814/75552.jpg'),
('Scout', 'Dog', 'Male', 5, 'Labrador', 'Arthritis', 'Calm and gentle, great with kids.', 'Adopted', 1, 'https://www.milofoundation.org/wp-content/uploads/2024/09/20240928130759.jpg'),
('Boni', 'Cat', 'Female', 1, 'Persian', 'None', 'Playful and curious kitten.', 'Available', NULL, 'https://www.vetmed.wisc.edu/wp-content/uploads/2022/12/lina-angelov-Ah_QC2v2alE-unsplash-1200x960.jpg');

-- Insert demo data for Application table
INSERT INTO Application (userID, householdNo, householdSupport, rescueID, ownershipExperience, vetCheck, petsCaredList, petsCaredStatus, foundPawssion, whyAdopt, interviewDate, interviewTime, approval, adoptedTo)
VALUES
(1, 4, 'Supportive', 1, 'Previously owned a Labrador.', TRUE, 'Labrador', 'Healthy', 'Social Media', 'Looking for a companion.', '2024-01-15', '10:00:00', TRUE, 1),
(2, 3, 'Neutral', 2, 'Owned a cat before.', TRUE, 'Siamese', 'Healthy', 'Friend Recommendation', 'Want to provide a loving home.', '2024-02-15', '14:00:00', FALSE, NULL);

-- Insert demo data for Adoption table
INSERT INTO Adoption (userID, rescueID, applicationID)
VALUES
(1, 3, 1);
