<script setup>
import { ref } from 'vue'
import { Users, Plus, TrendingUp, UserCheck, GraduationCap, Calendar } from 'lucide-vue-next'

const selectedClass = ref(null)
const showCreateModal = ref(false)

const classes = ref([
  { 
    id: 1, 
    name: 'Class 1A', 
    grade: 'Grade 1', 
    students: 28,
    teacher: 'Mrs. Johnson',
    subjects: 8,
    avgAttendance: 95
  },
  { 
    id: 2, 
    name: 'Class 1B', 
    grade: 'Grade 1', 
    students: 30,
    teacher: 'Mr. Smith',
    subjects: 8,
    avgAttendance: 92
  },
  { 
    id: 3, 
    name: 'Class 2A', 
    grade: 'Grade 2', 
    students: 27,
    teacher: 'Ms. Davis',
    subjects: 9,
    avgAttendance: 97
  }
])

const students = ref([
  { id: 1, name: 'Alice Wang', studentId: 'S001', attendance: 98, grade: 'A', status: 'active' },
  { id: 2, name: 'Bob Chen', studentId: 'S002', attendance: 95, grade: 'A-', status: 'active' },
  { id: 3, name: 'Carol Liu', studentId: 'S003', attendance: 92, grade: 'B+', status: 'active' },
  { id: 4, name: 'David Zhang', studentId: 'S004', attendance: 88, grade: 'B', status: 'active' },
  { id: 5, name: 'Emma Li', studentId: 'S005', attendance: 100, grade: 'A+', status: 'active' }
])

const viewClassDetails = (classItem) => {
  selectedClass.value = classItem
}
</script>

<template>
  <div class="class-mgmt-container">
    <div class="page-header">
      <div>
        <h1>Class Management</h1>
        <p>Manage classes and students</p>
      </div>
      <button @click="showCreateModal = true" class="create-btn">
        <Plus :size="20" />
        Add New Class
      </button>
    </div>

    <!-- Class Grid -->
    <div class="classes-grid">
      <div v-for="classItem in classes" :key="classItem.id" class="class-card">
        <div class="class-header">
          <div class="class-icon">
            <GraduationCap :size="24" />
          </div>
          <div class="class-info">
            <h3>{{ classItem.name }}</h3>
            <span class="grade-badge">{{ classItem.grade }}</span>
          </div>
        </div>

        <div class="class-stats">
          <div class="stat-item">
            <Users :size="18" class="stat-icon" />
            <div>
              <span class="stat-label">Students</span>
              <span class="stat-value">{{ classItem.students }}</span>
            </div>
          </div>

          <div class="stat-item">
            <UserCheck :size="18" class="stat-icon" />
            <div>
              <span class="stat-label">Attendance</span>
              <span class="stat-value">{{ classItem.avgAttendance }}%</span>
            </div>
          </div>
        </div>

        <div class="class-footer">
          <div class="teacher-info">
            <span class="teacher-label">Teacher:</span>
            <span class="teacher-name">{{ classItem.teacher }}</span>
          </div>
          <button @click="viewClassDetails(classItem)" class="view-btn">
            View Details
          </button>
        </div>
      </div>
    </div>

    <!-- Student List Section -->
    <div v-if="selectedClass" class="students-section">
      <div class="section-header">
        <h2>{{ selectedClass.name }} - Student Roster</h2>
        <button class="add-student-btn">
          <Plus :size="18" />
          Add Student
        </button>
      </div>

      <div class="students-table-container">
        <table class="students-table">
          <thead>
            <tr>
              <th>Student ID</th>
              <th>Name</th>
              <th>Attendance</th>
              <th>Grade</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in students" :key="student.id">
              <td>{{ student.studentId }}</td>
              <td class="student-name">{{ student.name }}</td>
              <td>
                <div class="attendance-cell">
                  <span>{{ student.attendance }}%</span>
                  <div class="attendance-bar">
                    <div class="attendance-fill" :style="{ width: `${student.attendance}%` }"></div>
                  </div>
                </div>
              </td>
              <td><span class="grade-badge">{{ student.grade }}</span></td>
              <td><span class="status-badge active">{{ student.status }}</span></td>
              <td>
                <div class="table-actions">
                  <button class="icon-btn">Edit</button>
                  <button class="icon-btn danger">Remove</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click="showCreateModal = false">
      <div class="modal-content" @click.stop>
        <h2>Create New Class</h2>
        <p class="modal-message">Class creation form will be implemented here.</p>
        <button @click="showCreateModal = false" class="close-btn">Close</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.class-mgmt-container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 0.5rem;
}

.page-header p {
  color: var(--text-muted);
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: var(--primary);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 600;
  transition: all 0.2s;
}

.create-btn:hover {
  background-color: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.classes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.class-card {
  background: var(--bg-surface);
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid var(--border-color);
  transition: all 0.2s;
}

.class-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.class-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.class-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--primary) 0%, #059669 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.class-info h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 0.25rem;
}

.grade-badge {
  background-color: #e0f2fe;
  color: #0284c7;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.class-stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: var(--bg-body);
  border-radius: 0.75rem;
}

.stat-item {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.stat-icon {
  color: var(--primary);
}

.stat-label {
  display: block;
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-bottom: 0.125rem;
}

.stat-value {
  display: block;
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--text-main);
}

.class-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.teacher-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.teacher-label {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.teacher-name {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--text-main);
}

.view-btn {
  padding: 0.625rem 1.25rem;
  background-color: var(--primary);
  color: white;
  border-radius: 0.5rem;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.view-btn:hover {
  background-color: var(--primary-hover);
}

.students-section {
  background: var(--bg-surface);
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid var(--border-color);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.section-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-main);
}

.add-student-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: transparent;
  color: var(--primary);
  border: 1px solid var(--primary);
  border-radius: 0.5rem;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.add-student-btn:hover {
  background-color: var(--primary);
  color: white;
}

.students-table-container {
  overflow-x: auto;
}

.students-table {
  width: 100%;
  border-collapse: collapse;
}

.students-table thead {
  background-color: var(--bg-body);
}

.students-table th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-main);
  border-bottom: 2px solid var(--border-color);
}

.students-table td {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  font-size: 0.9375rem;
}

.student-name {
  font-weight: 500;
  color: var(--text-main);
}

.attendance-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.attendance-bar {
  flex: 1;
  height: 6px;
  background-color: #e5e7eb;
  border-radius: 999px;
  overflow: hidden;
  max-width: 80px;
}

.attendance-fill {
  height: 100%;
  background-color: var(--primary);
  border-radius: 999px;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-badge.active {
  background-color: #dcfce7;
  color: #16a34a;
}

.table-actions {
  display: flex;
  gap: 0.5rem;
}

.icon-btn {
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.8125rem;
  font-weight: 500;
  background-color: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border-color);
  transition: all 0.2s;
}

.icon-btn:hover {
  background-color: var(--bg-body);
  color: var(--text-main);
}

.icon-btn.danger {
  color: #ef4444;
  border-color: #ef4444;
}

.icon-btn.danger:hover {
  background-color: #fef2f2;
  color: #dc2626;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--bg-surface);
  padding: 2rem;
  border-radius: 1rem;
  max-width: 500px;
  width: 90%;
}

.modal-content h2 {
  margin-bottom: 1rem;
  color: var(--text-main);
}

.modal-message {
  color: var(--text-muted);
  margin-bottom: 1.5rem;
}

.close-btn {
  background-color: var(--primary);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
}
</style>
