<script setup>
import { ref, computed, onMounted } from 'vue'
import { Users, Plus, UserCheck, GraduationCap, Edit, Trash2 } from 'lucide-vue-next'
import {
  getClasses,
  getClassStudents,
  addStudentToClass,
  updateStudentInClass,
  removeStudentFromClass,
  updateStudentGrades,
  createClass,
  updateClass,
  deleteClass,
  getUsers
} from '../api/classes.js'
import { useAuthStore } from '../stores/auth.js'

const classes = ref([])
const students = ref([])
const selectedClass = ref(null)
const isLoading = ref(false)
const error = ref('')

const auth = useAuthStore()
const isAdmin = auth.isAdmin

// 模态框状态
const showCreateClassModal = ref(false)
const teachers = ref([])
const showAddStudentModal = ref(false)
const showEditStudentModal = ref(false)
const editingStudent = ref(null)

// 班级编辑/删除
const showEditClassModal = ref(false)
const editingClass = ref(null)
const isUpdatingClass = ref(false)
const isDeletingClass = ref(false)
const editClassForm = ref({ name: '', grade: '', teacher_id: null })

const openEditClassModal = async (classItem) => {
  editingClass.value = classItem
  editClassForm.value = {
    name: classItem.name,
    grade: classItem.grade,
    teacher_id: classItem.teacher?.id || null
  }
  error.value = ''
  showEditClassModal.value = true
  if (auth.isAdmin) {
    await loadTeachers()
  }
}

const handleUpdateClass = async () => {
  if (!editingClass.value) return
  if (!editClassForm.value.name || !editClassForm.value.grade) {
    error.value = 'Class name and grade are required'
    return
  }
  isUpdatingClass.value = true
  error.value = ''
  try {
    const payload = {
      name: editClassForm.value.name.trim(),
      grade: editClassForm.value.grade
    }
    if (auth.isAdmin) {
      payload.teacher_id = editClassForm.value.teacher_id || null
    }
    await updateClass(editingClass.value.id, payload)
    await loadClasses()
    // 如果当前选择的班级被编辑，更新selectedClass引用
    const updated = classes.value.find(c => c.id === editingClass.value.id)
    if (updated && selectedClass.value && selectedClass.value.id === updated.id) {
      selectedClass.value = updated
    }
    showEditClassModal.value = false
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to update class'
  } finally {
    isUpdatingClass.value = false
  }
}

const handleDeleteClass = async (classItem) => {
  if (!confirm(`Delete class "${classItem.name}"? This cannot be undone.`)) return
  isDeletingClass.value = true
  error.value = ''
  try {
    await deleteClass(classItem.id)
    if (selectedClass.value && selectedClass.value.id === classItem.id) {
      selectedClass.value = null
      students.value = []
    }
    await loadClasses()
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to delete class'
  } finally {
    isDeletingClass.value = false
  }
}


// 表单数据
const newClass = ref({
  name: '',
  grade: '',
  teacher_id: null
})

const isCreatingClass = ref(false)

const loadTeachers = async () => {
  try {
    const list = await getUsers('teacher')
    teachers.value = Array.isArray(list) ? list : []
  } catch (e) {
    console.warn('Failed to load teachers', e)
    teachers.value = []
  }
}

const openCreateClassModal = async () => {
  newClass.value = { name: '', grade: '', teacher_id: null }
  error.value = ''
  showCreateClassModal.value = true
  if (auth.isAdmin) {
    await loadTeachers()
  }
}

const handleCreateClass = async () => {
  if (!newClass.value.name || !newClass.value.grade) {
    error.value = 'Class name and grade are required'
    return
  }
  isCreatingClass.value = true
  error.value = ''
  try {
    await createClass({
      name: newClass.value.name.trim(),
      grade: newClass.value.grade,
      teacher_id: newClass.value.teacher_id || null
    })
    await loadClasses()
    showCreateClassModal.value = false
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to create class'
  } finally {
    isCreatingClass.value = false
  }
}


const newStudent = ref({
  full_name: '',
  username: '',
  email: '',
  student_no: '',
  attendance_rate: 0,
  status: 'active',
  grades: {
    chinese: null,
    math: null,
    english: null
  }
})

const editStudentForm = ref({
  full_name: '',
  email: '',
  student_no: '',
  attendance_rate: 0,
  status: 'active',
  grades: {
    chinese: null,
    math: null,
    english: null
  }
})

