# Auto Work Assignment System PoC

## Overview

The Auto Task Assignment System is a task recommendation system based on collaborative filtering algorithms. It aims to recommend the most suitable executors for specific tasks by analyzing task complexity and type. By leveraging historical task records and user-task interaction data, the system generates intelligent recommendation lists to improve the efficiency and accuracy of task assignment.

## Table of Contents

- Installation
- Usage
- Modules
    - Data Import
    - Data Preprocessing
    - Matrix Related
    - Recommendation
    - Evaluation

## Installation

1. Create a virtual environment using **venv** for dependency management(Windows):
    
    ```bash
    python3 -m pip install venv
    python3 -m venv myenv
    myenv\Scripts\activate
    ```
    
2. Install the required packages:
    
    ```bash
    pip install -r requirements.txt
    ```
    
3. Ensure you have the necessary Excel files in the `static` directory for sqliteDB initialization:
    - `Sample_Permission.xlsx`
    - `Sample_Task.xlsx`
4. Ensure you have the `.pkl` matrix files in the da/evaluation_matrix for evaluation:
    - `eva_user_similarity_matrix.pkl`
    - `eva_user_task_vectorized_matrix.pkl`
    - `updated_eva_user_task_vectorized_matrix.pkl`

## Usage

To run the data import scripts, execute the following commands at the project root directory:

```bash
python data_import.py
```

To format the SQLite data to meet the matrix-building requirements, run: 

```bash
	python data_preprocessing.py
```

To test the user recommendation effect for a certain task, run:

```bash
	python recommend_test.py
```

To evaluate the impact of User Collaborative Filtering on recommendation effectiveness, run:

```bash
	python evaluation.py
```

To start the API for maker recommendation based on a exact task, run:

```bash
python app.py
```

## Modules

### Data Import

- **`data_import.py`**: Imports user permissions and task data from Excel files into the SQLite database.

### Data Processing

- **`data_preprocessing.py`**: Processes user task data to update scores based on user similarities. It loads user task vectors and similarity matrices, then updates the task scores for users based on the weighted contributions of similar users.

### Matrix Related

- **`service/simalarity_matrix_construction.py`**: Responsible for constructing similarity matrices based on user task data. It includes functions to vectorize user data, create user similarity matrices, and manage task classification mappings.

### Recommendation

- **`recommend.py`**: Provides functionality for recommending users based on task scores. It includes methods to retrieve task indices based on complexity and type, and to generate a list of recommended users sorted by their scores for specific tasks.

### Evaluation

- **`evaluation.py`**: Contains functions to calculate metrics such as precision, recall, and F1 score for evaluating recommendations.

# Auto Task Assignment System

## OverView

The Auto Task Assignment System is a task recommendation system based on collaborative filtering algorithms. It aims to recommend the most suitable executors for specific tasks by analyzing task complexity and type. By leveraging historical task records and user-task interaction data, the system generates intelligent recommendation lists to improve the efficiency and accuracy of task assignment.

## Table of Contents

- Project Structure
- Module
- API Endpoints
- Testing
- Quick Start

## Project Structure

```markdown
src/
├── main/
│   ├── java/
│   │   └── com/recommend/
│   │       ├── controller/        # API Controllers
│   │       │   
│   │       ├── config/            # Configuration
│   │       │   
│   │       ├── dao/               # Data Access Layer
│   │       │   
│   │       ├── domain/            # Data Models
│   │       │   
│   │       ├── service/           # API Controllers
│   │       │   
│   │       └── util/              # Tool
│   │ 
│   └──  resources/                # Configuration file
│ 
└── test/                          
		└── java/com/recommend/
				└── service/               # Unit Tests
```

## Module

The system consists of the following core components:

1. **Task Classification Service** (TaskClassificationService)
    - Manages task type and classification mapping
    - Dynamically loads task classification information
2. **Similarity Matrix Service** (SimilarityMatrixService)
    - Creates user similarity matrix
    - Generates user-task vectorized matrix
    - Manages task index data
