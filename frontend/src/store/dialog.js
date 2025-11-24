import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useDialogStore = defineStore('dialog', () => {
    const type = ref(''); // 'success', 'danger', 'warning', 'info' for bootstrap alert
    const show = ref(false);
    const content = ref({
        'title': '',
        'firstLine': '',
        'secondLine': '',
    })

    const isShow = computed(() => show.value);
    const dialogContent = computed(() => content.value);
    const dialogType = computed(() => type.value);


    async function setSuccess(newContent) {
        show.value = true;
        type.value = 'success';
        content.value = newContent;
    }

    async function setError(newContent) {
        show.value = true;
        type.value = 'danger';
        content.value = newContent;
    }

    async function setWarning(newContent) {
        show.value = true;
        type.value = 'warning';
        content.value = newContent;
    }

    async function setInfo(newContent) {
        show.value = true;
        type.value = 'info';
        content.value = newContent;
    }

    async function reset() {
        show.value = false;
    }

    return {
        dialogContent,
        isShow,
        dialogType,
        setSuccess,
        setError,
        setWarning,
        setInfo,
        reset
    }
})