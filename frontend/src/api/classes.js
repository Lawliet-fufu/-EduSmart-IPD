import api from './index.js'

/**
 * 获取班级列表
 */
export const getClasses = async () => {
    const response = await api.get('/admin/classes')
    return response.data
}

/**
 * 创建班级
 * @param {Object} classData - 班级数据 { name, grade, teacher_id, students_count, avg_attendance }
 */
export const createClass = async (classData) => {
    const response = await api.post('/admin/classes', classData)
    return response.data
}

/**
 * 更新班级
 * @param {number} id - 班级ID
 * @param {Object} classData - 更新的班级数据
 */
export const updateClass = async (id, classData) => {
    const response = await api.put(`/admin/classes/${id}`, classData)
    return response.data
}

/**
 * 删除班级
 * @param {number} id - 班级ID
 */
export const deleteClass = async (id) => {
    const response = await api.delete(`/admin/classes/${id}`)
    return response.data
}

/**
 * 获取班级学生列表
 * @param {number} classId - 班级ID
 */
export const getClassStudents = async (classId) => {
    const response = await api.get(`/admin/classes/${classId}/students`)
    return response.data
}

/**
 * 添加学生到班级
 * @param {number} classId - 班级ID
 * @param {Object} studentData - 学生数据 { user_id, student_no }
 */
export const addStudentToClass = async (classId, studentData) => {
    const response = await api.post(`/admin/classes/${classId}/students`, studentData)
    return response.data
}

/**
 * 更新班级中的学生信息
 * @param {number} classId - 班级ID
 * @param {number} studentId - 学生档案ID
 * @param {Object} studentData - 更新的学生数据
 */
export const updateStudentInClass = async (classId, studentId, studentData) => {
    const response = await api.put(`/admin/classes/${classId}/students/${studentId}`, studentData)
    return response.data
}

/**
 * 从班级中移除学生
 * @param {number} classId - 班级ID
 * @param {number} studentId - 学生档案ID
 */
export const removeStudentFromClass = async (classId, studentId) => {
    const response = await api.delete(`/admin/classes/${classId}/students/${studentId}`)
    return response.data
}

/**
 * 获取学生成绩
 * @param {number} classId - 班级ID
 * @param {number} studentId - 学生档案ID
 */
export const getStudentGrades = async (classId, studentId) => {
    const response = await api.get(`/admin/classes/${classId}/students/${studentId}/grades`)
    return response.data
}

/**
 * 更新学生成绩
 * @param {number} classId - 班级ID
 * @param {number} studentId - 学生档案ID
 * @param {Object} gradesData - 成绩数据 { chinese, math, english, term }
 */
export const updateStudentGrades = async (classId, studentId, gradesData) => {
    const response = await api.post(`/admin/classes/${classId}/students/${studentId}/grades`, gradesData)
    return response.data
}

/**
 * 获取所有用户（用于添加学生时选择）
 * @param {string} role - 角色过滤（可选）
 */
export const getUsers = async (role = null) => {
    const params = role ? { role } : {}
    const response = await api.get('/admin/users', { params })
    return response.data
}

/**
 * 获取某个班级的成绩分布（0-100 分 -> 人数）
 * @param {number} classId - 班级ID
 * @param {string} term - 学期，可选，默认 current
 */
export const getClassGradeDistribution = async (classId, term = 'current') => {
    const response = await api.get(`/admin/classes/${classId}/grade-distribution`, { params: { term } })
    return response.data
}