// 加载班级列表
const loadClasses = async () => {
  isLoading.value = true
  error.value = ''
  try {
    const data = await getClasses()
    classes.value = data.map(cls => ({
      ...cls,
      students: cls.students_count || 0,
      avgAttendance: cls.avg_attendance || 0,
      teacher: cls.teacher?.full_name || 'Unassigned'
    }))
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load classes'
    console.error('Error loading classes:', err)
  } finally {
    isLoading.value = false
  }
}

// 加载学生列表
const loadStudents = async (classId) => {
  if (!classId) return
  isLoading.value = true
  error.value = ''
  try {
    const data = await getClassStudents(classId)
    students.value = data
      .map(s => ({
        ...s,
        studentId: s.student_no || `S${String(s.id).padStart(3, '0')}`,
        name: s.full_name,
        attendance: s.attendance_rate || 0,
        grade: s.avg_grade,
        grades: s.grades || {},
        averageScore: s.grades?.average ?? s.avg_grade
      }))
      .sort((a, b) => (a.studentId || '').localeCompare(b.studentId || ''))
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load students'
    console.error('Error loading students:', err)
  } finally {
    isLoading.value = false
  }
}

// 查看班级详情
const viewClassDetails = async (classItem) => {
  selectedClass.value = classItem
  await loadStudents(classItem.id)
}

// 打开添加学生模态框
const openAddStudentModal = async () => {
  if (!selectedClass.value) return
  newStudent.value = {
    full_name: '',
    username: '',
    email: '',
    student_no: '',
    attendance_rate: 0,
    status: 'active',
    grades: {
      chinese: null,
      math: null,
      english: null
    }
  }
  showAddStudentModal.value = true
}

