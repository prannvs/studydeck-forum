# StudyDeck Forum

StudyDeck forum is a comprehensive academic discussion platform built with Django. It allows students to create threads linked to specific courses, engage in discussions via replies, interact with likes, and report inappropriate content. The platform includes robust moderation tools and a tagging system for efficient content discovery.

## 🚀 Setup Instructions

Follow these steps to get the project running on your local machine.

### 1. Prerequisites
* Python 3.10 or higher
* Git

### 2. Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd studydeck
    ```

2.  **Create a Virtual Environment:**
    * *Windows:*
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * *Mac/Linux:*
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Dependencies:**
    ```bash
    pip install django psycopg2-binary django-allauth bootstrap5
    # Or if you have a requirements.txt:
    # pip install -r requirements.txt
    ```

4.  **Database Setup:**
    Run the migrations to create the database tables (Threads, Replies, Reports, Tags, etc.):
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create an Admin Account (For Moderation):**
    You need a superuser account to access the Reporting System and Admin Panel.
    ```bash
    python manage.py createsuperuser
    ```
    *(Follow the prompts to set a username and password)*

6.  **Run the Server:**
    ```bash
    python manage.py runserver
    ```
    Open your browser and visit: `http://127.0.0.1:8000/`

---

## 📖 Feature Walkthrough

### For Students
1.  **Creating Threads:**
    * Click **"+ New Thread"** on the home page.
    * **Contextual Linking:** Select a **Course** (e.g., "CS F111") from the dropdown to link your question to a subject.
    * **Tagging:** Select tags like `#Urgent` or `#Midsem` to categorize your post.
2.  **Interactivity:**
    * **Likes:** Click the Heart icon on any thread or reply to upvote it. The counter updates instantly.
    * **Replies:** Open a thread to post replies. You can format your text using the provided text area.
3.  **Navigation:**
    * **Pagination:** The home page shows 10 threads per page. Use "Next" and "Previous" buttons to navigate.
    * **Sorting:** Use the "Sort By" dropdown to view Newest or Oldest discussions.

### For Moderators
1.  **Managing Content:**
    * **Locking:** Moderators can click the "Three Dots" menu on a thread to **Lock** it, preventing further replies.
    * **Deleting:** Moderators can delete any thread or reply that violates rules.
2.  **Reporting System:**
    * Users can report threads via the "Report Content" option in the thread menu.
    * Moderators access the **Admin Panel** (`/admin`) to view the **Reports** section.
    * Filter reports by "Pending" status and mark them as "Resolved" after taking action.

---

## 🧠 Design Decisions

This section explains the architectural choices made during development.

### 1. Database Structure
* **Contextual Linking (`Course` ForeignKey):**
    * *Decision:* Instead of just using text tags for courses, we created a distinct `Course` model linked via a ForeignKey.
    * *Reason:* This ensures data consistency (preventing typos like "CS F111" vs "csf111") and allows for future scalability, such as adding course-specific resource pages.
* **Tagging System (`ManyToMany` Field):**
    * *Decision:* We used a Many-to-Many relationship for Tags (e.g., `#Help`, `#Exam`).
    * *Reason:* This allows a single thread to have multiple tags, and a single tag to be associated with multiple threads, making filtering efficient and flexible.

### 2. Data Integrity & Moderation
* **Soft Deletion for Replies:**
    * *Decision:* The `Reply` model includes an `is_deleted` boolean field.
    * *Reason:* When a user deletes a reply, we don't remove the row from the database. Instead, we hide it from the UI. This preserves the conversation context and maintains an audit trail for moderators.
* **Reporting Workflow:**
    * *Decision:* A separate `Report` model tracks the `reporter`, `thread`, `reason`, and `status`.
    * *Reason:* This decouples the reporting logic from the content itself. It allows multiple users to report the same thread without conflict and gives moderators a clear "To-Do" list via the Status field (Pending vs. Resolved).

### 3. User Experience (UX)
* **Slugs for URLs:**
    * *Decision:* We use `slugs` (e.g., `/thread/how-to-study/`) instead of IDs (`/thread/15/`).
    * *Reason:* This improves SEO and makes links human-readable and shareable.
* **Bootstrap Integration:**
    * *Decision:* The frontend uses Bootstrap 5.
    * *Reason:* Ensures a responsive, mobile-friendly design without writing complex custom CSS, speeding up development.