package com.recommend.service;

import com.recommend.dao.impl.FileMatrixDataSource;
import com.recommend.dao.impl.SerializationDataSource;
import com.recommend.dao.impl.SqliteTaskDataSource;

import com.recommend.service.impl.TaskRecommendationServiceImpl;
import com.recommend.service.impl.UserCollaborativeFilteringImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.jdbc.core.JdbcTemplate;

import org.springframework.jdbc.datasource.DriverManagerDataSource;

import java.io.File;
import java.lang.reflect.Method;
import java.util.*;
// import java.util.Map;
// import java.util.Set;


import static org.junit.jupiter.api.Assertions.*;

import com.recommend.model.*;

import com.recommend.service.impl.SimilarityMatrixServiceImpl;
import org.springframework.test.util.ReflectionTestUtils;

public class TaskDataSourceTest {

    @Mock
    private JdbcTemplate jdbcTemplate;

    @InjectMocks
    private SqliteTaskDataSource taskDataSource;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        // 设置连接到测试数据库
        String testDbPath = "src/test/java/com/recommend/dao/test_db.sqlite"; // 替换为实际路径
        jdbcTemplate = new JdbcTemplate(new DriverManagerDataSource("jdbc:sqlite:" + testDbPath));
        taskDataSource = new SqliteTaskDataSource(jdbcTemplate);
    }

    @Test
    void testDatabaseConnection() {
        // 测试数据库连接是否成功
        try {
            jdbcTemplate.execute("SELECT 1");
        } catch (Exception e) {
            throw new AssertionError("数据库连接失败: " + e.getMessage());
        }
    }

    @Test
    void testFindTaskByName() {
        String sql = "SELECT task_name, complexity, task_type, maker FROM task_data WHERE task_name = ?";
        List<TaskData> result = jdbcTemplate.query(sql,
            (rs, rowNum) -> TaskData.builder()
                .taskName(rs.getString("task_name"))
                .complexity(rs.getString("complexity"))
                .taskType(rs.getString("task_type"))
                .maker(rs.getString("maker"))
                .build(),
            "TASK-8218");

        TaskData expectedTask = TaskData.builder()
            .taskName("TASK-8218")
            .complexity("Low")
            .taskType("FL") 
            .maker("Lavender")
            .build();
        
        if (!result.isEmpty()) {
            System.out.println("Found task: " + result.get(0).getTaskName());
        } else {
            System.out.println("Task not found");
        }

        // Verify we got a result and it matches expected
        assertEquals(1, result.size());
        assertEquals(expectedTask.getTaskName(), result.get(0).getTaskName());
        assertEquals(expectedTask.getComplexity(), result.get(0).getComplexity());
        assertEquals(expectedTask.getTaskType(), result.get(0).getTaskType());
        assertEquals(expectedTask.getMaker(), result.get(0).getMaker());
    }




    
    // 读取Sqlite
    @Test
    void testGetAllTasks() {
        List<TaskData> tasks = taskDataSource.getAllTasks();
        
        // Print all tasks
        System.out.println("All tasks in database:");
        tasks.forEach(task -> {
            System.out.printf("Task: %s, Complexity: %s, Type: %s, Maker: %s%n",
                task.getTaskName(),
                task.getComplexity(), 
                task.getTaskType(),
                task.getMaker()
            );
        });

        // Verify we got some results
        assertFalse(tasks.isEmpty(), "Task list should not be empty");
        
        // Verify task objects have required fields populated
        tasks.forEach(task -> {
            assertNotNull(task.getTaskName(), "Task name should not be null");
            assertNotNull(task.getComplexity(), "Complexity should not be null"); 
            assertNotNull(task.getTaskType(), "Task type should not be null");
            assertNotNull(task.getMaker(), "Maker should not be null");
        });
    }





    // private record TaskInfo(String complexity, String taskType) {}
    // private record TaskIndexData(
    //         Map<String, Map<String, TaskInfo>> makerInvertedIndex,
    //         Map<String, Map<String, Integer>> userTaskCounts,
    //         Map<String, Set<String>> itemInvertIndex,
    //         Map<String, String> taskClassifications
    // ) {}

    // // 获取从Sqlite中读取数据并构建 TaskData
    // @Test
    // void testGetTaskIndexData() {

    //     // Get access to private method using reflection
    //     Method getTaskIndexDataMethod;
    //     try {
    //         getTaskIndexDataMethod = SimilarityMatrixServiceImpl.class.getDeclaredMethod("getTaskIndexData");
    //         getTaskIndexDataMethod.setAccessible(true);

    //         // Get instance of service and invoke method
    //         SimilarityMatrixServiceImpl service = new SimilarityMatrixServiceImpl();
    //         ReflectionTestUtils.setField(service, "taskDataSource", taskDataSource);
            
    //         var taskIndexData = (TaskIndexData)getTaskIndexDataMethod.invoke(service);

    //         // Print maker inverted index
    //         System.out.println("\nMaker Inverted Index:");
    //         taskIndexData.makerInvertedIndex().forEach((maker, taskMap) -> {
    //             System.out.println("Maker: " + maker);
    //             taskMap.forEach((taskName, taskInfo) -> {
    //                 System.out.printf("\tTask: %s, Complexity: %s, Type: %s%n",
    //                     taskName, taskInfo.complexity(), taskInfo.taskType());
    //             });
    //         });

    //         // Print task classifications
    //         System.out.println("\nTask Classifications:");
    //         taskIndexData.taskClassifications().forEach((key, value) -> {
    //             System.out.printf("%s -> %s%n", key, value);
    //         });

    //         // Print user task counts
    //         System.out.println("\nUser Task Counts:");
    //         taskIndexData.userTaskCounts().forEach((user, counts) -> {
    //             System.out.println("User: " + user);
    //             counts.forEach((taskClass, count) -> {
    //                 System.out.printf("\t%s: %d%n", taskClass, count);
    //             });
    //         });

    //         // Print item invert index
    //         System.out.println("\nItem Invert Index:");
    //         taskIndexData.itemInvertIndex().forEach((taskClass, users) -> {
    //             System.out.printf("%s -> %s%n", taskClass, users);
    //         });

    //         // Verify data structure integrity
    //         assertNotNull(taskIndexData.makerInvertedIndex());
    //         assertNotNull(taskIndexData.taskClassifications());
    //         assertNotNull(taskIndexData.userTaskCounts());
    //         assertNotNull(taskIndexData.itemInvertIndex());
            
    //         assertFalse(taskIndexData.makerInvertedIndex().isEmpty());
    //         assertFalse(taskIndexData.taskClassifications().isEmpty());
    //         assertFalse(taskIndexData.userTaskCounts().isEmpty());
    //         assertFalse(taskIndexData.itemInvertIndex().isEmpty());

    //     } catch (Exception e) {
    //         fail("Failed to test getTaskIndexData: " + e.getMessage());
    //     }
    // }

    // // 创建Matrix并保存
    // @Test
    // void testCreateAndSaveSimilarityMatrix() {
    //     try {
    //         // Get the private method using reflection
    //         Method getTaskIndexDataMethod = SimilarityMatrixServiceImpl.class
    //             .getDeclaredMethod("getTaskIndexData");
    //         getTaskIndexDataMethod.setAccessible(true);

    //         // Create service instance and get task index data
    //         SimilarityMatrixServiceImpl service = new SimilarityMatrixServiceImpl();
    //         service.taskDataSource = taskDataSource;
    //         service.matrixDataSource = new FileMatrixDataSource();
            
    //         var taskIndexData = (TaskIndexData)getTaskIndexDataMethod.invoke(service);


    //         // Print user task counts
    //         System.out.println("\nUser Task Counts:");
    //         taskIndexData.userTaskCounts().forEach((user, counts) -> {
    //             System.out.println("User: " + user);
    //             counts.forEach((taskClass, count) -> {
    //                 System.out.printf("\t%s: %d%n", taskClass, count);
    //             });
    //         });

    //         // Create and configure FileMatrixDataSource with SerializationDataSource
    //         FileMatrixDataSource matrixDataSource = new FileMatrixDataSource();
    //         SerializationDataSource<Map<String, double[]>> userTaskDataSource = new SerializationDataSource<>();
    //         SerializationDataSource<Map<String, Map<String, Double>>> similarityDataSource = new SerializationDataSource<>();
    //         ReflectionTestUtils.setField(matrixDataSource, "userTaskDataSource", userTaskDataSource);
    //         ReflectionTestUtils.setField(matrixDataSource, "similarityDataSource", similarityDataSource);
    //         service.matrixDataSource = matrixDataSource;

    //         // Create user task vectorized matrix
    //         Map<String, double[]> userTaskMatrix = 
    //             service.createUserTaskVectorizedMatrix(taskIndexData);

    //         // Print user task vectorized matrix
    //         System.out.println("\nUser Task Vectorized Matrix:");
    //         userTaskMatrix.forEach((user, vector) -> {
    //             System.out.println("User: " + user);
    //             System.out.println("\tVector: " + Arrays.toString(vector));
    //         });

    //         // Verify user task matrix is not empty
    //         assertNotNull(userTaskMatrix);
    //         assertFalse(userTaskMatrix.isEmpty());

    //         // Create similarity matrix
    //         Map<String, Map<String, Double>> similarityMatrix = 
    //             service.createUserSimilarityMatrix(taskIndexData);

    //         // Print similarity matrix
    //         System.out.println("\nUser Similarity Matrix:");
    //         similarityMatrix.forEach((user1, similarities) -> {
    //             System.out.println("User: " + user1);
    //             similarities.forEach((user2, similarity) -> {
    //                 System.out.printf("\t%s: %.4f%n", user2, similarity);
    //             });
    //         });

    //         // Verify similarity matrix is not empty
    //         assertNotNull(similarityMatrix);
    //         assertFalse(similarityMatrix.isEmpty());

    //         // Verify files exist
    //         File userTaskFile = new File("./src/main/java/com/recommend/dao/original_user_task_vectorized_matrix.ser");
    //         File similarityFile = new File("./src/main/java/com/recommend/dao/original_user_similarity_matrix.ser");
            
    //         assertTrue(userTaskFile.exists(), "User task matrix file should exist");
    //         assertTrue(similarityFile.exists(), "Similarity matrix file should exist");

    //     } catch (Exception e) {
    //         fail("Failed to test similarity matrix creation: " + e.getMessage());
    //     }
    // }

    // @Test
    // void testLoadMatrixFromFile() {
    //     try {
    //         // Create and configure FileMatrixDataSource with SerializationDataSource
    //         FileMatrixDataSource matrixDataSource = new FileMatrixDataSource();
    //         SerializationDataSource<Map<String, double[]>> userTaskDataSource = new SerializationDataSource<>();
    //         SerializationDataSource<Map<String, Map<String, Double>>> similarityDataSource = new SerializationDataSource<>();
    //         ReflectionTestUtils.setField(matrixDataSource, "userTaskDataSource", userTaskDataSource);
    //         ReflectionTestUtils.setField(matrixDataSource, "similarityDataSource", similarityDataSource);

    //         // Load matrices from files
    //         Map<String, double[]> userTaskMatrix = matrixDataSource.loadUserTaskMatrix();
    //         Map<String, Map<String, Double>> similarityMatrix = matrixDataSource.loadUserSimilarityMatrix();

    //         // Print loaded user task matrix
    //         System.out.println("\nLoaded User Task Matrix:");
    //         userTaskMatrix.forEach((user, vector) -> {
    //             System.out.println("User: " + user);
    //             System.out.println("\tVector: " + Arrays.toString(vector));
    //         });

    //         // Print loaded similarity matrix  
    //         System.out.println("\nLoaded User Similarity Matrix:");
    //         similarityMatrix.forEach((user1, similarities) -> {
    //             System.out.println("User: " + user1);
    //             similarities.forEach((user2, similarity) -> {
    //                 System.out.printf("\t%s: %.4f%n", user2, similarity);
    //             });
    //         });

    //         // Verify matrices are not empty
    //         assertNotNull(userTaskMatrix);
    //         assertFalse(userTaskMatrix.isEmpty());
    //         assertNotNull(similarityMatrix); 
    //         assertFalse(similarityMatrix.isEmpty());

    //     } catch (Exception e) {
    //         fail("Failed to load matrices from files: " + e.getMessage());
    //     }
    // }


    // // UF更新Matrix
    // @Test
    // void testUpdateUserTaskMatrix() {
    //     try {
    //         // Create and configure FileMatrixDataSource with SerializationDataSource
    //         FileMatrixDataSource matrixDataSource = new FileMatrixDataSource();
    //         SerializationDataSource<Map<String, double[]>> userTaskDataSource = new SerializationDataSource<>();
    //         SerializationDataSource<Map<String, Map<String, Double>>> similarityDataSource = new SerializationDataSource<>();
    //         ReflectionTestUtils.setField(matrixDataSource, "userTaskDataSource", userTaskDataSource);
    //         ReflectionTestUtils.setField(matrixDataSource, "similarityDataSource", similarityDataSource);

    //         // Create and configure UserCollaborativeFiltering service
    //         UserCollaborativeFilteringService userCollaborativeFiltering = new UserCollaborativeFilteringImpl(matrixDataSource);

    //         // Update task scores which will:
    //         // 1. Load matrices from files
    //         // 2. Update scores
    //         // 3. Save updated matrix back to file
    //         userCollaborativeFiltering.updateTaskScores();

    //         // Get the updated matrix
    //         Map<String, double[]> updatedMatrix = userCollaborativeFiltering.getUserTaskVectorizedMatrix();

    //         // Print updated matrix
    //         System.out.println("\nUpdated User Task Matrix:");
    //         updatedMatrix.forEach((user, vector) -> {
    //             System.out.println("User: " + user);
    //             System.out.println("\tVector: " + Arrays.toString(vector));
    //         });

    //         // Verify matrix is not empty
    //         assertNotNull(updatedMatrix);
    //         assertFalse(updatedMatrix.isEmpty());

    //         // Verify each user has a non-empty vector
    //         updatedMatrix.forEach((user, vector) -> {
    //             assertNotNull(vector);
    //             assertTrue(vector.length > 0);
    //         });

    //     } catch (Exception e) {
    //         fail("Failed to update user task matrix: " + e.getMessage());
    //     }
    // }


    // 根据一个具体的Task，获得推荐结果（推荐前五个人，）
    @Test
    void testRecommendUsersForTask() {
        try {
            // Get task classifications from TaskIndexData
            SimilarityMatrixServiceImpl similarityMatrixService = new SimilarityMatrixServiceImpl();
            ReflectionTestUtils.setField(similarityMatrixService, "taskDataSource", taskDataSource);
            TaskIndexData taskIndexData = similarityMatrixService.getTaskIndexData();
            Map<String, String> taskClassifications = taskIndexData.taskClassifications();

            // Initialize TaskRecommendationService with classifications
            TaskRecommendationService recommendationService = new TaskRecommendationServiceImpl(taskClassifications);

            // Configure matrix data source
            FileMatrixDataSource matrixDataSource = new FileMatrixDataSource();
            SerializationDataSource<Map<String, double[]>> userTaskDataSource = new SerializationDataSource<>();
            SerializationDataSource<Map<String, Map<String, Double>>> similarityDataSource = new SerializationDataSource<>();
            ReflectionTestUtils.setField(matrixDataSource, "userTaskDataSource", userTaskDataSource);
            ReflectionTestUtils.setField(matrixDataSource, "similarityDataSource", similarityDataSource);

            // Configure and set UserCollaborativeFilteringService
            UserCollaborativeFilteringService userCollaborativeFiltering = new UserCollaborativeFilteringImpl(matrixDataSource);
            
            // Load matrices before using the service
            userCollaborativeFiltering.updateTaskScores();
            
            ReflectionTestUtils.setField(recommendationService, "userCollaborativeFilteringService", userCollaborativeFiltering);

            // Test recommendation for a specific task
            String complexity = "Medium";
            String taskType = "FL";
            List<Map.Entry<String, Double>> recommendations = recommendationService.recommendUsersForTask(complexity, taskType);

            // Verify and print recommendations
            assertNotNull(recommendations);
            // assertTrue(recommendations.size() <= 5);

            System.out.println("\nRecommended users for " + complexity + " " + taskType + " task:");
            recommendations.stream()
                .limit(9)
                .forEach(entry -> System.out.printf("User: %s, Score: %.2f%n", entry.getKey(), entry.getValue()));

        } catch (Exception e) {
            fail("Failed to get task recommendations: " + e.getMessage());
        }
    }

}