// 添加学生
const handleAddStudent = async () => {
  if (!newStudent.value.full_name || !newStudent.value.student_no) {
    error.value = 'Full name and student number are required'
    return
  }

  isLoading.value = true
  error.value = ''
  try {
    await addStudentToClass(selectedClass.value.id, {
      full_name: newStudent.value.full_name.trim(),
      username: newStudent.value.username?.trim() || undefined,
      email: newStudent.value.email?.trim() || undefined,
      student_no: newStudent.value.student_no.trim(),
      attendance_rate: newStudent.value.attendance_rate || 0,
      status: newStudent.value.status || 'active',
      grades: {
        chinese: newStudent.value.grades.chinese,
        math: newStudent.value.grades.math,
        english: newStudent.value.grades.english
      }
    })
    await loadStudents(selectedClass.value.id)
    await loadClasses() // 更新班级学生数
    showAddStudentModal.value = false
    newStudent.value = {
      full_name: '',
      username: '',
      email: '',
      student_no: '',
      attendance_rate: 0,
      status: 'active',
      grades: {
        chinese: null,
        math: null,
        english: null
      }
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to add student'
  } finally {
    isLoading.value = false
  }
}

// 打开编辑学生模态框
const openEditStudentModal = async (student) => {
  editingStudent.value = student
  editStudentForm.value = {
    full_name: student.full_name,
    email: student.email || '',
    student_no: student.student_no || '',
    attendance_rate: student.attendance_rate || 0,
    status: student.status || 'active',
    grades: {
      chinese: student.grades?.chinese || null,
      math: student.grades?.math || null,
      english: student.grades?.english || null
    }
  }
  showEditStudentModal.value = true
}

// 更新学生信息
const handleUpdateStudent = async () => {
  if (!editingStudent.value) return

  isLoading.value = true
  error.value = ''
  try {
    // 更新学生档案
    await updateStudentInClass(selectedClass.value.id, editingStudent.value.id, {
      student_no: editStudentForm.value.student_no,
      attendance_rate: editStudentForm.value.attendance_rate,
      status: editStudentForm.value.status,
      full_name: editStudentForm.value.full_name,
      email: editStudentForm.value.email
    })

    // 更新成绩（只发送有值的成绩）
    const gradesData = {
      term: 'current'
    }
    if (editStudentForm.value.grades.chinese !== null && editStudentForm.value.grades.chinese !== undefined && editStudentForm.value.grades.chinese !== '') {
      gradesData.chinese = editStudentForm.value.grades.chinese
    }
    if (editStudentForm.value.grades.math !== null && editStudentForm.value.grades.math !== undefined && editStudentForm.value.grades.math !== '') {
      gradesData.math = editStudentForm.value.grades.math
    }
    if (editStudentForm.value.grades.english !== null && editStudentForm.value.grades.english !== undefined && editStudentForm.value.grades.english !== '') {
      gradesData.english = editStudentForm.value.grades.english
    }
    await updateStudentGrades(selectedClass.value.id, editingStudent.value.id, gradesData)

    await loadStudents(selectedClass.value.id)
    showEditStudentModal.value = false
    editingStudent.value = null
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to update student'
  } finally {
    isLoading.value = false
  }
}

// 删除学生
const handleRemoveStudent = async (student) => {
  if (!confirm(`Remove ${student.full_name} from this class?`)) {
    return
  }

  isLoading.value = true
  error.value = ''
  try {
    await removeStudentFromClass(selectedClass.value.id, student.id)
    await loadStudents(selectedClass.value.id)
    await loadClasses() // 更新班级学生数
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to remove student'
  } finally {
    isLoading.value = false
  }
}

// 获取成绩显示文本
const getGradeDisplay = (score) => {
  if (score === null || score === undefined) return '-'
  return Number(score).toFixed(0)
}

const formatAverageScore = (score) => {
  if (score === null || score === undefined) return '-'
  return Number(score).toFixed(2)
}

// 组件挂载时加载数据
onMounted(() => {
  loadClasses()
})
</script>

<template>
  <div class="class-mgmt-container">
    <div class="page-header">
      <div>
        <h1>Class Management</h1>
        <p>Manage classes and students</p>
      </div>
      <button @click="openCreateClassModal" class="create-btn">
        <Plus :size="20" />
        Add New Class
      </button>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="error-banner">
      {{ error }}
    </div>

    <!-- Class Grid -->
    <div v-if="!isLoading || classes.length > 0" class="classes-grid">
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
          <div class="card-actions">
            <button @click="openEditClassModal(classItem)" class="icon-btn" title="Edit class">
              <Edit :size="16" />
            </button>
            <button @click="handleDeleteClass(classItem)" class="icon-btn danger" title="Delete class">
              <Trash2 :size="16" />
            </button>
            <button @click="viewClassDetails(classItem)" class="view-btn">
              View Details
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading && classes.length === 0" class="loading-state">
      <p>Loading classes...</p>
    </div>

    <!-- Student List Section -->
    <div v-if="selectedClass" class="students-section">
      <div class="section-header">
        <h2>{{ selectedClass.name }} - Student Roster</h2>
        <button @click="openAddStudentModal" class="add-student-btn">
          <Plus :size="18" />
          Add Student
        </button>
      </div>

      <div v-if="isLoading && students.length === 0" class="loading-state">
        <p>Loading students...</p>
      </div>

      <div v-else-if="students.length === 0" class="empty-state">
        <p>No students in this class yet.</p>
      </div>

      <div v-else class="students-table-container">
        <table class="students-table">
          <thead>
            <tr>
              <th>Student ID</th>
              <th>Name</th>
              <th>Attendance</th>
              <th>Chinese</th>
              <th>Math</th>
              <th>English</th>
              <th>Average</th>
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
                  <span>{{ Math.round(student.attendance) }}%</span>
                  <div class="attendance-bar">
                    <div class="attendance-fill" :style="{ width: `${student.attendance}%` }"></div>
                  </div>
                </div>
              </td>
              <td><span class="grade-score">{{ getGradeDisplay(student.grades?.chinese) }}</span></td>
              <td><span class="grade-score">{{ getGradeDisplay(student.grades?.math) }}</span></td>
              <td><span class="grade-score">{{ getGradeDisplay(student.grades?.english) }}</span></td>
              <td>
                <span class="grade-score">
                  {{ formatAverageScore(student.averageScore) }}
                </span>
              </td>
              <td><span class="status-badge" :class="student.status">{{ student.status }}</span></td>
              <td>
                <div class="table-actions">
                  <button @click="openEditStudentModal(student)" class="icon-btn" title="Edit">
                    <Edit :size="16" />
                  </button>
                  <button @click="handleRemoveStudent(student)" class="icon-btn danger" title="Remove">
                    <Trash2 :size="16" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add Student Modal -->
    <div v-if="showAddStudentModal" class="modal-overlay" @click="showAddStudentModal = false">
      <div class="modal-content" @click.stop>
        <h2>Add Student to Class</h2>

        <form @submit.prevent="handleAddStudent" class="form">
          <div class="form-group">
            <label>Full Name *</label>
            <input v-model="newStudent.full_name" type="text" placeholder="Enter full name" required />
          </div>

          <div class="form-group">
            <label>Username (optional)</label>
            <input v-model="newStudent.username" type="text" placeholder="auto derived from student number if empty" />
          </div>

          <div class="form-group">
            <label>Email</label>
            <input v-model="newStudent.email" type="email" placeholder="student@example.com" />
          </div>

          <div class="form-group">
            <label>Student Number *</label>
            <input v-model="newStudent.student_no" type="text" placeholder="e.g., S001" required />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Attendance Rate (%)</label>
              <input v-model.number="newStudent.attendance_rate" type="number" min="0" max="100" placeholder="0-100" />
            </div>

            <div class="form-group">
              <label>Status</label>
              <select v-model="newStudent.status">
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>
          </div>

          <div class="grades-section">
            <h3>Grades (1-100 points)</h3>
            <div class="form-row">
              <div class="form-group">
                <label>Chinese</label>
                <input v-model.number="newStudent.grades.chinese" type="number" min="0" max="100" placeholder="0-100" />
              </div>

              <div class="form-group">
                <label>Math</label>
                <input v-model.number="newStudent.grades.math" type="number" min="0" max="100" placeholder="0-100" />
              </div>

              <div class="form-group">
                <label>English</label>
                <input v-model.number="newStudent.grades.english" type="number" min="0" max="100" placeholder="0-100" />
              </div>
            </div>
          </div>

          <div v-if="error" class="form-error">
            {{ error }}
          </div>

          <div class="modal-actions">
            <button type="button" @click="showAddStudentModal = false" class="btn-secondary">Cancel</button>
            <button type="submit" :disabled="isLoading" class="btn-primary">
              {{ isLoading ? 'Adding...' : 'Add Student' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit Class Modal -->
    <div v-if="showEditClassModal" class="modal-overlay" @click="showEditClassModal = false">
      <div class="modal-content" @click.stop>
        <h2>Edit Class</h2>
        <form @submit.prevent="handleUpdateClass" class="form">
          <div class="form-group">
            <label>Class Name *</label>
            <input v-model="editClassForm.name" type="text" required />
          </div>
          <div class="form-group">
            <label>Grade *</label>
            <select v-model="editClassForm.grade" required>
              <option value="Grade 1">Grade 1</option>
              <option value="Grade 2">Grade 2</option>
              <option value="Grade 3">Grade 3</option>
              <option value="Grade 4">Grade 4</option>
              <option value="Grade 5">Grade 5</option>
              <option value="Grade 6">Grade 6</option>
            </select>
          </div>
          <div class="form-group" v-if="auth.isAdmin">
            <label>Teacher (Optional)</label>
            <select v-model.number="editClassForm.teacher_id">
              <option :value="null">No teacher assigned</option>
              <option v-for="t in teachers" :key="t.id" :value="t.id">{{ t.full_name }}</option>
            </select>
          </div>
          <div v-if="error" class="form-error">{{ error }}</div>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="showEditClassModal = false">Cancel</button>
            <button type="submit" :disabled="isUpdatingClass" class="btn-primary">{{ isUpdatingClass ? 'Saving...' :
              'Save Changes' }}</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit Student Modal -->
    <div v-if="showEditStudentModal" class="modal-overlay" @click="showEditStudentModal = false">
      <div class="modal-content large" @click.stop>
        <h2>Edit Student Information</h2>

        <form @submit.prevent="handleUpdateStudent" class="form">
          <div class="form-row">
            <div class="form-group">
              <label>Full Name *</label>
              <input v-model="editStudentForm.full_name" type="text" required />
            </div>

            <div class="form-group">
              <label>Email</label>
              <input v-model="editStudentForm.email" type="email" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Student Number</label>
              <input v-model="editStudentForm.student_no" type="text" />
            </div>

            <div class="form-group">
              <label>Attendance Rate (%)</label>
              <input v-model.number="editStudentForm.attendance_rate" type="number" min="0" max="100" />
            </div>
          </div>

          <div class="form-group">
            <label>Status</label>
            <select v-model="editStudentForm.status">
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>

          <div class="grades-section">
            <h3>Grades (1-100 points)</h3>
            <div class="form-row">
              <div class="form-group">
                <label>Chinese</label>
                <input v-model.number="editStudentForm.grades.chinese" type="number" min="0" max="100"
                  placeholder="0-100" />
              </div>

              <div class="form-group">
                <label>Math</label>
                <input v-model.number="editStudentForm.grades.math" type="number" min="0" max="100"
                  placeholder="0-100" />
              </div>

              <div class="form-group">
                <label>English</label>
                <input v-model.number="editStudentForm.grades.english" type="number" min="0" max="100"
                  placeholder="0-100" />
              </div>
            </div>
          </div>

          <div v-if="error" class="form-error">
            {{ error }}
          </div>

          <div class="modal-actions">
            <button type="button" @click="showEditStudentModal = false" class="btn-secondary">Cancel</button>
            <button type="submit" :disabled="isLoading" class="btn-primary">
              {{ isLoading ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Create Class Modal -->
    <div v-if="showCreateClassModal" class="modal-overlay" @click="showCreateClassModal = false">
      <div class="modal-content" @click.stop>
        <h2>Create New Class</h2>

        <form @submit.prevent="handleCreateClass" class="form">
          <div class="form-group">
            <label>Class Name *</label>
            <input v-model="newClass.name" type="text" placeholder="e.g., Class 1A" required />
          </div>

          <div class="form-group">
            <label>Grade *</label>
            <select v-model="newClass.grade" required>
              <option value="">Select a grade</option>
              <option value="Grade 1">Grade 1</option>
              <option value="Grade 2">Grade 2</option>
              <option value="Grade 3">Grade 3</option>
              <option value="Grade 4">Grade 4</option>
              <option value="Grade 5">Grade 5</option>
              <option value="Grade 6">Grade 6</option>
            </select>
          </div>

          <div class="form-group" v-if="auth.isAdmin">
            <label>Teacher (Optional)</label>
            <select v-model.number="newClass.teacher_id">
              <option :value="null">No teacher assigned</option>
              <option v-for="teacher in teachers" :key="teacher.id" :value="teacher.id">
                {{ teacher.full_name }}
              </option>
            </select>
          </div>
          <div class="form-group" v-else>
            <label>Teacher</label>
            <input type="text" value="Assigned to current teacher" disabled />
            <span class="hint">This class will be assigned to your account.</span>
          </div>

          <div v-if="error" class="form-error">
            {{ error }}
          </div>

          <div class="modal-actions">
            <button type="button" @click="showCreateClassModal = false" class="btn-secondary">Cancel</button>
            <button type="submit" :disabled="isCreatingClass" class="btn-primary">
              {{ isCreatingClass ? 'Creating...' : 'Create Class' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.class-mgmt-container {
  max-width: 1400px;
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
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.create-btn:hover {
  background-color: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.error-banner {
  background-color: #fef2f2;
  color: #ef4444;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid #fecaca;
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

.card-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.hint {
  font-size: 0.8125rem;
  color: var(--text-light);
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
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
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
  cursor: pointer;
  transition: all 0.2s;
}

.add-student-btn:hover {
  background-color: var(--primary);
  color: white;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-muted);
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

.grade-score {
  font-weight: 500;
  color: var(--text-main);
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

.status-badge.inactive {
  background-color: #fee2e2;
  color: #dc2626;
}

.table-actions {
  display: flex;
  gap: 0.5rem;
}

.icon-btn {
  padding: 0.375rem;
  border-radius: 0.375rem;
  font-size: 0.8125rem;
  font-weight: 500;
  background-color: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
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
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content.large {
  max-width: 700px;
}

.modal-content h2 {
  margin-bottom: 1.5rem;
  color: var(--text-main);
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-main);
}

.form-group input,
.form-group select {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  font-size: 0.9375rem;
  color: var(--text-main);
  background-color: var(--bg-body);
  transition: all 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.grades-section {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.grades-section h3 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-main);
  margin-bottom: 1rem;
}

.form-error {
  color: #ef4444;
  font-size: 0.875rem;
  background-color: #fef2f2;
  padding: 0.75rem;
  border-radius: 0.5rem;
}

.modal-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-top: 1rem;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-primary {
  background-color: var(--primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--primary-hover);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover {
  background-color: var(--bg-body);
  color: var(--text-main);
}

.close-btn {
  background-color: var(--primary);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
}
</style>
