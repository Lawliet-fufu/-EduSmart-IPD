// 简化的语言包 - 不需要 vue-i18n
// Simplified language pack - no vue-i18n needed

export const translations = {
    zh: {
        // 导航
        nav: {
            dashboard: '仪表板',
            assignments: '作业',
            notices: '通知',
            classes: '班级',
            aiAssistant: 'AI 助手',
            settings: '设置',
            logout: '退出登录'
        },
        // 设置页面
        settings: {
            title: '设置',
            description: '管理您的账户和偏好设置',
            profile: '个人信息',
            fullName: '姓名',
            email: '电子邮箱',
            role: '角色',
            security: '安全',
            currentPassword: '当前密码',
            newPassword: '新密码',
            confirmPassword: '确认新密码',
            preferences: '通知与偏好',
            pushNotifications: '推送通知',
            pushNotificationsDesc: '接收重要更新的通知',
            emailAlerts: '邮件提醒',
            emailAlertsDesc: '接收新作业的邮件通知',
            darkMode: '深色模式',
            darkModeDesc: '切换到深色主题',
            language: '语言',
            languageDesc: '选择您偏好的语言',
            saveChanges: '保存更改',
            saving: '保存中...',
            saveSuccess: '设置保存成功！',
            saveFailed: '保存失败，请重试。'
        },
        // 通用
        common: {
            loading: '加载中...',
            save: '保存',
            cancel: '取消',
            confirm: '确认',
            delete: '删除',
            edit: '编辑',
            add: '添加',
            search: '搜索',
            filter: '筛选',
            all: '全部',
            yes: '是',
            no: '否'
        }
    },
    en: {
        // Navigation
        nav: {
            dashboard: 'Dashboard',
            assignments: 'Assignments',
            notices: 'Notices',
            classes: 'Classes',
            aiAssistant: 'AI Assistant',
            settings: 'Settings',
            logout: 'Logout'
        },
        // Settings page
        settings: {
            title: 'Settings',
            description: 'Manage your account and preferences',
            profile: 'Profile Information',
            fullName: 'Full Name',
            email: 'Email Address',
            role: 'Role',
            security: 'Security',
            currentPassword: 'Current Password',
            newPassword: 'New Password',
            confirmPassword: 'Confirm New Password',
            preferences: 'Notifications & Preferences',
            pushNotifications: 'Push Notifications',
            pushNotificationsDesc: 'Receive notifications about important updates',
            emailAlerts: 'Email Alerts',
            emailAlertsDesc: 'Get email notifications for new assignments',
            darkMode: 'Dark Mode',
            darkModeDesc: 'Switch to dark theme',
            language: 'Language',
            languageDesc: 'Select your preferred language',
            saveChanges: 'Save Changes',
            saving: 'Saving...',
            saveSuccess: 'Settings saved successfully!',
            saveFailed: 'Failed to save settings. Please try again.'
        },
        // Common
        common: {
            loading: 'Loading...',
            save: 'Save',
            cancel: 'Cancel',
            confirm: 'Confirm',
            delete: 'Delete',
            edit: 'Edit',
            add: 'Add',
            search: 'Search',
            filter: 'Filter',
            all: 'All',
            yes: 'Yes',
            no: 'No'
        }
    }
}

// 简单的翻译函数
export function useTranslation(locale) {
    const t = (key) => {
        const keys = key.split('.')
        let value = translations[locale]

        for (const k of keys) {
            value = value?.[k]
        }

        return value || key
    }

    return { t }
}
