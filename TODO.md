# Consent Form Implementation

## Overview

This document outlines the steps to implement a consent form with "I Agree" and "I don't Agree" buttons, and a database to store user consent.

## Database Schema

The consent database should store the following fields:

- `user_id` (integer): Unique identifier for the user.
- `consent` (boolean): Indicates whether the user has consented (`true` for agree, `false` for disagree).
- `timestamp` (datetime): Records the time when the consent was given or denied.

### Example SQLite Table Creation

```sql
CREATE TABLE user_consent (
    user_id INTEGER PRIMARY KEY,
    consent BOOLEAN NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Implementation Steps

### 1. Set Up the Database

Create a SQLite database (or any other database of your choice) with a table to store consent information. Use the schema provided above.

### 2. Modify the Consent Command

Update the `/consent` command to save the user's consent to the database when they agree. If they do not agree, handle it accordingly (e.g., not recording their voice). You can also add a command to check if a user has consented.

#### Example Code for Handling Consent

```python
import sqlite3
from datetime import datetime

def save_consent(user_id, consent):
    conn = sqlite3.connect('consent.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_consent (user_id, consent, timestamp)
        VALUES (?, ?, ?)
    ''', (user_id, consent, datetime.now()))
    conn.commit()
    conn.close()

def check_consent(user_id):
    conn = sqlite3.connect('consent.db')
    cursor = conn.cursor()
    cursor.execute('SELECT consent FROM user_consent WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
```

### 3. Check Consent Before Recording

Before recording a user's voice, check the database to ensure they have consented. If they have not, do not record their voice.

#### Example Code for Checking Consent

```python
def record_voice(user_id):
    consent = check_consent(user_id)
    if consent:
        # Proceed with recording
        print("Recording voice...")
    else:
        print("User has not consented. Recording aborted.")
```

## Consent Form UI

The consent form should have two buttons: "I Agree" and "I Disagree". When a user clicks one of the buttons, their choice should be saved to the database.

### Example HTML for Consent Form

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Consent Form</title>
  </head>
  <body>
    <h1>Consent Form</h1>
    <p>Do you agree to the terms and conditions?</p>
    <button id="agree">I Agree</button>
    <button id="disagree">I Disagree</button>

    <script>
      document.getElementById("agree").addEventListener("click", function () {
        saveConsent(true);
      });

      document.getElementById("disagree").addEventListener("click", function () {
        saveConsent(false);
      });

      function saveConsent(consent) {
        // Send the consent choice to the server
        fetch("/save_consent", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ consent: consent }),
        })
          .then((response) => response.json())
          .then((data) => {
            console.log("Consent saved:", data);
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      }
    </script>
  </body>
</html>
```

## Conclusion

By following these steps, you can implement a consent form with "I Agree" and "I Disagree" buttons, and store the user's consent in a database. This ensures that you only record user data when they have explicitly agreed to it.