3. **Collaborative Filtering Service** (UserCollaborativeFilteringService)
    - Implements user-based collaborative filtering algorithm
    - Updates task ratings dynamically
    - Matrix data persistence
4. **Recommendation Service** (TaskRecommendationService)
    - Recommends suitable users based on task complexity and type
    - Calculates task discrete index

## API Endpoints

### Get Recommended Users for Task

```bash
GET /api/recommend/users?complexity={complexity}&taskType={taskType}
```

Parameters:

- `complexity`: Task complexity (Low/Medium/High)
- `taskType`: Task type (e.g., FL)

Response Example:

```json
[
	{
		"maker_name": "user1",
		"score": 3
	},
	{
		"maker_name": "user2",
		"score": 1.4
	}
]
```

## Test

- Run Unit Test

```bash
mvn test -Dtest={TESTCLASS} -Dsurefire.useFile=false
```

Change the `{TESTCLASS}` to the name of the test java class

## Quick Start

1. Configure database

Ensure SQLite database file exists in the correct location in both main and test folder.

2. Build the project

```bash
mvn clean package
```

3. Run the application

```bash
java -jar target/{FILENAME}-1.0-SNAPSHOT.jar

or

mvn spring-boot:run
```

```ok
package com.recommend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.recommend.service.TaskRecommendationService;

import java.util.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/recommend")
public class RecommendationController {
    
    @Autowired
    private TaskRecommendationService taskRecommendationService;
    
    @GetMapping("/users")
    public List<Map<String, Object>> getRecommendedUsers(
            @RequestParam String complexity,
            @RequestParam String taskType) {
        return taskRecommendationService.recommendUsersForTask(complexity, taskType)
            .stream()
            .map(entry -> {
                Map<String, Object> result = new HashMap<>();
                result.put("userId", entry.getKey());
                result.put("score", entry.getValue());
                return result;
            })
            .collect(Collectors.toList());
    }
}

```

```ok
package com.recommend.dto;

public class UserRecommendationDTO {
    private String maker_name;
    private Double score;

    public Double getScore() {
        return score;
    }

    public void setScore(Double score) {
        this.score = score;
    }

    public String getMaker_name() {
        return maker_name;
    }

    public void setMaker_name(String maker_name) {
        this.maker_name = maker_name;
    }
}

```

- Application

```ok
package com.recommend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling 
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

```

- Service

```ok
package com.recommend.service.scheduler;

import com.recommend.service.SimilarityMatrixService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class MatrixUpdateScheduler {
    
    @Autowired
    private SimilarityMatrixService similarityMatrixService;
    
    
    //private static final String USER_TASK_MATRIX_PATH = "./src/main/java/com/recommend/dao/original_user_task_vectorized_matrix.ser";
    //private static final String USER_SIMILARITY_MATRIX_PATH = "./src/main/java/com/recommend/dao/original_user_similarity_matrix.ser"
    private static final String MATRIX_UPDATE_PATH = "./data/updated_user_task_vectorized_matrix.ser";
    private static final String SIMILARITY_UPDATE_PATH = "./data/updated_user_similarity_matrix.ser";
    
    // 每20小时执行一次
    @Scheduled(fixedRate = 20 * 60 * 60 * 1000)
    public void updateMatrix() {
        log.info("Starting scheduled matrix update...");
        try {
            var taskData = similarityMatrixService.getTaskIndexData();
            similarityMatrixService.createUserSimilarityMatrix(
                taskData, 
                MATRIX_UPDATE_PATH, 
                SIMILARITY_UPDATE_PATH
            );
            log.info("Matrix update completed successfully");
        } catch (Exception e) {
            log.error("Failed to update matrix", e);
        }
    }
}
```

