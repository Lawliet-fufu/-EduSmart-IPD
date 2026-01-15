import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { translations } from '../utils/i18n.js'

export const useLocaleStore = defineStore('locale', () => {
    // 从 localStorage 读取，默认中文
    const locale = ref(localStorage.getItem('pref_language') || 'zh')

    // 翻译函数
    const t = computed(() => {
        return (key) => {
            const keys = key.split('.')
            let value = translations[locale.value]

            for (const k of keys) {
                value = value?.[k]
            }

            return value || key
        }
    })

    // 切换语言
    function setLocale(newLocale) {
        locale.value = newLocale
        localStorage.setItem('pref_language', newLocale)
    }

    return {
        locale,
        t,
        setLocale
    }
})
