import api from './index.js'

/**
 * Obtain the list of assignments
 * @param {Object} filters - filter condition
 { status, subject }
 */
export const getAssignments = async (filters = {}) => {
    const params = {}
    if (filters.status) params.status = filters.status
    if (filters.subject) params.subject = filters.subject
    
    const response = await api.get('/teacher-tasks/assignments', { params })
    return response.data
}

/**
 * Create an assignment
 * @param {Object} assignmentData - Assignment data
 */
export const createAssignment = async (assignmentData) => {
    const response = await api.post('/teacher-tasks/assignments', {
        title: assignmentData.title,
        subject: assignmentData.subject,
        description: assignmentData.description || '',
        dueDate: assignmentData.dueDate,
        class_id: assignmentData.class_id,
        status: assignmentData.status || 'pending'
    })
    return response.data
}

/**
 * Update the assignment
 * @param {number} id - Assignment ID
 * @param {Object} assignmentData - Updated job data
 */
export const updateAssignment = async (id, assignmentData) => {
    const response = await api.put(`/teacher-tasks/assignments/${id}`, {
        title: assignmentData.title,
        subject: assignmentData.subject,
        description: assignmentData.description,
        dueDate: assignmentData.dueDate,
        status: assignmentData.status,
        class_id: assignmentData.class_id
    })
    return response.data
}

/**
 * Delete the assignment
 * @param {number} id - 作业ID
 */
export const deleteAssignment = async (id) => {
    const response = await api.delete(`/teacher-tasks/assignments/${id}`)
    return response.data
}