```ok
import org.hibernate.dialect.Dialect;
import org.hibernate.dialect.function.StandardSQLFunction;
import org.hibernate.dialect.function.SQLFunctionTemplate;
import org.hibernate.dialect.function.NoArgSQLFunction;
import org.hibernate.type.StringType;

public class SQLiteDialect extends Dialect {
    public SQLiteDialect() {
        super();
        registerColumnType(java.sql.Types.BIT, "integer");
        registerColumnType(java.sql.Types.TINYINT, "tinyint");
        registerColumnType(java.sql.Types.SMALLINT, "smallint");
        registerColumnType(java.sql.Types.INTEGER, "integer");
        registerColumnType(java.sql.Types.BIGINT, "bigint");
        registerColumnType(java.sql.Types.FLOAT, "float");
        registerColumnType(java.sql.Types.REAL, "real");
        registerColumnType(java.sql.Types.DOUBLE, "double");
        registerColumnType(java.sql.Types.NUMERIC, "numeric");
        registerColumnType(java.sql.Types.DECIMAL, "decimal");
        registerColumnType(java.sql.Types.CHAR, "char");
        registerColumnType(java.sql.Types.VARCHAR, "varchar");
        registerColumnType(java.sql.Types.LONGVARCHAR, "longvarchar");
        registerColumnType(java.sql.Types.DATE, "date");
        registerColumnType(java.sql.Types.TIME, "time");
        registerColumnType(java.sql.Types.TIMESTAMP, "timestamp");
        registerColumnType(java.sql.Types.BINARY, "blob");
        registerColumnType(java.sql.Types.VARBINARY, "blob");
        registerColumnType(java.sql.Types.LONGVARBINARY, "blob");
        registerColumnType(java.sql.Types.BLOB, "blob");
        registerColumnType(java.sql.Types.CLOB, "clob");
        registerColumnType(java.sql.Types.BOOLEAN, "integer");

        // Functions
        registerFunction("concat", new SQLFunctionTemplate(StringType.INSTANCE, "?1 || ?2"));
        registerFunction("mod", new SQLFunctionTemplate(StringType.INSTANCE, "?1 % ?2"));
        registerFunction("substr", new StandardSQLFunction("substr", StringType.INSTANCE));
        registerFunction("substring", new StandardSQLFunction("substr", StringType.INSTANCE));
    }

    public boolean supportsIdentityColumns() {
        return true;
    }

    public boolean hasDataTypeInIdentityColumn() {
        return false; // As per SQLite specification
    }

    public String getIdentityColumnString() {
        return "integer";
    }

    public String getIdentitySelectString() {
        return "select last_insert_rowid()";
    }

    public boolean supportsLimit() {
        return true;
    }

    public String getLimitString(String query, boolean hasOffset) {
        return query + (hasOffset ? " limit ? offset ?" : " limit ?");
    }

    public boolean supportsTemporaryTables() {
        return true;
    }

    public String getCreateTemporaryTableString() {
        return "create temporary table if not exists";
    }

    public boolean dropTemporaryTableAfterUse() {
        return false;
    }

    public boolean supportsCurrentTimestampSelection() {
        return true;
    }

    public boolean isCurrentTimestampSelectStringCallable() {
        return false;
    }

    public String getCurrentTimestampSelectString() {
        return "select current_timestamp";
    }

    public boolean supportsUnionAll() {
        return true;
    }

    public boolean hasAlterTable() {
        return false;
    }

    public boolean dropConstraints() {
        return false;
    }

    public String getAddColumnString() {
        return "add column";
    }

    public String getForUpdateString() {
        return "";
    }

    public boolean supportsOuterJoinForUpdate() {
        return false;
    }

    public String getDropForeignKeyString() {
        throw new UnsupportedOperationException("No drop foreign key syntax supported by SQLiteDialect");
    }

    public String getAddForeignKeyConstraintString(String constraintName, String[] foreignKey, String referencedTable, String[] primaryKey, boolean referencesPrimaryKey) {
        throw new UnsupportedOperationException("No add foreign key syntax supported by SQLiteDialect");
    }

    public String getAddPrimaryKeyConstraintString(String constraintName) {
        throw new UnsupportedOperationException("No add primary key syntax supported by SQLiteDialect");
    }

    public boolean supportsIfExistsBeforeTableName() {
        return true;
    }

    public boolean supportsCascadeDelete() {
        return false;
    }
}

```