import api from './index.js'

/**
 * 获取通知列表
 * @param {Object} filters - 过滤条件 { priority, category }
 */
export const getNotices = async (filters = {}) => {
    const params = {}
    if (filters.priority) params.priority = filters.priority
    if (filters.category) params.category = filters.category
    
    const response = await api.get('/admin/notices', { params })
    return response.data
}

/**
 * 获取单个通知详情
 * @param {number} id - 通知ID
 */
export const getNotice = async (id) => {
    const response = await api.get(`/admin/notices/${id}`)
    return response.data
}

/**
 * 创建通知
 * @param {Object} noticeData - 通知数据
 */
export const createNotice = async (noticeData) => {
    const response = await api.post('/admin/notices', {
        title: noticeData.title,
        content: noticeData.content,
        date: noticeData.date,
        priority: noticeData.priority || 'normal',
        category: noticeData.category || ''
    })
    return response.data
}

/**
 * 更新通知
 * @param {number} id - 通知ID
 * @param {Object} noticeData - 更新的通知数据
 */
export const updateNotice = async (id, noticeData) => {
    const response = await api.put(`/admin/notices/${id}`, {
        title: noticeData.title,
        content: noticeData.content,
        date: noticeData.date,
        priority: noticeData.priority,
        category: noticeData.category
    })
    return response.data
}

/**
 * 删除通知
 * @param {number} id - 通知ID
 */
export const deleteNotice = async (id) => {
    const response = await api.delete(`/admin/notices/${id}`)
    return response.data
}


