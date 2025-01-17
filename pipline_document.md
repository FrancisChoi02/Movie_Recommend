### **Data Preprocessing**

This module is responsible for:

1. Importing data from the data source (CSV) into the database (SQLite).
2. Cleaning the data in the database into an agreed-upon format, removing erroneous data, and preparing it for matrix construction.

### **Matrix Data Processing Module**

This module is responsible for:

1. **Building the Task Map (Classification)**:
    - Classifying tasks into predefined categories.
2. **Building Inverted Dictionaries**:
    - **user_item_dict**: Stores users' task completion data as vectors (e.g., user: [1, 0, 1, 2, 1, 3]).
    - **item_user_dict**: Tracks which users have completed specific tasks.
3. **Constructing Matrices**:
    - **user_task_vectorized_matrix**:
        - Records each user's score for every task.
        - Initial scores are based on the number of times a user has completed a particular type of task (e.g., user 1: {‘task 1’: 1}, {‘task 2’: 0}, {‘task 3’: 0}, {‘task 4’: 2}, {‘task 5’: 0}).
    - **maker_similarity_matrix**:
        - Vectorizes each user's task data using **user_item_dict** and calculates user similarity through cosine similarity, constructing a similarity matrix.
4. **Reading and Writing Matrix Data**:
    - Handles the storage and retrieval of matrix data.

### **User Collaborative Filtering**

This module is responsible for:

1. Updating the **user_task_vectorized_matrix** based on user-to-user similarity. Scores for tasks are updated using collaborative filtering (e.g., user 1: {‘task 1’: 1}, {‘task 2’: 1.22}, {‘task 3’: 0.98}, {‘task 4’: 4}, {‘task 5’: 3}).
2. Processing test dataset data to validate the effectiveness of the algorithm.

### **Recommendation**

This module is responsible for:

1. Recommending the most suitable and available candidate for a specific task.
2. Executing scheduled tasks to trigger **User Collaborative Filtering** updates based on new task data, ensuring up-to-date recommendation results.
