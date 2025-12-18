import api from './index.js'

// Dashboard aggregation statistics
export const getDashboardSummary = async () => {
  const res = await api.get('/admin/dashboard/summary')
  return res.data
}

